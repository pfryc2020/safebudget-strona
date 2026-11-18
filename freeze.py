"""
Zamienia stronę Flask na zwykłe pliki (HTML, CSS, obrazy) w folderze build/.
Takie pliki można wystawić na GitHub Pages, Cloudflare Pages albo dowolnym hostingu — bez Pythona na serwerze.

    python freeze.py                       → build/
    ADRES_STRONY=https://safebudget.pl python freeze.py

Zmienna DOMENA (np. safebudget.pl) tworzy plik CNAME — tak GitHub Pages poznaje własną domenę.
"""
import os
from pathlib import Path

from flask_frozen import Freezer

from flask_app import app

KATALOG = Path(__file__).parent / "build"

app.config.update(
    FREEZER_DESTINATION=str(KATALOG),
    FREEZER_RELATIVE_URLS=True,       # linki względne: strona działa także pod adresem z podfolderem
    FREEZER_REMOVE_EXTRA_FILES=True,
    FREEZER_IGNORE_404_NOT_FOUND=False,
)
freezer = Freezer(app)


@freezer.register_generator
def strona_404():
    yield {}


if __name__ == "__main__":
    adresy = freezer.freeze()
    (KATALOG / ".nojekyll").write_text("")          # GitHub Pages: pliki podaje bez przetwarzania
    domena = os.environ.get("DOMENA", "").strip()
    if domena:
        (KATALOG / "CNAME").write_text(domena + "\n")
    print(f"Gotowe: {len(adresy)} adresów → {KATALOG}")
