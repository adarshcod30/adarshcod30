"""The banner: every project placed in a radial system, drawn from the
snapshot in data/repos.json rather than a hand-written list.

Each of the five areas owns an angular sector. A project sits on a ring whose
radius comes from its weight, so the work I would show first sits nearest the
core. Nothing here is positioned by hand.
"""
from __future__ import annotations

import math
import random

from PIL import Image, ImageDraw, ImageFilter

from common import (ASSETS, CREAM, GREY, INK, ORANGE_HI, add_glow, font,
                    projects)
from themes import AREAS, THEME, short

W, H, F = 1600, 560, 2
CW, CH = W * F, H * F
CX, CY = int(CW * 0.700), int(CH * 0.505)
R_CORE = int(CH * 0.055)
R_IN, R_OUT = int(CH * 0.150), int(CH * 0.360)


def build() -> Image.Image:
    rng = random.Random(19)
    img = Image.new("RGB", (CW, CH), INK)

    # a wide, soft pool of warmth behind the system
    img = add_glow(img, CX, CY, int(R_OUT * 1.35), (74, 46, 28), 0.55)
    d = ImageDraw.Draw(img)

    # concentric guides
    for k in range(1, 5):
        r = R_IN + (R_OUT - R_IN) * k / 4
        d.ellipse([CX - r, CY - r, CX + r, CY + r], outline=(56, 51, 46),
                  width=int(1.3 * F))

    by_area = {a: [] for a, _, _ in AREAS}
    for r in projects():
        by_area[THEME[r["name"]][0]].append(r)

    # every area gets an angular sector, sized by how much sits in it
    total = sum(len(v) for v in by_area.values())
    gap = math.radians(7)
    start = math.radians(-102)
    sectors = []
    for area, colour, _ in AREAS:
        n = len(by_area[area])
        if not n:
            continue
        span = 2 * math.pi * (n / total) - gap
        sectors.append((area, colour, start, span, by_area[area]))
        start += span + gap

    # sector dividers
    for _a, _c, s0, span, _m in sectors:
        for ang in (s0 - gap / 2, s0 + span + gap / 2):
            d.line([CX + R_IN * 0.82 * math.cos(ang), CY + R_IN * 0.82 * math.sin(ang),
                    CX + R_OUT * 1.10 * math.cos(ang), CY + R_OUT * 1.10 * math.sin(ang)],
                   fill=(40, 36, 33), width=int(1.2 * F))

    # nodes, and the spoke each one hangs from
    placed = []
    for area, colour, s0, span, members in sectors:
        members = sorted(members, key=lambda r: -THEME[r["name"]][1])
        for i, r in enumerate(members):
            w = THEME[r["name"]][1]
            frac = (i + 0.5) / len(members)
            ang = s0 + span * frac
            # heavier work sits closer to the core, with a little stagger so
            # neighbouring nodes never sit on one perfect arc
            rad = R_OUT - (R_OUT - R_IN) * ((w - 1) / 2.0) * 0.42
            rad += (0.10 if i % 2 else -0.10) * (R_OUT - R_IN)
            rad += rng.uniform(-1, 1) * (R_OUT - R_IN) * 0.02
            x, y = CX + rad * math.cos(ang), CY + rad * math.sin(ang)
            d.line([CX + R_CORE * 1.25 * math.cos(ang),
                    CY + R_CORE * 1.25 * math.sin(ang), x, y],
                   fill=(52, 47, 43), width=int(1.25 * F))
            placed.append((x, y, w, colour, short(r["name"]), ang))

    for (x, y, w, colour, _n, _a) in placed:
        rr = (5.0 + 3.4 * w) * F
        if w >= 3:
            img = add_glow(img, x, y, rr * 2.8, colour, 0.40)
            d = ImageDraw.Draw(img)
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=colour)

    # the core
    img = add_glow(img, CX, CY, R_CORE * 2.4, (198, 88, 32), 0.55)
    d = ImageDraw.Draw(img)
    d.ellipse([CX - R_CORE, CY - R_CORE, CX + R_CORE, CY + R_CORE], fill=(26, 22, 20))
    d.ellipse([CX - R_CORE, CY - R_CORE, CX + R_CORE, CY + R_CORE],
              outline=ORANGE_HI, width=int(2.0 * F))
    rc = R_CORE * 0.34
    d.ellipse([CX - rc, CY - rc, CX + rc, CY + rc], fill=ORANGE_HI)
    # area captions, outside the outermost ring
    f_cl = font(int(12 * F), bold=True)
    for area, colour, s0, span, members in sectors:
        ang = s0 + span / 2
        r = R_OUT * 1.20
        tx, ty = CX + r * math.cos(ang), CY + r * math.sin(ang)
        label = area.upper()
        tw = d.textlength(label, font=f_cl)
        if math.cos(ang) < -0.15:
            tx -= tw
        elif abs(math.cos(ang)) <= 0.15:
            tx -= tw / 2
        d.text((tx, ty - 6 * F), label, font=f_cl, fill=colour)
        d.text((tx, ty + 9 * F), f"{len(members)} projects", font=font(int(10.5 * F)),
               fill=(112, 105, 98))

    # the name block
    x0, y0 = int(CW * 0.052), int(CH * 0.255)
    d.text((x0, y0), "Adarsh Dwivedi", font=font(int(48 * F), bold=True), fill=CREAM)
    f_tag = font(int(17 * F))
    d.text((x0, y0 + int(64 * F)), "Measured, explainable ML", font=f_tag, fill=ORANGE_HI)
    d.text((x0, y0 + int(88 * F)), "for problems that matter in India.",
           font=f_tag, fill=ORANGE_HI)
    d.line([x0, y0 + int(124 * F), x0 + int(330 * F), y0 + int(124 * F)],
           fill=(74, 67, 60), width=int(1.5 * F))

    n = len(projects())
    n_org = len({r["org"] for r in projects() if r.get("org")})
    stats = [(str(n), "projects"), (str(len(sectors)), "areas"),
             (str(n_org), "organisations")]
    sx = x0
    f_num, f_cap = font(int(23 * F), bold=True), font(int(11 * F))
    for val, cap in stats:
        d.text((sx, y0 + int(140 * F)), val, font=f_num, fill=CREAM)
        d.text((sx, y0 + int(170 * F)), cap.upper(), font=f_cap, fill=(126, 118, 110))
        sx += int(112 * F)
    d.text((x0, y0 + int(202 * F)),
           "every number reproducible  ·  every limit stated",
           font=font(int(12.5 * F)), fill=GREY)

    return img.resize((W, H), Image.LANCZOS)


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    out = ASSETS / "banner.png"
    build().save(out)
    print("wrote", out)
