# Strona internetowa Safe Budget

Strona aplikacji pisana w Pythonie (Flask). Publikowana jako **wersja statyczna** (zwykłe pliki HTML)
na **GitHub Pages** — hosting za 0 zł, z własną domeną i HTTPS.

```
safebudget-strona/
├── flask_app.py          ← cała logika i treść (funkcje, zrzuty, bezpieczeństwo, FAQ, autor)
├── freeze.py             ← zamiana na pliki HTML → build/
├── requirements.txt
├── templates/            ← base.html, index.html, polityka.html, pobierz.html, 404.html, _przycisk_play.html
└── static/               ← css/style.css, img/ (ikona, grafika, zrzuty/*.webp), instrukcja-pl.pdf
```

Podstrony: `/` (strona główna), `/polityka-prywatnosci/` (adres do podania w Konsoli Google Play),
`/pobierz/` (krótki link do ulotek/QR → Google Play), `/404.html`, `/sitemap.xml`, `/robots.txt`.

## Podgląd na żywo
```
cd safebudget-strona
pip install -r requirements.txt
python flask_app.py        # http://localhost:5000 — zmiany w szablonach widać od razu
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
1. U rejestratora domeny dodaj rekordy DNS:
   - `A` dla `@` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `CNAME` dla `www` → `pfryc2020.github.io`
2. **Settings → Pages → Custom domain**: wpisz `safebudget.eu`, zapisz, a po weryfikacji zaznacz **Enforce HTTPS**.
3. **Settings → Secrets and variables → Actions → Variables → New variable**:
   `ADRES_STRONY` = `https://safebudget.eu` i uruchom workflow ponownie (adres trafia do sitemap.xml i podglądu linków).

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
Dopóki jest `None`, przyciski pokazują „Wkrótce w Google Play”.

## Zrzuty ekranu
Pochodzą z instrukcji w prywatnym repozytorium aplikacji (`www/instrukcja/pl/`, robi je `node skrypty/zrzuty-instrukcji.js`).
Po zmianie wyglądu aplikacji skopiuj je ponownie do `static/img/zrzuty/` (te same nazwy plików `.webp`),
a instrukcję PDF — do `static/instrukcja-pl.pdf`.
