"""
Obraz w nagłówku strony: dwa przechylone telefony ze zrzutami aplikacji — dla każdego języka.

Obrót robi się tu, w wysokiej rozdzielczości (4×), a potem obraz zmniejsza się starannie (Lanczos)
do rozmiarów 1× i 2×. Dzięki temu przechylone zrzuty są ostre — przeglądarka obracająca obraz
w CSS zmniejsza go zgrubnie i tekst wygląda na rozpikselowany.

    pip install Pillow
    python narzedzia/hero.py            → static/img/hero/<język>-1x.webp, <język>-2x.webp

Uruchom ponownie po podmianie zrzutów w static/img/zrzuty/<język>/.
"""
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

KATALOG = Path(__file__).resolve().parent.parent
ZRZUTY = KATALOG / "static" / "img" / "zrzuty"
WYJSCIE = KATALOG / "static" / "img" / "hero"

S = 4                       # nadpróbkowanie: rysujemy 4× większe niż rozmiar 1×
PLOTNO = (500, 600)         # rozmiar obrazu w pikselach CSS (1×)
TEL_SZER = 250              # szerokość telefonu (z ramką) w pikselach CSS
RAMKA = 9                   # grubość ramki telefonu
PROMIEN_TEL, PROMIEN_EKRANU = 34, 26
# (zrzut, lewy górny róg przed obrotem, kąt w stopniach — dodatni = przeciwnie do wskazówek zegara, krycie)
TELEFONY = [
    ("statystyki", (222, 86), -6, 0.9),     # z tyłu
    ("budzet", (34, 30), 4, 1.0),           # z przodu
]


def zaokraglony(rozmiar, promien, kolor):
    maska = Image.new("L", rozmiar, 0)
    ImageDraw.Draw(maska).rounded_rectangle((0, 0, rozmiar[0] - 1, rozmiar[1] - 1), promien, fill=255)
    obraz = Image.new("RGBA", rozmiar, kolor)
    obraz.putalpha(maska)
    return obraz


def telefon(zrzut: Path):
    """Telefon (ramka + zrzut) w skali S, jeszcze bez obrotu i cienia."""
    ekran_szer = (TEL_SZER - 2 * RAMKA) * S
    ekran = Image.open(zrzut).convert("RGB")
    ekran_wys = round(ekran_szer * ekran.height / ekran.width)
    ekran = ekran.resize((ekran_szer, ekran_wys), Image.LANCZOS)

    szer, wys = ekran_szer + 2 * RAMKA * S, ekran_wys + 2 * RAMKA * S
    tel = zaokraglony((szer, wys), PROMIEN_TEL * S, (10, 18, 32, 255))
    # cienka jaśniejsza krawędź ramki (jak inset 0 0 0 2px #2b3a55)
    krawedz = zaokraglony((szer, wys), PROMIEN_TEL * S, (43, 58, 85, 255))
    wnetrze = zaokraglony((szer - 4 * S, wys - 4 * S), (PROMIEN_TEL - 2) * S, (10, 18, 32, 255))
    krawedz.alpha_composite(wnetrze, (2 * S, 2 * S))
    tel = krawedz

    maska = Image.new("L", ekran.size, 0)
    ImageDraw.Draw(maska).rounded_rectangle((0, 0, ekran.width - 1, ekran.height - 1), PROMIEN_EKRANU * S, fill=255)
    tel.paste(ekran, (RAMKA * S, RAMKA * S), maska)
    return tel


def cien(rozmiar_tel, kat, krycie):
    """Miękki cień pod telefonem (jak box-shadow 0 24px 48px rgba(0,0,0,.45)), liczony w 1× i powiększony."""
    w, h = (round(v / S) for v in rozmiar_tel)
    m = 80
    sylwetka = Image.new("L", (w + 2 * m, h + 2 * m), 0)
    ImageDraw.Draw(sylwetka).rounded_rectangle((m, m, m + w, m + h), PROMIEN_TEL, fill=round(255 * 0.45 * krycie))
    sylwetka = sylwetka.rotate(kat, resample=Image.BICUBIC, expand=True).filter(ImageFilter.GaussianBlur(24))
    warstwa = Image.new("RGBA", sylwetka.size, (0, 0, 0, 0))
    warstwa.putalpha(sylwetka)
    return warstwa.resize((sylwetka.width * S, sylwetka.height * S), Image.BICUBIC)


def wygaszanie_krawedzi(rozmiar, szerokosc):
    """Maska, która łagodnie schodzi do zera przy brzegach obrazu — cień nie urywa się na krawędzi."""
    maska = Image.new("L", rozmiar, 255)
    rys = ImageDraw.Draw(maska)
    for i in range(szerokosc):
        rys.rectangle((i, i, rozmiar[0] - 1 - i, rozmiar[1] - 1 - i), outline=round(255 * i / szerokosc))
    return maska


def hero(jezyk: str):
    rozmiar = (PLOTNO[0] * S, PLOTNO[1] * S)
    plotno = Image.new("RGBA", rozmiar, (0, 0, 0, 0))
    wygaszanie = wygaszanie_krawedzi(rozmiar, 48 * S)
    for nazwa, (x, y), kat, krycie in TELEFONY:
        tel = telefon(ZRZUTY / jezyk / f"{nazwa}.webp")
        srodek = (x * S + tel.width / 2, y * S + tel.height / 2)

        c = cien(tel.size, kat, krycie)
        warstwa = Image.new("RGBA", rozmiar, (0, 0, 0, 0))
        warstwa.alpha_composite(c, (round(srodek[0] - c.width / 2), round(srodek[1] + 24 * S - c.height / 2)))
        warstwa.putalpha(ImageChops.multiply(warstwa.getchannel("A"), wygaszanie))
        plotno.alpha_composite(warstwa)

        obr = tel.rotate(kat, resample=Image.BICUBIC, expand=True)
        if krycie < 1:
            obr.putalpha(obr.getchannel("A").point(lambda a: round(a * krycie)))
        plotno.alpha_composite(obr, (round(srodek[0] - obr.width / 2), round(srodek[1] - obr.height / 2)))

    WYJSCIE.mkdir(parents=True, exist_ok=True)
    for skala in (1, 2):
        rozmiar = (PLOTNO[0] * skala, PLOTNO[1] * skala)
        # zmniejszanie w przestrzeni z przemnożoną alfą — bez ciemnych obwódek na krawędziach
        plotno_pm = plotno.convert("RGBa").resize(rozmiar, Image.LANCZOS).convert("RGBA")
        plotno_pm.save(WYJSCIE / f"{jezyk}-{skala}x.webp", "WEBP", quality=90, method=6)


if __name__ == "__main__":
    jezyki = sys.argv[1:] or sorted(p.name for p in ZRZUTY.iterdir() if p.is_dir())
    for j in jezyki:
        hero(j)
        print("hero:", j)
