# Jak samodzielnie zmienić treść strony

Wszystko robisz w przeglądarce, na github.com, bez instalowania niczego.
Po zapisaniu zmiany strona **sama się przebuduje i opublikuje na safebudget.eu w 1–2 minuty**.

## Edycja krok po kroku

1. Otwórz https://github.com/pfryc2020/safebudget-strona
2. Wejdź w plik, który chcesz zmienić (np. `tlumaczenia` → `pl.json`).
3. Kliknij ikonę ołówka ✏️ („Edit this file”) w prawym górnym rogu pliku.
4. Popraw tekst. Szukanie w pliku: `Ctrl+F`.
5. Kliknij zielony przycisk **Commit changes…** → wpisz krótki opis (np. „Nowy opis w hero”)
   → zostaw zaznaczone „Commit directly to the main branch” → **Commit changes**.
6. Zakładka **Actions**: przy Twojej zmianie pojawi się kółko 🟡, potem ✅ — strona jest już zaktualizowana
   (odśwież ją w przeglądarce, ewentualnie `Ctrl+F5`).

Na telefonie: w aplikacji GitHub lub w przeglądarce (tryb „Wersja na komputer”) działa tak samo.

## Gdzie co jest

| Co chcesz zmienić | Plik |
|---|---|
| Teksty strony po polsku | `tlumaczenia/pl.json` |
| Teksty w innych językach | `tlumaczenia/en.json`, `de.json`, `fr.json`, `es.json`, `it.json`, `pt.json`, `id.json`, `zh.json`, `hi.json`, `bn.json`, `ar.json` |
| Link do Google Play | `flask_app.py` → `GOOGLE_PLAY_URL` |
| Imię autora, e-mail | `flask_app.py` → `AUTOR` |
| Liczba dni darmowej wersji próbnej | `flask_app.py` → `DNI_PROBY` |
| Data polityki prywatności | `flask_app.py` → `DATA_POLITYKI` |
| Zrzuty ekranu | `static/img/zrzuty/<język>/<nazwa>.webp` (podmień plik o tej samej nazwie: „Add file” → „Upload files”) |
| Instrukcja PDF | `static/instrukcja/<język>.pdf` |

### Sekcje w pliku `pl.json`

| Klucz w pliku | Miejsce na stronie |
|---|---|
| `meta` | tytuł karty przeglądarki i opis w Google / przy udostępnianiu linku |
| `menu` | górne menu |
| `hero` | pierwszy ekran (duży nagłówek, opis, „znaczki”) |
| `o_aplikacji` | sekcja „O aplikacji” — funkcje i 3 kroki |
| `zrzuty` | podpisy zrzutów ekranu |
| `bezpieczenstwo` | „Bezpieczeństwo i prywatność” (teksty jak w aplikacji) |
| `pobierz` | sekcja „Pobierz” i cennik (wersja darmowa / Pro) |
| `faq` | „Pytania” — pytania i odpowiedzi |
| `autor` | opis autora |
| `stopka` | stopka strony |
| `polityka` | strona „Polityka prywatności” |
| `blad404` | strona „Nie znaleziono” |

Przykład — zmiana nagłówka:

```json
"tytul_1": "Twój budżet.",
"tytul_2": "Tylko w Twoim telefonie.",
```

zmieniasz tylko tekst **po dwukropku, w cudzysłowie**:

```json
"tytul_1": "Twoje pieniądze.",
"tytul_2": "Pod pełną kontrolą.",
```

## Zasady (żeby nic nie zepsuć)

- Zmieniaj **tylko tekst po prawej stronie** dwukropka. Nazw po lewej (`"tytul_1":`) nie ruszaj.
- Każdy tekst jest w prostych cudzysłowach `"…"`. Wewnątrz tekstu używaj polskich „ ” zamiast `"`.
- Między wierszami jest przecinek; **po ostatnim elemencie** w nawiasie `}` lub `]` przecinka nie ma.
- `{n}` zostaw — w to miejsce strona wstawia liczbę dni wersji próbnej.
- Jeśli w tekście są znaczniki typu `<b>…</b>` (pogrubienie) — zostaw je; działają tylko tam, gdzie już są.
- Nowy element listy (np. pytanie w FAQ) dodajesz kopiując cały blok `{ "pytanie": "…", "odpowiedz": "…" }`
  razem z przecinkiem.

### Teksty w innych językach

Strona pilnuje, żeby **wszystkie 12 plików miało te same elementy**. Jeśli:

- **zmieniasz tylko treść** istniejącego tekstu po polsku — możesz zmienić tylko `pl.json`,
  pozostałe języki zostaną po staremu (warto je potem poprawić, np. prosząc Claude o tłumaczenie);
- **dodajesz lub usuwasz element** (np. nowe pytanie w FAQ) — trzeba to zrobić we wszystkich 12 plikach,
  inaczej publikacja się nie uda.

## Gdy coś pójdzie nie tak

Nie ma ryzyka zepsucia działającej strony: **jeśli w zmianie jest błąd, publikacja się zatrzyma, a na
safebudget.eu zostanie poprzednia wersja.**

1. W zakładce **Actions** zobaczysz ❌ przy swojej zmianie.
2. Kliknij ją → „Budowanie strony” → krok „Flask → pliki HTML”. Będzie tam opis po polsku, np.:

   ```
   BŁĄD w pliku tlumaczenia/pl.json, wiersz 38, znak 5: Expecting ',' delimiter
   ```

   albo `Niekompletne tłumaczenia: en: brak faq.lista[7]…` (brakuje elementu w innym języku).
3. Popraw plik (ołówek ✏️) i zapisz ponownie.

Cofnięcie zmiany: zakładka **Commits** → otwórz swoją zmianę → podejrzyj poprzednią wersję tekstu
i wpisz ją z powrotem (albo poproś Claude: „cofnij ostatnią zmianę na stronie”).
