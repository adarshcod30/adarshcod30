"""The banner: every project a node, clustered by area, drawn from the
snapshot in data/repos.json rather than a hand-written list.
"""
from __future__ import annotations

import math
import random

from PIL import Image, ImageDraw

from common import ASSETS, CREAM, DIM, GREY, INK, INK2, ORANGE_HI, font, projects
from themes import AREAS, THEME, short

W, H, F = 1600, 540, 2
CW, CH = W * F, H * F

# where each area sits, and how tightly its nodes pack
LAYOUT = {
    "public-interest AI":  ((0.470, 0.335), 1.00),
    "trust & verification": ((0.700, 0.335), 0.92),
    "agentic systems":     ((0.886, 0.335), 0.78),
    "quant & pipelines":   ((0.560, 0.760), 0.72),
    "foundations":         ((0.790, 0.760), 0.62),
}


def build() -> Image.Image:
    rng = random.Random(11)
    img = Image.new("RGB", (CW, CH), INK)
    d = ImageDraw.Draw(img)

    # a soft warm wash so the field is not a flat black slab
    for i in range(220, 0, -1):
        t = i / 220
        col = tuple(int(INK[j] + (INK2[j] - INK[j]) * (1 - t) * 0.9) for j in range(3))
        r = CW * 0.62 * t
        d.ellipse([CW * .66 - r, CH * .42 - r, CW * .66 + r, CH * .42 + r], fill=col)

    by_area: dict[str, list[dict]] = {a: [] for a, _, _ in AREAS}
    for r in projects():
        by_area[THEME[r["name"]][0]].append(r)

    placed, anchors = [], []
    for area, colour, _desc in AREAS:
        members = by_area[area]
        if not members:
            continue
        (fx, fy), scale = LAYOUT[area]
        ax, ay = fx * CW, fy * CH
        k = len(members)
        spread = CW * (0.026 + 0.0062 * k) * scale
        anchors.append((ax, ay, area, colour, spread))

        nodes = []
        for i, r in enumerate(members):
            weight = THEME[r["name"]][1]
            a = 2 * math.pi * i / k + rng.uniform(-0.22, 0.22)
            rr = spread * rng.uniform(0.80, 1.06)
            nodes.append((ax + rr * math.cos(a), ay + rr * math.sin(a) * 0.78,
                          weight, colour, short(r["name"])))
        placed.extend(nodes)

        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                if rng.random() < 0.62:
                    d.line([nodes[i][0], nodes[i][1], nodes[j][0], nodes[j][1]],
                           fill=DIM, width=int(1.6 * F))

    for i in range(len(anchors)):
        for j in range(i + 1, len(anchors)):
            a, b = anchors[i], anchors[j]
            if rng.random() < 0.8:
                d.line([a[0], a[1], b[0], b[1]], fill=(38, 35, 32), width=int(1.3 * F))

    for (x, y, w, colour, _name) in placed:
        r = (5.5 + 3.6 * w) * F
        if w >= 3:
            for gr, al in ((r * 3.2, 22), (r * 2.0, 40)):
                layer = Image.new("RGB", (CW, CH), INK)
                ImageDraw.Draw(layer).ellipse([x - gr, y - gr, x + gr, y + gr],
                                              fill=colour)
                img = Image.blend(img, layer, al / 255)
                d = ImageDraw.Draw(img)
        d.ellipse([x - r, y - r, x + r, y + r], fill=colour)

    # name only the heaviest node in each area, so it stays a picture
    f_node, seen = font(int(11.5 * F)), set()
    for (x, y, w, colour, name) in sorted(placed, key=lambda t: -t[2]):
        if w >= 3 and colour not in seen:
            seen.add(colour)
            d.text((x + 14 * F, y - 6 * F), name, font=f_node, fill=(206, 198, 190))

    f_cl = font(int(11.5 * F), bold=True)
    for (ax, ay, label, colour, spread) in anchors:
        tw = d.textlength(label.upper(), font=f_cl)
        d.text((ax - tw / 2, ay + spread * 0.80 + 16 * F), label.upper(),
               font=f_cl, fill=colour)

    n = len(projects())
    x0, y0 = int(CW * 0.055), int(CH * 0.30)
    d.text((x0, y0), "Adarsh Dwivedi", font=font(int(46 * F), bold=True), fill=CREAM)
    f_tag = font(int(16.5 * F))
    d.text((x0, y0 + int(60 * F)), "Measured, explainable ML", font=f_tag, fill=ORANGE_HI)
    d.text((x0, y0 + int(83 * F)), "for problems that matter in India.",
           font=f_tag, fill=ORANGE_HI)
    d.line([x0, y0 + int(112 * F), x0 + int(300 * F), y0 + int(112 * F)],
           fill=(70, 64, 58), width=int(1.5 * F))
    d.text((x0, y0 + int(120 * F)),
           f"{n} projects  ·  every number reproducible  ·  every limit stated",
           font=font(int(13 * F)), fill=GREY)

    return img.resize((W, H), Image.LANCZOS)


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    out = ASSETS / "banner.png"
    build().save(out)
    print("wrote", out)
