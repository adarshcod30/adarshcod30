"""The arc: when each project started, coloured by area.

Reads creation dates straight from the snapshot, so the shape of the chart is
the shape of the account rather than a story told after the fact.
"""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime

from PIL import Image, ImageDraw

from common import ASSETS, CREAM, GREY, INK, INK2, ORANGE_HI, font, projects, repos
from themes import AREAS, LEARNING, THEME, area_colour, short

W, H, F = 1600, 460, 2
CW, CH = W * F, H * F
PAD_L, PAD_R, PAD_T, PAD_B = int(CW * .050), int(CW * .105), int(CH * .30), int(CH * .22)


def month_key(iso: str) -> str:
    return iso[:7]


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
    for i in range(200, 0, -1):
        t = i / 200
        col = tuple(int(INK[j] + (INK2[j] - INK[j]) * (1 - t) * .85) for j in range(3))
        r = CW * .70 * t
        d.ellipse([CW * .5 - r, CH * .55 - r, CW * .5 + r, CH * .55 + r], fill=col)

    allr = repos()
    first = month_key(allr[0]["createdAt"])
    last = month_key(allr[-1]["createdAt"])
    months = months_between(first, last)
    span = max(1, len(months) - 1)
    plot_w = CW - PAD_L - PAD_R
    plot_h = CH - PAD_T - PAD_B

    def mx(mk: str) -> float:
        return PAD_L + plot_w * (months.index(mk) / span)

    # baseline
    d.line([PAD_L, PAD_T + plot_h, PAD_L + plot_w, PAD_T + plot_h],
           fill=(64, 58, 53), width=int(1.6 * F))

    # year ticks
    f_ax = font(int(12 * F))
    seen_year = set()
    for mk in months:
        if mk[:4] not in seen_year:
            seen_year.add(mk[:4])
            x = mx(mk)
            d.line([x, PAD_T + plot_h, x, PAD_T + plot_h + 9 * F],
                   fill=(84, 77, 70), width=int(1.6 * F))
            d.text((x + 6 * F, PAD_T + plot_h + 13 * F), mk[:4], font=f_ax, fill=GREY)

    # stack the projects in each month
    per_month: dict[str, list[dict]] = defaultdict(list)
    for r in projects():
        per_month[month_key(r["createdAt"])].append(r)
    learning = [r for r in allr if r["name"] in LEARNING]
    for r in learning:
        per_month[month_key(r["createdAt"])].append(r)

    step = plot_h / 7.0
    f_lab = font(int(10.5 * F))
    for mk, items in sorted(per_month.items()):
        x = mx(mk)
        for i, r in enumerate(items):
            y = PAD_T + plot_h - step * (i + 0.85)
            is_learn = r["name"] in LEARNING
            if is_learn:
                colour, rad = (86, 80, 74), 5.0 * F
            else:
                area, weight = THEME[r["name"]]
                colour, rad = area_colour(area), (5.0 + 2.6 * weight) * F
            d.line([x, PAD_T + plot_h, x, y], fill=(46, 42, 38), width=int(1.3 * F))
            if not is_learn and weight >= 3:
                for gr, al in ((rad * 3.0, 26), (rad * 1.9, 44)):
                    layer = Image.new("RGB", (CW, CH), INK)
                    ImageDraw.Draw(layer).ellipse(
                        [x - gr, y - gr, x + gr, y + gr], fill=colour)
                    img = Image.blend(img, layer, al / 255)
                    d = ImageDraw.Draw(img)
            d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=colour)
            if not is_learn and weight >= 3:
                lab = short(r["name"])
                lw = d.textlength(lab, font=f_lab)
                if x + rad + 8 * F + lw > CW - PAD_R * 0.25:
                    d.text((x - rad - 8 * F - lw, y - 6 * F), lab,
                           font=f_lab, fill=(200, 192, 184))
                else:
                    d.text((x + rad + 6 * F, y - 6 * F), lab,
                           font=f_lab, fill=(200, 192, 184))

    # heading
    x0 = PAD_L
    ps = projects()
    n = len(ps)
    ds = sorted(datetime.fromisoformat(r["createdAt"].replace("Z", "+00:00"))
                for r in ps)
    cadence = round((ds[-1] - ds[0]).days / max(1, n - 1))
    recent_from = "2026-03"
    recent = [x for x in ds if x.strftime("%Y-%m") >= recent_from]
    recent_months = len({x.strftime("%Y-%m") for x in recent})
    d.text((x0, int(CH * .085)),
           f"From a first repository to one every {cadence} days",
           font=font(int(27 * F), bold=True), fill=CREAM)
    d.text((x0, int(CH * .175)),
           f"{n} substantive projects  ·  {len(recent)} of them in the last "
           f"{recent_months} months  ·  grey marks the four I learned on",
           font=font(int(13.5 * F)), fill=GREY)

    # legend
    lx = PAD_L
    ly = CH - int(CH * .075)
    f_lg = font(int(11.5 * F), bold=True)
    for area, colour, _ in AREAS:
        d.ellipse([lx, ly - 5 * F, lx + 10 * F, ly + 5 * F], fill=colour)
        d.text((lx + 16 * F, ly - 7 * F), area.upper(), font=f_lg, fill=colour)
        lx += int(d.textlength(area.upper(), font=f_lg)) + int(52 * F)

    return img.resize((W, H), Image.LANCZOS)


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    out = ASSETS / "timeline.png"
    build().save(out)
    print("wrote", out)
