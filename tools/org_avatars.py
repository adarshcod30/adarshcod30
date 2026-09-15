"""The three avatars: mine and the two organisations'.

Each is a node composition on deep navy - same construction, different colour,
different idea - so they read as a set without being the same picture. They
are drawn full-bleed because GitHub crops an avatar to a circle, so a disc on
a white square only wastes the corners.

  adarshcod30   - one dense cluster inside a sparse population: the thing my
                  work keeps looking for.
  VaidyaMitra   - a cluster whose inner nodes are hollow: every identifier is
                  masked before the model ever sees it.
  B-TechProject - a request crossing a gate: in AGENTIQ nothing reaches the
                  network except through a permission-checked tool layer.
"""
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

S, F = 460, 4
N = S * F
OUT = Path(__file__).resolve().parent.parent / "assets"

# Same cool palette as the banner and the timeline.
INK = (10, 14, 26)
ACCENT = (29, 118, 219)       # mine: the dense cluster
ACCENT_HI = (64, 169, 255)
TEAL = (20, 165, 170)         # VaidyaMitra: clinical data
TEAL_HI = (45, 212, 218)
BLUE = (79, 110, 240)         # B-TechProject: the gate
BLUE_HI = (129, 149, 255)
MUTED = (96, 112, 142)        # the ordinary population
DIM = (34, 46, 72)


def circle(d, cx, cy, r, **kw):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], **kw)


def add_glow(img, x, y, r, colour, strength=0.5):
    layer = Image.new("RGB", img.size, (0, 0, 0))
    ImageDraw.Draw(layer).ellipse(
        [x - r, y - r, x + r, y + r],
        fill=tuple(int(c * strength) for c in colour))
    return ImageChops.add(img, layer.filter(ImageFilter.GaussianBlur(r * 0.45)))


def ring(cx, cy, r, k, phase=0.0):
    return [(cx + r * math.cos(phase + 2 * math.pi * i / k),
             cy + r * math.sin(phase + 2 * math.pi * i / k)) for i in range(k)]


def me() -> Image.Image:
    """A dense cluster hiding in an ordinary population - the shape almost
    every project here is looking for. Read small, it is one bright knot."""
    rng = random.Random(7)
    img = Image.new("RGB", (N, N), INK)
    cx = cy = N / 2

    # light pooled behind the cluster, so the knot carries the eye at 40px
    img = add_glow(img, cx + N * 0.045, cy - N * 0.030, N * 0.30, ACCENT, 0.42)
    d = ImageDraw.Draw(img)

    inner = N * 0.425
    pts, tries = [], 0
    while len(pts) < 21 and tries < 6000:
        tries += 1
        a = rng.uniform(0, 2 * math.pi)
        r = inner * math.sqrt(rng.uniform(0.05, 1.0))
        p = (cx + r * math.cos(a), cy + r * math.sin(a))
        if all(math.hypot(p[0] - q[0], p[1] - q[1]) > N * 0.100 for q in pts):
            pts.append(p)

    clus = ring(cx + N * 0.045, cy - N * 0.030, N * 0.105, 6, phase=0.4)

    # the sparse population: faint, and only loosely joined
    for i, p in enumerate(pts):
        for q in pts[i + 1:]:
            if math.hypot(p[0] - q[0], p[1] - q[1]) < N * 0.155 and rng.random() < 0.45:
                d.line([p[0], p[1], q[0], q[1]], fill=DIM, width=int(2.4 * F))
    # the cluster: every pair joined, which is what makes it findable
    for i in range(len(clus)):
        for j in range(i + 1, len(clus)):
            d.line([clus[i][0], clus[i][1], clus[j][0], clus[j][1]],
                   fill=ACCENT, width=int(4.6 * F))

    for p in pts:
        circle(d, p[0], p[1], 7.5 * F, fill=MUTED)
    for p in clus:
        img = add_glow(img, p[0], p[1], 20 * F, ACCENT_HI, 0.30)
        d = ImageDraw.Draw(img)
        circle(d, p[0], p[1], 14.0 * F, fill=ACCENT_HI)

    return img.resize((S, S), Image.LANCZOS)


def vaidyamitra() -> Image.Image:
    """Data around a masked core."""
    img = Image.new("RGB", (N, N), INK)
    d = ImageDraw.Draw(img)
    cx = cy = N / 2

    outer = ring(cx, cy, N * 0.255, 8, phase=-math.pi / 2)
    inner = ring(cx, cy, N * 0.108, 4, phase=math.pi / 4)

    for p in outer:
        d.line([cx, cy, p[0], p[1]], fill=DIM, width=int(2.4 * F))
    for i in range(len(outer)):
        d.line([outer[i][0], outer[i][1],
                outer[(i + 1) % len(outer)][0], outer[(i + 1) % len(outer)][1]],
               fill=DIM, width=int(2.2 * F))

    for p in outer:
        img = add_glow(img, p[0], p[1], 13 * F, TEAL, 0.30)
        d = ImageDraw.Draw(img)
        circle(d, p[0], p[1], 11.5 * F, fill=TEAL_HI)

    # the masked core: present in the graph, withheld from the model
    for p in inner:
        circle(d, p[0], p[1], 15 * F, fill=INK)
        circle(d, p[0], p[1], 15 * F, outline=(122, 140, 172), width=int(3.0 * F))
    circle(d, cx, cy, 20 * F, fill=INK)
    circle(d, cx, cy, 20 * F, outline=(158, 176, 206), width=int(3.4 * F))

    return img.resize((S, S), Image.LANCZOS)


def btechproject() -> Image.Image:
    """A request that only crosses through the gate."""
    img = Image.new("RGB", (N, N), INK)
    d = ImageDraw.Draw(img)
    cx = cy = N / 2

    lx, rx = cx - N * 0.235, cx + N * 0.200
    d.line([lx, cy, rx, cy], fill=DIM, width=int(3.0 * F))

    # the gate
    gx = cx - N * 0.010
    img = add_glow(img, gx, cy, 62 * F, BLUE, 0.26)
    d = ImageDraw.Draw(img)
    d.line([gx, cy - N * 0.175, gx, cy + N * 0.175], fill=BLUE_HI, width=int(7.0 * F))
    for sy in (-1, 1):
        d.line([gx - 17 * F, cy + sy * N * 0.175, gx + 17 * F, cy + sy * N * 0.175],
               fill=BLUE_HI, width=int(6.0 * F))

    # request in, verified out
    circle(d, lx, cy, 19 * F, fill=(132, 150, 182))
    for p in ring(rx - N * 0.005, cy, N * 0.098, 3, phase=-math.pi / 2):
        img = add_glow(img, p[0], p[1], 15 * F, BLUE, 0.32)
        d = ImageDraw.Draw(img)
        circle(d, p[0], p[1], 12.5 * F, fill=BLUE_HI)

    # blocked attempt: it does not get past the gate
    for sy in (-1, 1):
        y = cy + sy * N * 0.125
        d.line([lx + 6 * F, y, gx - 26 * F, y], fill=(104, 52, 68), width=int(3.0 * F))
        x = gx - 22 * F
        for dx, dy in ((-1, -1), (-1, 1)):
            d.line([x, y, x + dx * 12 * F, y + dy * 12 * F],
                   fill=(226, 90, 110), width=int(3.4 * F))

    return img.resize((S, S), Image.LANCZOS)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name, im in (("avatar", me()),
                     ("org-vaidyamitra", vaidyamitra()),
                     ("org-btechproject", btechproject())):
        p = OUT / f"{name}.png"
        im.save(p)
        print("wrote", p)
