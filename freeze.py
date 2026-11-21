"""
Zamienia stronę Flask na zwykłe pliki (HTML, CSS, obrazy) w folderze build/.
Takie pliki można wystawić na GitHub Pages, Cloudflare Pages albo dowolnym hostingu — bez Pythona na serwerze.

    python freeze.py                                  → build/
    ADRES_STRONY=https://safebudget.eu python freeze.py

Zmienna DOMENA (np. safebudget.eu) tworzy plik CNAME (potrzebny tylko przy publikacji z gałęzi, nie przez Actions).
Budowanie przerywa się, gdy w którymś języku brakuje tekstu albo gdy jakiś odnośnik prowadzi donikąd.
"""
import os
import sys
from pathlib import Path
from urllib.parse import urlsplit

from flask_frozen import Freezer

from flask_app import ADRES_STRONY, JEZYKI, JEZYKI_WARUNKOW, T, app, sprawdz_tlumaczenia

KATALOG = Path(__file__).parent / "build"

app.config.update(
    FREEZER_DESTINATION=str(KATALOG),
    FREEZER_BASE_URL=ADRES_STRONY + "/",
    FREEZER_RELATIVE_URLS=False,       # adresy od korzenia domeny: /de/, /polityka-prywatnosci/ (bez „index.html”)
    FREEZER_REMOVE_EXTRA_FILES=True,
    FREEZER_IGNORE_404_NOT_FOUND=False,
)
freezer = Freezer(app)


@freezer.register_generator
def strona_glowna():
    for j in JEZYKI:
        yield {"jezyk": j}


@freezer.register_generator
def polityka():
    for j in JEZYKI:
        yield {"jezyk": j}


@freezer.register_generator
def warunki():
    for j in JEZYKI_WARUNKOW:
        yield {"jezyk": j}


@freezer.register_generator
def strona_404():
    yield {}


if __name__ == "__main__":
    bledy = sprawdz_tlumaczenia(T)
    if bledy:
        sys.exit("Niekompletne tłumaczenia:\n  " + "\n  ".join(bledy))
    adresy = freezer.freeze()
    (KATALOG / ".nojekyll").write_text("")          # GitHub Pages: pliki podaje bez przetwarzania
    domena = os.environ.get("DOMENA", "").strip() or ""
    if domena:
        (KATALOG / "CNAME").write_text(domena + "\n")
    print(f"Gotowe: {len(adresy)} adresów → {KATALOG} (adres strony: {urlsplit(ADRES_STRONY).netloc})")
