#!/usr/bin/env python3
"""Render social cards and app icons from the site's own type and vector art.

Run with Python 3 and Pillow. No network, browser, or generated stock art is used.
The Manrope fonts are licensed in site/assets/OFL-Manrope.txt.
"""

from functools import lru_cache
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "site" / "assets"
OUTPUT = ROOT / "site" / "brand"
SCALE = 3
PAPER = "#f4f3ee"
INK = "#222a27"
MUTED = "#59615a"
ACCENT = "#d95535"
LIME = "#d8e594"


@lru_cache(maxsize=64)
def font(size, weight, extended=False):
    filename = "manrope-4.woff2" if extended else "manrope-5.woff2"
    result = ImageFont.truetype(str(ASSETS / filename), size * SCALE)
    result.set_variation_by_axes([weight])
    return result


def text(draw, value, xy, size, weight=500, color=INK, tracking=0):
    """Use the bundled Latin and Latin Extended subsets on one baseline."""
    x, y = (coordinate * SCALE for coordinate in xy)
    for i, character in enumerate(value):
        extended = ord(character) > 255 and character not in "ı·’—–"
        selected = font(size, weight, extended)
        draw.text((x, y), character, font=selected, fill=color, anchor="ls")
        advance = selected.getlength(character)
        if i + 1 < len(value):
            next_character = value[i + 1]
            next_extended = ord(next_character) > 255 and next_character not in "ı·’—–"
            if next_extended == extended:
                advance = selected.getlength(character + next_character) - selected.getlength(next_character)
        x += advance + tracking * SCALE
    return x / SCALE


def line(draw, points, color, width=1):
    draw.line([(x * SCALE, y * SCALE) for x, y in points], fill=color, width=width * SCALE)


def polygon(draw, points, color):
    draw.polygon([(round(x * SCALE), round(y * SCALE)) for x, y in points], fill=color)


def mark(image, xy, size):
    """The same M and red detail used by the site's existing favicon.svg."""
    x, y = xy
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((x * SCALE, y * SCALE, (x + size) * SCALE, (y + size) * SCALE),
                           radius=6 * size / 48 * SCALE, fill=INK)
    points = [(7, 37), (7, 11), (14, 11), (24, 25), (34, 11), (41, 11),
              (41, 37), (34, 37), (34, 24), (24, 38), (14, 24), (14, 37)]
    polygon(draw, [(x + px * size / 48, y + py * size / 48) for px, py in points], PAPER)
    polygon(draw, [(x + px * size / 48, y + py * size / 48)
                   for px, py in [(34, 33), (41, 33), (41, 40), (34, 40)]], ACCENT)


def path_points(data):
    """Read the straight-line M/L/H/V/Z paths in our structure.svg."""
    tokens = re.findall(r"[MmLlHhVvZz]|-?(?:\d*\.\d+|\d+)", data)
    result = []
    current = (0, 0)
    command = None
    i = 0
    while i < len(tokens):
        if tokens[i].isalpha():
            command = tokens[i]
            i += 1
            if command in "Zz":
                break
        if command in "MmLl":
            x, y = float(tokens[i]), float(tokens[i + 1])
            i += 2
            if command.islower():
                x += current[0]
                y += current[1]
            current = (x, y)
            command = "l" if command == "m" else "L" if command == "M" else command
        elif command in "Hh":
            x = float(tokens[i])
            i += 1
            current = (x + current[0] if command == "h" else x, current[1])
        elif command in "Vv":
            y = float(tokens[i])
            i += 1
            current = (current[0], y + current[1] if command == "v" else y)
        else:
            raise ValueError("structure.svg contains an unsupported path command")
        result.append(current)
    return result


def illustration(image):
    """Reuse the existing architectural illustration, keeping the brand intact."""
    draw = ImageDraw.Draw(image)
    panel_left = 752
    draw.rectangle((panel_left * SCALE, 0, 1200 * SCALE, 630 * SCALE), fill=INK)
    for x in range(panel_left + 28, 1200, 38):
        line(draw, [(x, 0), (x, 630)], "#2b332e")
    for y in range(10, 630, 38):
        line(draw, [(panel_left, y), (1200, y)], "#2b332e")
    for radius in (178, 208):
        draw.ellipse(((976 - radius) * SCALE, (306 - radius) * SCALE,
                      (976 + radius) * SCALE, (306 + radius) * SCALE),
                     outline="#3d493e", width=SCALE)

    svg = ET.parse(ASSETS / "structure.svg").getroot()
    group = svg.find("{http://www.w3.org/2000/svg}g[@transform]")
    if group is None:
        raise ValueError("The brand illustration's drawing group is missing")
    for element in group:
        points = path_points(element.attrib["d"])
        translated = [(755 + (x + 30) * .71, 102 + y * .71) for x, y in points]
        fill = element.attrib["fill"]
        if fill == "url(#face)":
            fill = "#cbd797"
        if element.attrib.get("fill-opacity"):
            fill = "#19211c"
        polygon(draw, translated, fill)

    for x, y in ((780, 112), (1169, 112), (780, 488), (1169, 488)):
        line(draw, [(x - 5, y), (x + 5, y)], "#79886a")
        line(draw, [(x, y - 5), (x, y + 5)], "#79886a")


def social_card(language):
    image = Image.new("RGB", (1200 * SCALE, 630 * SCALE), PAPER)
    draw = ImageDraw.Draw(image)
    illustration(image)
    mark(image, (64, 54), 46)
    text(draw, "Mevlana Yalçın", (126, 87), 31, 650)
    if language == "tr":
        text(draw, "YAPAY ZEKÂ DANIŞMANLIĞI VE ÜRÜN GELİŞTİRME", (64, 139), 12, 650, MUTED, .9)
        text(draw, "Yapay zekâ.", (60, 272), 76, 600)
        text(draw, "Gerçek işler için.", (62, 350), 63, 600)
        text(draw, "Claude ile geliştiriyoruz.", (64, 415), 25, 500, MUTED)
        text(draw, "YANKI / CLAUDE İLE", (784, 67), 13, 650, LIME, .8)
        text(draw, "Fikirden çalışan ürüne.", (784, 553), 21, 550, PAPER)
        text(draw, "Yankı'yı keşfedin", (784, 580), 14, 450, "#a4b199")
    else:
        text(draw, "AI CONSULTING & PRODUCT DEVELOPMENT", (64, 139), 12, 650, MUTED, .9)
        text(draw, "Practical AI.", (60, 272), 76, 600)
        text(draw, "Built with Claude.", (62, 350), 60, 600)
        text(draw, "AI consulting · Makers of Yankı", (64, 415), 25, 500, MUTED)
        text(draw, "YANKI / BUILT WITH CLAUDE", (784, 67), 12, 650, LIME, .6)
        text(draw, "From idea to working product.", (784, 553), 19, 550, PAPER)
        text(draw, "Discover Yankı", (784, 580), 14, 450, "#a4b199")
    line(draw, [(64, 493), (696, 493)], "#d5d8cd")
    text(draw, "mevlanayalcin.com.tr", (64, 548), 20, 650)
    text(draw, "info@mevlanayalcin.com.tr", (64, 579), 16, 450, MUTED)
    image = image.resize((1200, 630), Image.Resampling.LANCZOS)
    target = OUTPUT / ("og-tr.png" if language == "tr" else "og.png")
    image.save(target, optimize=True)


def icons():
    image = Image.new("RGB", (512 * SCALE, 512 * SCALE), INK)
    mark(image, (0, 0), 512)
    image = image.resize((512, 512), Image.Resampling.LANCZOS)
    image.save(OUTPUT / "icon-512.png", optimize=True)
    for name, size in (("apple-touch-icon.png", 180), ("favicon-32.png", 32)):
        image.resize((size, size), Image.Resampling.LANCZOS).save(OUTPUT / name, optimize=True)
    image.save(OUTPUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    social_card("en")
    social_card("tr")
    icons()
    for path in sorted(OUTPUT.iterdir()):
        if path.is_file():
            with Image.open(path) as image:
                print(f"{path.relative_to(ROOT)}: {image.width}×{image.height}, {path.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
