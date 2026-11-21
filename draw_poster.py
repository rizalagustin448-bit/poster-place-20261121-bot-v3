#!/usr/bin/env python3
"""Draw the AURMARA v3 travel poster (1024x1024) with Pillow.

v3 vs v2: the place name is no longer a header band — it is a giant
sun-cast shadow across the terrace floor, like rank-1 SUVENNE. The scene
is much denser: a full whitewashed cliff town, café couples in the
foreground, sailboats, bougainvillea, grain — warm, grounded, lived-in.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(img, box, top, bottom):
    x0, y0, x1, y1 = box
    h = max(1, y1 - y0)
    d = ImageDraw.Draw(img)
    for y in range(y0, y1):
        d.line([(x0, y), (x1, y)], fill=lerp(top, bottom, (y - y0) / h))


def main():
    random.seed(41)
    img = Image.new("RGB", (W, H), (247, 232, 200))
    d = ImageDraw.Draw(img, "RGBA")

    # ---- sky (0..430) ----
    vgrad(img, (14, 14, 1010, 430), (44, 92, 156), (252, 196, 108))
    # sun glow + sun
    cx, cy = 360, 392
    for r, a in ((220, 40), (160, 60), (110, 80)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 226, 150, a))
    d.ellipse([cx - 58, cy - 58, cx + 58, cy + 58], fill=(255, 240, 190, 255))
    d.ellipse([cx - 46, cy - 46, cx + 46, cy + 46], fill=(255, 248, 214, 255))
    # birds
    for bx, by, s in ((700, 120, 12), (760, 95, 9), (820, 140, 10), (620, 80, 8)):
        d.arc([bx - s, by - s // 2, bx, by + s // 2], 200, 340, fill=(40, 60, 90, 220), width=3)
        d.arc([bx, by - s // 2, bx + s, by + s // 2], 200, 340, fill=(40, 60, 90, 220), width=3)
    # distant headland
    d.polygon([(560, 430), (640, 372), (720, 388), (800, 366), (860, 430)],
              fill=(96, 128, 138, 255))
    d.polygon([(640, 372), (720, 388), (800, 366), (860, 430), (560, 430)],
              fill=(120, 148, 140, 255))

    # ---- sea (430..650) ----
    vgrad(img, (14, 430, 1010, 650), (30, 110, 122), (62, 158, 158))
    # sun path: widening light dashes
    for i, y in enumerate(range(440, 650, 14)):
        wdt = 26 + i * 7
        d.rectangle([cx - wdt, y, cx + wdt, y + 5], fill=(255, 232, 160, 150 - i * 5))
    # sailboats
    def boat(x, y, s):
        d.polygon([(x, y), (x + 34 * s, y), (x + 17 * s, y + 12 * s)], fill=(74, 40, 28, 255))
        d.polygon([(x + 4 * s, y), (x + 4 * s, y - 52 * s), (x + 30 * s, y - 4 * s)],
                  fill=(250, 244, 226, 255))
        d.polygon([(x + 2 * s, y), (x + 2 * s, y - 38 * s), (x - 18 * s, y - 4 * s)],
                  fill=(240, 228, 200, 255))
        d.line([x + 4 * s, y - 54 * s, x + 4 * s, y], fill=(60, 40, 30, 255), width=2)
    boat(180, 520, 1.0)
    boat(480, 585, 0.7)
    boat(90, 600, 0.55)

    # ---- cliff + town (right, 300..650) ----
    d.polygon([(660, 650), (700, 420), (760, 330), (880, 300), (1010, 320),
               (1010, 650)], fill=(138, 90, 58, 255))
    d.polygon([(660, 650), (700, 420), (760, 330), (880, 300), (1010, 320),
               (1010, 380), (900, 360), (780, 390), (710, 470), (680, 650)],
              fill=(160, 108, 70, 255))
    # houses: tiers of whitewashed houses with terracotta roofs
    houses = [
        (700, 430, 92, 66), (800, 408, 84, 60), (892, 392, 96, 64),
        (716, 500, 100, 70), (826, 482, 92, 66), (922, 470, 80, 60),
        (690, 576, 110, 70), (812, 560, 104, 70), (924, 548, 78, 62),
    ]
    for hx, hy, hw, hh in houses:
        d.rectangle([hx, hy, hx + hw, hy + hh], fill=(250, 242, 224, 255))
        d.polygon([(hx - 4, hy), (hx + hw + 4, hy), (hx + hw - 12, hy - 16),
                   (hx + 12, hy - 16)], fill=(196, 96, 52, 255))
        for wx in range(hx + 12, hx + hw - 8, 26):
            for wy in (hy + 14, hy + 40):
                lit = random.random() < 0.45
                d.rectangle([wx, wy, wx + 12, wy + 18],
                            fill=(255, 214, 130, 255) if lit else (52, 74, 96, 255))
        d.rectangle([hx + hw // 2 - 8, hy + hh - 22, hx + hw // 2 + 8, hy + hh],
                    fill=(90, 60, 40, 255))
    # balconies + awnings
    for ax, ay in ((716, 540), (826, 522), (924, 588)):
        d.rectangle([ax, ay, ax + 46, ay + 5], fill=(120, 70, 40, 255))
        d.polygon([(ax, ay), (ax + 46, ay), (ax + 40, ay + 16), (ax + 6, ay + 16)],
                  fill=(232, 120, 60, 255))
    # cypress trees
    for tx, ty, th in ((690, 420, 46), (884, 372, 52), (985, 400, 44), (760, 470, 40)):
        d.ellipse([tx - 9, ty - th, tx + 9, ty + 6], fill=(28, 92, 52, 255))
        d.rectangle([tx - 2, ty, tx + 2, ty + 8], fill=(90, 60, 40, 255))
    # bougainvillea clusters on town
    for bx, by in ((800, 470), (910, 452), (700, 560), (980, 520)):
        for _ in range(26):
            ox, oy = random.gauss(0, 13), random.gauss(0, 9)
            d.ellipse([bx + ox - 4, by + oy - 4, bx + ox + 4, by + oy + 4],
                      fill=(214, 44, 110, 255))
        for _ in range(12):
            ox, oy = random.gauss(0, 15), random.gauss(0, 11)
            d.ellipse([bx + ox - 3, by + oy - 3, bx + ox + 3, by + oy + 3],
                      fill=(52, 110, 60, 255))

    # ---- grand staircase (centre, terrace -> sea) ----
    d.polygon([(452, 470), (572, 470), (636, 650), (388, 650)], fill=(232, 200, 150, 255))
    for i in range(10):
        t0 = i / 10
        y = 470 + t0 * 180
        x0 = 452 - t0 * 64
        x1 = 572 + t0 * 64
        d.line([(x0, y), (x1, y)], fill=(150, 100, 60, 255), width=3)
        d.line([(x0, y + 3), (x1, y + 3)], fill=(255, 240, 205, 160), width=2)
    # stair lamps
    for lx, ly in ((430, 500), (594, 500), (414, 580), (610, 580)):
        d.rectangle([lx - 3, ly, lx + 3, ly + 26], fill=(60, 45, 30, 255))
        d.ellipse([lx - 8, ly - 12, lx + 8, ly + 2], fill=(255, 220, 130, 255))

    # ---- terrace / plaza (650..1010) ----
    vgrad(img, (14, 650, 1010, 1010), (238, 200, 143), (214, 164, 104))
    # paving arcs radiating from stairs base
    for r in (120, 210, 300, 390):
        d.arc([512 - r, 650 - r * 0.55, 512 + r, 650 + r * 0.55], 0, 180,
              fill=(170, 120, 70, 140), width=4)
    # balustrade along terrace top edge
    d.rectangle([14, 648, 1010, 660], fill=(250, 238, 210, 255))
    for bx in range(30, 1000, 44):
        d.rectangle([bx, 626, bx + 12, 650], fill=(245, 230, 198, 255))
        d.ellipse([bx - 2, 618, bx + 14, 632], fill=(250, 238, 210, 255))
    # terracotta pots with bougainvillea at terrace corners
    for px, py in ((70, 930), (950, 930)):
        d.polygon([(px - 34, py - 44), (px + 34, py - 44), (px + 26, py + 34),
                   (px - 26, py + 34)], fill=(178, 84, 44, 255))
        for _ in range(30):
            ox, oy = random.gauss(0, 26), random.gauss(-52, 14)
            d.ellipse([px + ox - 5, py + oy - 5, px + ox + 5, py + oy + 5],
                      fill=(214, 44, 110, 255))
        for _ in range(14):
            ox, oy = random.gauss(0, 28), random.gauss(-50, 16)
            d.ellipse([px + ox - 4, py + oy - 4, px + ox + 4, py + oy + 4],
                      fill=(52, 110, 60, 255))

    # ---- the name as a sun-cast shadow across the plaza ----
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    big = font(SERIF, 138)
    ld.text((512, 812), "AURMARA", font=big, anchor="mm",
            fill=(28, 28, 70, 155))
    layer = layer.rotate(-11, center=(512, 812), resample=Image.BICUBIC)
    img.paste(layer, (0, 0), layer)
    d = ImageDraw.Draw(img, "RGBA")

    # ---- café couples in the foreground ----
    def person(x, y, s, shirt, skin=(232, 190, 150, 255), hat=None, dress=False):
        # chair
        d.arc([x - 26 * s, y + 18 * s, x + 26 * s, y + 66 * s], 180, 360,
              fill=(120, 84, 48, 255), width=4)
        d.line([x - 24 * s, y + 44 * s, x - 24 * s, y + 78 * s], fill=(120, 84, 48, 255), width=4)
        d.line([x + 24 * s, y + 44 * s, x + 24 * s, y + 78 * s], fill=(120, 84, 48, 255), width=4)
        # body
        if dress:
            d.polygon([(x - 20 * s, y + 76 * s), (x + 20 * s, y + 76 * s),
                       (x + 11 * s, y + 6 * s), (x - 11 * s, y + 6 * s)], fill=shirt)
        else:
            d.rounded_rectangle([x - 17 * s, y + 4 * s, x + 17 * s, y + 52 * s],
                                radius=8 * s, fill=shirt)
        # head
        d.ellipse([x - 11 * s, y - 22 * s, x + 11 * s, y], fill=skin)
        if hat:
            d.ellipse([x - 18 * s, y - 20 * s, x + 18 * s, y - 12 * s], fill=hat)
            d.rectangle([x - 9 * s, y - 34 * s, x + 9 * s, y - 16 * s], fill=hat)
    def table(x, y, s):
        d.ellipse([x - 52 * s, y - 12 * s, x + 52 * s, y + 12 * s], fill=(252, 246, 232, 255))
        d.ellipse([x - 52 * s, y - 12 * s, x + 52 * s, y + 2 * s], fill=(255, 252, 240, 255))
        d.rectangle([x - 4 * s, y + 8 * s, x + 4 * s, y + 52 * s], fill=(90, 64, 40, 255))
        d.ellipse([x - 20 * s, y + 48 * s, x + 20 * s, y + 58 * s], fill=(90, 64, 40, 255))
        # glasses
        d.rectangle([x - 30 * s, y - 26 * s, x - 22 * s, y - 14 * s], fill=(255, 220, 130, 230))
        d.rectangle([x + 24 * s, y - 26 * s, x + 32 * s, y - 14 * s], fill=(255, 220, 130, 230))
    # left table: man with hat + woman in red
    table(180, 880, 1.0)
    person(120, 830, 1.0, (74, 110, 160, 255), hat=(214, 178, 110, 255))
    person(240, 826, 1.0, (196, 52, 68, 255), dress=True)
    # right table: woman in yellow + man in white
    table(840, 890, 0.95)
    person(790, 840, 0.95, (240, 190, 60, 255), dress=True)
    person(895, 844, 0.95, (248, 244, 232, 255), hat=(214, 178, 110, 255))

    # ---- bougainvillea draping top-left ----
    for _ in range(90):
        ox, oy = random.gauss(40, 42), random.gauss(60, 46)
        if 0 <= ox < 260 and 0 <= oy < 220:
            d.ellipse([ox - 6, oy - 6, ox + 6, oy + 6], fill=(214, 44, 110, 255))
    for _ in range(46):
        ox, oy = random.gauss(40, 46), random.gauss(60, 50)
        if 0 <= ox < 260 and 0 <= oy < 220:
            d.ellipse([ox - 5, oy - 5, ox + 5, oy + 5], fill=(46, 100, 56, 255))

    # ---- subtitle on the terrace edge ----
    sub = "T H E   H A R B O U R   O F   G O L D E N   S T A I R S"
    fsub = font(SERIF_R, 30)
    d.text((512, 985), sub, font=fsub, anchor="mm", fill=(74, 48, 28, 255))

    # ---- grain + frame ----
    grain = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grain)
    for _ in range(9000):
        x, y = random.randint(0, W - 1), random.randint(0, H - 1)
        v = random.randint(0, 255)
        gd.point((x, y), fill=(v, v, v, 10))
    img.paste(grain, (0, 0), grain)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([6, 6, 1017, 1017], outline=(247, 232, 200, 255), width=12)
    d.rectangle([20, 20, 1003, 1003], outline=(120, 84, 48, 120), width=2)

    img.save("poster.png", optimize=True)
    print("saved poster.png", img.size)


if __name__ == "__main__":
    main()
