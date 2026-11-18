"""
Strona internetowa aplikacji Safe Budget.

Uruchomienie lokalne (podgląd na żywo):
    pip install -r requirements.txt
    python flask_app.py            → http://localhost:5000

Wersja statyczna (zwykłe pliki HTML do GitHub Pages / dowolnego hostingu):
    python freeze.py               → folder build/

Treść strony jest w słownikach poniżej, wygląd — w templates/ i static/.
"""
import os
from datetime import date

from flask import Flask, render_template

app = Flask(__name__)

# ------------------------------------------------------------------ USTAWIENIA
# Link do Sklepu Google Play — wpisz, gdy aplikacja zostanie opublikowana.
# Dopóki jest None, strona pokazuje „Wkrótce w Google Play”.
GOOGLE_PLAY_URL = None  # np. "https://play.google.com/store/apps/details?id=pl.safebudget.app"

AUTOR = {
    "imie": "Paweł Fryc",
    "email": "safebudget@interia.pl",
}

# Pełny adres strony (do sitemap.xml i podglądu linków). Przy publikacji ustawia go zmienna środowiskowa.
ADRES_STRONY = os.environ.get("ADRES_STRONY", "https://safebudget.eu").rstrip("/")
DNI_PROBY = 7

# ------------------------------------------------------------------ TREŚĆ
FUNKCJE = [
    ("💰", "Plan i wykonanie", "Zaplanuj wpływy i wydatki na okres, a aplikacja na bieżąco pokaże, ile już wydałeś i ile zostało."),
    ("⬇️", "Import z banku", "Wczytaj wyciąg CSV, Excel lub PDF — transakcje same trafią do właściwych kategorii, bez duplikatów."),
    ("🏷️", "Automatyczne kategorie", "Reguły ze słowami kluczowymi i wbudowany słownik sklepów z wielu krajów porządkują wydatki za Ciebie."),
    ("📊", "Statystyki i trend", "Wykresy wydatków według kategorii oraz porównanie okresów pokazują, dokąd naprawdę idą pieniądze."),
    ("🔁", "Stałe opłaty", "Czynsz, raty, abonamenty — od razu widzisz, co już zapłacone, a co jest po terminie."),
    ("🏢", "Budżet domowy i firmowy", "Dwa osobne budżety w jednej aplikacji — przełączasz je jednym dotknięciem."),
    ("📅", "Własne okresy", "Okres rozliczeniowy może zaczynać się w dniu wypłaty, a nie pierwszego dnia miesiąca."),
    ("🌍", "12 języków", "Polski, angielski, niemiecki, francuski, hiszpański, włoski, portugalski, indonezyjski, chiński, hindi, bengalski i arabski."),
]

# Zrzuty ekranu: (plik w static/img/zrzuty, tytuł, podpis)
ZRZUTY = [
    ("budzet", "Budżet", "Saldo okresu, plan i wykonanie w jednym miejscu"),
    ("transakcje", "Transakcje", "Wyszukiwanie, filtry i szybka zmiana kategorii"),
    ("statystyki", "Statystyki", "Wydatki według kategorii i okresów"),
    ("trend", "Trend okresów", "Jak zmieniają się wydatki z miesiąca na miesiąc"),
    ("podglad", "Import z banku", "Podgląd przed zapisem — duplikaty są pomijane"),
    ("oplaty", "Stałe opłaty", "Co zapłacone, a co jeszcze czeka"),
    ("plan", "Plan", "Planowanie pozycji budżetu na okres"),
    ("kopia", "Kopia zapasowa", "Excel, plik bazy i szyfrowana kopia automatyczna"),
    ("blokada", "Blokada PIN-em", "PIN lub odcisk palca przy każdym uruchomieniu"),
]

# Ta sama treść, co w aplikacji: Więcej → O aplikacji → Bezpieczeństwo i prywatność
BEZPIECZENSTWO = [
    ("📴", "Działa w pełni offline.",
     "Aplikacja nie potrzebuje internetu i niczego nie wysyła — nie ma kont, reklam, śledzenia ani statystyk użycia. "
     "Pliki z banku są odczytywane wyłącznie w telefonie. Internet jest potrzebny tylko do zakupu wersji Pro "
     "w Sklepie Google Play — bez żadnych danych z budżetu."),
    ("🔐", "Dane są zaszyfrowane.",
     "Budżet zapisany w telefonie jest zaszyfrowany algorytmem AES-256-GCM. Klucz do danych jest chroniony Twoim PIN-em "
     "(PBKDF2-SHA-256, 400 000 powtórzeń), a sam PIN nie jest nigdzie zapisywany. Bez PIN-u albo odcisku palca danych "
     "nie da się odczytać — nawet po skopiowaniu plików z telefonu."),
    ("🧠", "Odszyfrowane dane są tylko w pamięci.",
     "Aplikacja odszyfrowuje budżet dopiero po odblokowaniu i trzyma go wyłącznie w pamięci — na dysku budżet "
     "jest zawsze zaszyfrowany."),
    ("🔢", "Blokada PIN-em.",
     "PIN (od 4 do 8 cyfr) jest potrzebny przy każdym uruchomieniu, a aplikacja blokuje się sama po czasie bezczynności "
     "(domyślnie po 5 minutach). Po 5 błędnych próbach trzeba odczekać 30 sekund, a po każdej kolejnej — dwa razy dłużej "
     "(najwyżej 15 minut)."),
    ("👆", "Odcisk palca.",
     "Gdy go włączysz, klucz do danych jest przechowywany w bezpiecznym magazynie kluczy telefonu (Android Keystore) "
     "i wydawany dopiero po przyłożeniu palca. PIN zawsze pozostaje zapasowym sposobem odblokowania."),
    ("💾", "Bezpieczny zapis.",
     "Każda zmiana trafia najpierw do pliku tymczasowego i dopiero potem zastępuje poprzednią wersję — wyłączenie "
     "telefonu w trakcie zapisu nie psuje danych."),
    ("☁️", "Kopie zapasowe.",
     "Kopia automatyczna jest zaszyfrowana i trafia tylko do folderu, który sam wybierzesz — aplikacja ma dostęp "
     "wyłącznie do niego. Na innym telefonie otworzysz ją tylko PIN-em z chwili zapisu kopii. Kopie Excel i pliku bazy "
     "zapisane ręcznie nie są zaszyfrowane — przechowuj je w bezpiecznym miejscu."),
    ("📱", "Bez zbędnych uprawnień.",
     "Aplikacja nie korzysta z kontaktów, lokalizacji, aparatu ani mikrofonu. Do plików ma dostęp tylko wtedy, "
     "gdy sam je wskażesz (import, wczytanie kopii) albo wybierzesz folder kopii automatycznej."),
    ("🗝️", "Nikt nie odzyska Twojego PIN-u.",
     "Nie zna go ani autor aplikacji, ani nikt inny, więc nikt poza Tobą nie odczyta Twoich danych. Gdy zapomnisz PIN, "
     "jedynym wyjściem jest wyczyszczenie danych aplikacji — dlatego rób regularnie kopię zapasową."),
]

PRO = {
    "darmowe": ["Budżet i plan", "Transakcje", "Kategorie i reguły", "Okresy rozliczeniowe", "Kopia w pliku bazy danych"],
    "pro": ["Import z banku", "Budżet firmowy", "Statystyki", "Trend okresów", "Stałe opłaty",
            "Kopia automatyczna szyfrowana", "Eksport do Excela"],
}

FAQ = [
    ("Czy aplikacja wymaga konta lub internetu?",
     "Nie. Safe Budget działa w pełni offline i nie ma żadnych kont. Twoje dane nigdy nie trafiają na serwer autora."),
    ("Z jakich banków mogę importować wyciągi?",
     "Aplikacja czyta pliki CSV, Excel (XLSX) i PDF z wyciągami. W podglądzie importu widzisz wszystko przed zapisem, "
     "a transakcje już zaimportowane są pomijane."),
    ("Co się stanie, gdy zmienię telefon?",
     "Zapisz kopię budzet.db albo włącz szyfrowaną kopię automatyczną do wybranego folderu (np. w Dysku Google). "
     "Na nowym telefonie wczytasz ją jednym przyciskiem."),
    ("Co jeśli zapomnę PIN?",
     "PIN-u nie da się odzyskać — nie zna go nikt poza Tobą. Dlatego warto regularnie robić kopię zapasową."),
    ("Ile kosztuje aplikacja?",
     f"Przez pierwsze {DNI_PROBY} dni wszystkie funkcje są dostępne za darmo. Potem podstawowe funkcje pozostają darmowe, "
     "a wersja Pro to jednorazowy zakup — bez subskrypcji i bez reklam."),
]


@app.context_processor
def wspolne():
    return {
        "GOOGLE_PLAY_URL": GOOGLE_PLAY_URL,
        "AUTOR": AUTOR,
        "ADRES_STRONY": ADRES_STRONY,
        "rok": date.today().year,
    }


# ------------------------------------------------------------------ WIDOKI
@app.route("/")
def strona_glowna():
    return render_template(
        "index.html",
        funkcje=FUNKCJE, zrzuty=ZRZUTY, bezpieczenstwo=BEZPIECZENSTWO,
        pro=PRO, faq=FAQ, dni_proby=DNI_PROBY,
    )


# Adresy podstron kończą się „/”, bo w wersji statycznej każda to folder z plikiem index.html.
@app.route("/polityka-prywatnosci/")
def polityka():
    # Adres tej podstrony można podać w Konsoli Google Play jako „Polityka prywatności”.
    return render_template("polityka.html", bezpieczenstwo=BEZPIECZENSTWO, data=date(2026, 11, 18))


@app.route("/pobierz/")
def pobierz():
    """Stały, krótki adres do ulotek i kodu QR — przekierowuje do Sklepu Google Play (albo do sekcji Pobierz)."""
    return render_template("pobierz.html")


@app.route("/robots.txt")
def robots():
    return app.response_class(f"User-agent: *\nAllow: /\nSitemap: {ADRES_STRONY}/sitemap.xml\n", mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap():
    adresy = ["/", "/polityka-prywatnosci/"]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml += [f"  <url><loc>{ADRES_STRONY}{a}</loc></url>" for a in adresy]
    xml.append("</urlset>")
    return app.response_class("\n".join(xml), mimetype="application/xml")


@app.route("/404.html")
def strona_404():
    """Wersja statyczna: GitHub Pages pokazuje plik 404.html przy nieistniejących adresach."""
    return render_template("404.html")


@app.errorhandler(404)
def nie_znaleziono(_):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
