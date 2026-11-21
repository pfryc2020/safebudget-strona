"""
Strona internetowa aplikacji Safe Budget — https://safebudget.eu

Uruchomienie lokalne (podgląd na żywo):
    pip install -r requirements.txt
    python flask_app.py            → http://localhost:5000

Wersja statyczna (zwykłe pliki HTML do GitHub Pages / dowolnego hostingu):
    python freeze.py               → folder build/

Teksty strony są w tlumaczenia/<język>.json (polski to wzór dla pozostałych),
wygląd — w templates/ i static/.
"""
import json
import os
from datetime import date
from pathlib import Path

from flask import Flask, render_template, request, url_for
from markupsafe import Markup, escape

KATALOG = Path(__file__).resolve().parent
app = Flask(__name__)

# ------------------------------------------------------------------ USTAWIENIA
# Link do Sklepu Google Play — wpisz, gdy aplikacja zostanie opublikowana.
# Dopóki jest None, strona pokazuje „Wkrótce w Google Play”.
GOOGLE_PLAY_URL = None  # np. "https://play.google.com/store/apps/details?id=pl.safebudget.app"

AUTOR = {
    "imie": "Paweł Fryc",
    "email": "office@safebudget.eu",
}

# Pełny adres strony (do sitemap.xml, hreflang i podglądu linków). Przy publikacji ustawia go zmienna środowiskowa.
ADRES_STRONY = os.environ.get("ADRES_STRONY", "https://safebudget.eu").rstrip("/")
DNI_PROBY = 7
DATA_POLITYKI = date(2026, 11, 19)

# ------------------------------------------------------------------ JĘZYKI
# Kolejność jak w aplikacji. Polski jest pod adresem głównym (/), pozostałe pod /<kod>/.
JEZYKI = ["pl", "en", "de", "fr", "es", "it", "pt", "id", "zh", "hi", "bn", "ar"]
DOMYSLNY = "pl"
INNE = [j for j in JEZYKI if j != DOMYSLNY]
KOD_JEZYKA = f"any({', '.join(INNE)})"           # konwerter adresów: /en/, /de/ … (inne kody → 404)


def wczytaj_tlumaczenia():
    tl = {}
    for j in JEZYKI:
        plik = KATALOG / "tlumaczenia" / f"{j}.json"
        try:
            tl[j] = json.loads(plik.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            # czytelny komunikat w logu GitHub Actions po ręcznej edycji tekstów
            linia = e.doc.splitlines()[e.lineno - 1] if e.lineno <= len(e.doc.splitlines()) else ""
            raise SystemExit(
                f"\nBŁĄD w pliku tlumaczenia/{j}.json, wiersz {e.lineno}, znak {e.colno}: {e.msg}\n"
                f"    {linia.strip()}\n"
                "(błąd może być też w wierszu powyżej)\n"
                "Najczęstsze przyczyny: brak przecinka między wierszami, przecinek po ostatnim elemencie,\n"
                "cudzysłów \" wewnątrz tekstu (użyj „ ” albo \\\").\n"
            ) from None
    return tl


def _klucze(obiekt, sciezka=""):
    if isinstance(obiekt, dict):
        for k, v in obiekt.items():
            yield from _klucze(v, f"{sciezka}.{k}" if sciezka else k)
    elif isinstance(obiekt, list):
        yield f"{sciezka}[{len(obiekt)}]"
        for i, v in enumerate(obiekt):
            yield from _klucze(v, f"{sciezka}[{i}]")
    else:
        yield sciezka


def sprawdz_tlumaczenia(tl):
    """Każdy język musi mieć dokładnie te same teksty (klucze i długości list) co polski."""
    wzor = set(_klucze(tl[DOMYSLNY]))
    bledy = []
    for j in INNE:
        klucze = set(_klucze(tl[j]))
        bledy += [f"{j}: brak {k}" for k in sorted(wzor - klucze)]
        bledy += [f"{j}: nadmiarowy {k}" for k in sorted(klucze - wzor)]
    return bledy


T = wczytaj_tlumaczenia()

# ------------------------------------------------------------------ TREŚĆ NIEZALEŻNA OD JĘZYKA
# (identyfikator tekstu w tlumaczenia/*.json, ikona)
FUNKCJE = [("plan", "💰"), ("import", "⬇️"), ("kategorie", "🏷️"), ("statystyki", "📊"),
           ("oplaty", "🔁"), ("firma", "🏢"), ("okresy", "📅"), ("jezyki", "🌍")]
# zrzuty ekranu: static/img/zrzuty/<język>/<nazwa>.webp
ZRZUTY = ["budzet", "transakcje", "statystyki", "trend", "podglad", "oplaty", "plan", "kopia", "blokada"]
# punkty „Bezpieczeństwo i prywatność” — teksty takie same jak w aplikacji (Więcej → O aplikacji)
IKONY_BEZPIECZENSTWA = {"offline": "📴", "szyfrowanie": "🔐", "pamiec": "🧠", "pin": "🔢", "odcisk": "👆",
                        "zapis": "💾", "kopie": "☁️", "uprawnienia": "📱", "odzyskanie": "🗝️"}


@app.template_filter("wstaw")
def wstaw(tekst, **wartosci):
    """Wstawia wartości w miejsca {nazwa} — np. {{ T.pobierz.tekst | wstaw(n=7) }}."""
    for klucz, wartosc in wartosci.items():
        tekst = tekst.replace("{" + klucz + "}", str(wartosc))
    return tekst


def data_w_jezyku(d, wzor):
    return wzor.replace("YYYY", f"{d.year:04d}").replace("MM", f"{d.month:02d}").replace("DD", f"{d.day:02d}")


def adres_strony_glownej(jezyk):
    return url_for("strona_glowna", jezyk=jezyk)


@app.context_processor
def wspolne():
    jezyk = (request.view_args or {}).get("jezyk", DOMYSLNY)
    if jezyk not in T:
        jezyk = DOMYSLNY
    # strony dostępne we wszystkich językach mają odpowiedniki (hreflang, przełącznik języka, wykrywanie)
    wielojezyczna = request.endpoint in ("strona_glowna", "polityka")
    if wielojezyczna:
        odpowiedniki = {j: url_for(request.endpoint, jezyk=j) for j in JEZYKI}
    else:
        odpowiedniki = {j: adres_strony_glownej(j) for j in JEZYKI}
    return {
        "T": T[jezyk],
        "jezyk": jezyk,
        "DOMYSLNY": DOMYSLNY,
        "JEZYKI": [(j, T[j]["jezyk"]["nazwa"], T[j]["jezyk"]["html_lang"]) for j in JEZYKI],
        "wielojezyczna": wielojezyczna,
        "odpowiedniki": odpowiedniki,
        "glowna": adres_strony_glownej(jezyk),
        "GOOGLE_PLAY_URL": GOOGLE_PLAY_URL,
        "AUTOR": AUTOR,
        "ADRES_STRONY": ADRES_STRONY,
        "DNI_PROBY": DNI_PROBY,
        "rok": date.today().year,
    }


# ------------------------------------------------------------------ WIDOKI
@app.route("/", defaults={"jezyk": DOMYSLNY})
@app.route(f"/<{KOD_JEZYKA}:jezyk>/")
def strona_glowna(jezyk):
    return render_template(
        "index.html",
        funkcje=FUNKCJE, zrzuty=ZRZUTY, ikony_bezpieczenstwa=IKONY_BEZPIECZENSTWA,
    )


# Adresy podstron kończą się „/”, bo w wersji statycznej każda to folder z plikiem index.html.
# Polski adres zostaje ten sam (podany w Konsoli Google Play), inne języki: /<kod>/privacy/.
@app.route("/polityka-prywatnosci/", defaults={"jezyk": DOMYSLNY})
@app.route(f"/<{KOD_JEZYKA}:jezyk>/privacy/")
def polityka(jezyk):
    t = T[jezyk]
    email = Markup('<a href="mailto:{0}">{0}</a>').format(AUTOR["email"])
    sekcje = []
    for s in t["polityka"]["sekcje"]:
        if s["tresc"] == "{bezpieczenstwo}":
            sekcje.append({"tytul": s["tytul"], "bezpieczenstwo": True})
        else:
            tresc = s["tresc"].replace("{autor}", str(escape(AUTOR["imie"]))).replace("{email}", email)
            sekcje.append({"tytul": s["tytul"], "tresc": Markup(tresc)})
    return render_template(
        "polityka.html",
        sekcje=sekcje, ikony_bezpieczenstwa=IKONY_BEZPIECZENSTWA,
        data=data_w_jezyku(DATA_POLITYKI, t["jezyk"]["format_daty"]),
    )


@app.route("/pobierz/")
def pobierz():
    """Stały, krótki adres do ulotek i kodu QR — przekierowuje do Sklepu Google Play (albo do sekcji Pobierz)."""
    return render_template("pobierz.html")


@app.route("/robots.txt")
def robots():
    return app.response_class(f"User-agent: *\nAllow: /\nSitemap: {ADRES_STRONY}/sitemap.xml\n", mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap():
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for endpoint in ("strona_glowna", "polityka"):
        adresy = {j: ADRES_STRONY + url_for(endpoint, jezyk=j) for j in JEZYKI}
        for j in JEZYKI:
            xml.append(f"  <url><loc>{adresy[j]}</loc>")
            for k in JEZYKI:
                xml.append(f'    <xhtml:link rel="alternate" hreflang="{k}" href="{adresy[k]}"/>')
            xml.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{adresy[DOMYSLNY]}"/>')
            xml.append("  </url>")
    xml.append("</urlset>")
    return app.response_class("\n".join(xml), mimetype="application/xml")


def _strona_404():
    return render_template(
        "404.html",
        bledy404={j: T[j]["blad404"] for j in JEZYKI},
        kierunki={j: [T[j]["jezyk"]["html_lang"], T[j]["jezyk"]["kierunek"]] for j in JEZYKI},
    )


@app.route("/404.html")
def strona_404():
    """Wersja statyczna: GitHub Pages pokazuje plik 404.html przy nieistniejących adresach."""
    return _strona_404()


@app.errorhandler(404)
def nie_znaleziono(_):
    return _strona_404(), 404


if __name__ == "__main__":
    for blad in sprawdz_tlumaczenia(T):
        print("UWAGA tłumaczenia:", blad)
    app.run(debug=True)
