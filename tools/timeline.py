"""The arc: when each project started, and how the total accumulated.

Creation dates come straight from the snapshot, so the shape of this chart is
the shape of the account rather than a story told after the fact. The flat
stretch in the middle is real and stays in.
"""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime

from PIL import Image, ImageDraw, ImageFilter

from common import (ASSETS, CREAM, GREY, INK, ORANGE_HI, add_glow, font,
                    projects, repos)
from themes import AREAS, LEARNING, SKIP, THEME, area_colour

W, H, F = 1600, 500, 2
CW, CH = W * F, H * F
L, R = int(CW * .052), int(CW * .058)
T, B = int(CH * .335), int(CH * .175)
PW, PH = CW - L - R, CH - T - B

MONTH = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
         "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def months_between(a: str, b: str) -> list[str]:
    y, m = int(a[:4]), int(a[5:7])
    out = []
    while f"{y:04d}-{m:02d}" <= b:
        out.append(f"{y:04d}-{m:02d}")
        m += 1
        if m == 13:
            m, y = 1, y + 1
    return out


def build() -> Image.Image:
    img = Image.new("RGB", (CW, CH), INK)
    d = ImageDraw.Draw(img)

    allr = [r for r in repos() if r["name"] not in SKIP]
    ps = projects()
    months = months_between(allr[0]["createdAt"][:7], allr[-1]["createdAt"][:7])
    span = max(1, len(months) - 1)

    def mx(mk: str) -> float:
        return L + PW * (months.index(mk) / span)

    per_month: dict[str, list[dict]] = defaultdict(list)
    for r in ps:
        per_month[r["createdAt"][:7]].append(r)
    for r in allr:
        if r["name"] in LEARNING:
            per_month[r["createdAt"][:7]].append(r)

    # ---- cumulative curve of substantive projects -------------------------
    running, cum = 0, []
    for mk in months:
        running += sum(1 for r in per_month.get(mk, []) if r["name"] not in LEARNING)
        cum.append(running)
    top = max(cum) or 1

    def cy(v: float) -> float:
        return T + PH - PH * (v / top) * 0.92

    pts = [(mx(mk), cy(v)) for mk, v in zip(months, cum)]

    # the filled area goes down first, so nothing drawn later is dimmed by it
    d.polygon(pts + [(pts[-1][0], T + PH), (pts[0][0], T + PH)], fill=(52, 27, 14))

    # ---- gridlines and axes ----------------------------------------------
    f_ax = font(int(12 * F))
    for v in range(0, top + 1, 7):
        y = cy(v)
        d.line([L, y, L + PW, y], fill=(52, 47, 43), width=int(1.2 * F))
        d.text((L - 26 * F, y - 8 * F), str(v), font=f_ax, fill=(132, 124, 116))
    d.line([L, T + PH, L + PW, T + PH], fill=(90, 82, 74), width=int(1.6 * F))
    d.line(pts, fill=ORANGE_HI, width=int(3.0 * F), joint="curve")

    for mk in months:
        x = mx(mk)
        first = mk.endswith("-01") or mk == months[0]
        d.line([x, T + PH, x, T + PH + (9 if first else 5) * F],
               fill=(112, 103, 94) if first else (72, 66, 60), width=int(1.4 * F))
        if int(mk[5:7]) % 3 == 1 or mk == months[0]:
            lab = f"{MONTH[int(mk[5:7]) - 1]} {mk[2:4]}"
            d.text((x - d.textlength(lab, font=f_ax) / 2, T + PH + 14 * F),
                   lab, font=f_ax, fill=(158, 149, 140))

    # ---- one dot per project, stacked in its month ------------------------
    step = PH / 8.2
    for mk, items in sorted(per_month.items()):
        x = mx(mk)
        items = sorted(items, key=lambda r: r["name"] in LEARNING)
        for i, r in enumerate(items):
            y = T + PH - step * (i + 0.7)
            if r["name"] in LEARNING:
                colour, rad = (84, 78, 72), 5.0 * F
            else:
                area_name, weight = THEME[r["name"]]
                colour, rad = area_colour(area_name), (5.0 + 2.5 * weight) * F
                if weight >= 3:
                    img = add_glow(img, x, y, rad * 2.6, colour, 0.42)
                    d = ImageDraw.Draw(img)
            d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=colour)

    # ---- heading ----------------------------------------------------------
    ds = sorted(datetime.fromisoformat(r["createdAt"].replace("Z", "+00:00"))
                for r in ps)
    cadence = round((ds[-1] - ds[0]).days / max(1, len(ds) - 1))
    recent = [x for x in ds if x.strftime("%Y-%m") >= "2026-03"]
    rmonths = len({x.strftime("%Y-%m") for x in recent})
    d.text((L, int(CH * .085)), f"One project every {cadence} days",
           font=font(int(30 * F), bold=True), fill=CREAM)
    d.text((L, int(CH * .175)),
           f"{len(ps)} substantive projects  ·  {len(recent)} of them in the last "
           f"{rmonths} months  ·  the line is the running total",
           font=font(int(14 * F)), fill=GREY)
    d.text((L, int(CH * .235)),
           "grey dots are the four repositories I learned on, kept public on purpose",
           font=font(int(12.5 * F)), fill=(104, 97, 90))

    # ---- legend -----------------------------------------------------------
    lx, ly = L, CH - int(CH * .058)
    f_lg = font(int(11.5 * F), bold=True)
    for area, colour, _ in AREAS:
        d.ellipse([lx, ly - 5 * F, lx + 10 * F, ly + 5 * F], fill=colour)
        d.text((lx + 16 * F, ly - 7 * F), area.upper(), font=f_lg, fill=colour)
        lx += int(d.textlength(area.upper(), font=f_lg)) + int(54 * F)

    return img.resize((W, H), Image.LANCZOS)


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    out = ASSETS / "timeline.png"
    build().save(out)
    print("wrote", out)
