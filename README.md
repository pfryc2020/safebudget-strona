# Strona internetowa Safe Budget

> ✏️ **Chcesz samodzielnie zmienić teksty na stronie?** Zobacz [EDYCJA.md](EDYCJA.md) — edycja w przeglądarce, bez instalowania czegokolwiek.

Strona aplikacji pisana w Pythonie (Flask), w 12 językach. Publikowana jako **wersja statyczna**
(zwykłe pliki HTML) na **GitHub Pages** pod adresem **https://safebudget.eu** — hosting za 0 zł, z HTTPS.

```
safebudget-strona/
├── flask_app.py          ← adresy stron, języki, ustawienia (link do Google Play, autor)
├── freeze.py             ← zamiana na pliki HTML → build/ (sprawdza też kompletność tłumaczeń)
├── tlumaczenia/          ← teksty strony: pl.json (wzór) + en, de, fr, es, it, pt, id, zh, hi, bn, ar
├── templates/            ← base.html, index.html, polityka.html, pobierz.html, 404.html, …
├── static/
│   ├── css/style.css, js/strona.js
│   ├── img/zrzuty/<język>/*.webp   ← zrzuty ekranu aplikacji w każdym języku
│   ├── img/hero/<język>-1x/2x.webp ← obraz w nagłówku (robi go narzedzia/hero.py)
│   └── instrukcja/<język>.pdf      ← instrukcja obsługi w każdym języku
└── narzedzia/hero.py     ← generator obrazu w nagłówku (przechylone telefony bez pikseli)
```

## Adresy
| Strona | Polski (domyślny) | Inne języki |
|---|---|---|
| Strona główna | `/` | `/en/`, `/de/`, `/fr/`, `/es/`, `/it/`, `/pt/`, `/id/`, `/zh/`, `/hi/`, `/bn/`, `/ar/` |
| Polityka prywatności | `/polityka-prywatnosci/` (podany w Konsoli Google Play) | `/<kod>/privacy/` |

Do tego `/pobierz/` (krótki link do ulotek i kodu QR → Google Play), `/404.html`, `/sitemap.xml`, `/robots.txt`.

## Języki
- Przy pierwszej wizycie strona polska (`/` i `/polityka-prywatnosci/`) sprawdza język przeglądarki
  i przechodzi do odpowiedniej wersji, jeśli strona ją ma (np. przeglądarka po niemiecku → `/de/`).
  Gdy języka przeglądarki nie ma wśród 12, zostaje polski.
- Wybór z listy języków w nagłówku zapamiętuje się w przeglądarce i ma pierwszeństwo przed wykrywaniem.
- Roboty wyszukiwarek nie są przekierowywane; każda wersja ma znaczniki `hreflang`, a `sitemap.xml` wymienia wszystkie.
- Arabski wyświetla się od prawej do lewej (`dir="rtl"`).

### Zmiana tekstów
Teksty są w `tlumaczenia/<język>.json`. Wzorem jest `pl.json` — każdy język musi mieć te same klucze
(`python freeze.py` przerwie budowanie i wypisze, czego brakuje). W tekstach można używać `{n}` (liczba dni próbnych),
a w polityce prywatności `{autor}`, `{email}` i `{data}`. Fragmenty `bezpieczenstwo.lista` i `pobierz.lista_pro`
są przepisane 1:1 z tłumaczeń aplikacji (Więcej → O aplikacji → Bezpieczeństwo i prywatność) — po zmianie tych tekstów
w aplikacji warto je tu zaktualizować.

## Podgląd na żywo
```
cd safebudget-strona
pip install -r requirements.txt
python flask_app.py        # http://localhost:5000 — zmiany w szablonach i tłumaczeniach widać po odświeżeniu
```

## Wersja statyczna
```
python freeze.py           # → build/ (folder build/ nie trafia do repozytorium)
```

## Publikacja na GitHub Pages (automatyczna)
Workflow `.github/workflows/strona.yml` buduje i publikuje stronę po każdym pushu na gałąź `main`
(albo ręcznie: Actions → „Strona internetowa (GitHub Pages)” → Run workflow).

Jednorazowo w repozytorium na GitHubie:
1. **Settings → Pages → Build and deployment → Source: GitHub Actions**.
2. Repozytorium musi zostać **publiczne** — na darmowym koncie GitHub Pages nie publikuje z prywatnych.

### Własna domena (safebudget.eu)
1. U rejestratora domeny (Hostido) w strefie DNS:
   - `A` dla `safebudget.eu.` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `CNAME` dla `www` → `pfryc2020.github.io.`
   - `TXT` `_github-pages-challenge-pfryc2020` — weryfikacja domeny na koncie GitHub (nie usuwać)
2. **Settings → Pages → Custom domain**: `safebudget.eu`, zaznaczone **Enforce HTTPS**.
3. Adres strony w `sitemap.xml` i podglądzie linków to domyślnie `https://safebudget.eu`; zmienna
   `ADRES_STRONY` (Settings → Secrets and variables → Actions → Variables) może go zastąpić.

### Poczta w domenie (Interia Poczta PRO)
Strona działa na GitHub Pages, a poczta `…@safebudget.eu` w Interii. Strefę DNS prowadzi Hostido
(`ns1/ns2/ns3.hostido.net.pl`). Rekordy poczty:

| Typ | Nazwa | Wartość |
|---|---|---|
| `MX` | `@` | `10 mx.interia.pl.` |
| `TXT` (SPF) | `safebudget.eu.` | `v=spf1 include:interia.pl -all` |
| `TXT` (DMARC) | `_dmarc` | `v=DMARC1; p=quarantine; adkim=s; aspf=s;` |

- W panelu Hostido wartość MX wpisuj **z kropką na końcu** (`mx.interia.pl.`). Bez niej panel dokleja
  domenę i powstaje błędne `mx.interia.pl.safebudget.eu.`.
- Może być **tylko jeden** rekord SPF (`v=spf1 …`). Nowego nadawcę dopisuj do istniejącego rekordu.
- **Nie ustawiaj** rekordu `A` na adres Interii (`217.74.71.168`), choć panel Interii o to prosi.
  To rekord dla strony hostowanej w Interii i zastąpiłby rekordy GitHub Pages, przez co strona przestałaby działać.
- W Interii („Twój adres w sieci”) przy domenie włączony jest tylko przełącznik **Email**, a **WWW** zostaje wyłączony.
  Gdy przełącznik Email nie chciał się włączyć mimo poprawnego MX, pomogło usunięcie domeny i dodanie jej ponownie.
- Każde „Dodatkowe konto pocztowe” to osobna skrzynka z własnym logowaniem (adres w domenie + hasło),
  a alias dostarcza pocztę do głównej skrzynki.
- Sprawdzenie DNS: <https://dns.google/query?name=safebudget.eu&rr_type=MX> (podobnie `rr_type=TXT`, `NS`).

## Link do Google Play
W `flask_app.py` ustaw `GOOGLE_PLAY_URL = "https://play.google.com/store/apps/details?id=..."`.
Dopóki jest `None`, przyciski pokazują „Wkrótce w Google Play” (w każdym języku).

## Zrzuty ekranu, obraz w nagłówku i instrukcje
Zrzuty i instrukcje PDF pochodzą z prywatnego repozytorium aplikacji (`www/instrukcja/<język>/`,
robi je `node skrypty/zrzuty-instrukcji.js`). Po zmianie wyglądu aplikacji skopiuj je ponownie
(z katalogu, w którym leżą oba repozytoria):
```
for j in pl en de fr es it pt id zh hi bn ar; do
  cp budzet-domowy/www/instrukcja/$j/{budzet,transakcje,statystyki,trend,podglad,oplaty,plan,kopia,blokada}.webp safebudget-strona/static/img/zrzuty/$j/
  cp budzet-domowy/www/instrukcja/$j/instrukcja.pdf safebudget-strona/static/instrukcja/$j.pdf
done
cd safebudget-strona && pip install Pillow && python narzedzia/hero.py     # nowe obrazy do nagłówka
```
