"""The three avatars: mine and the two organisations'.

Each is a node composition on warm ink - same construction, different colour,
different idea - so they read as a set without being the same picture.

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

INK = (18, 17, 16)
TEAL = (34, 158, 132)
TEAL_HI = (58, 196, 164)
BLUE = (58, 138, 196)
BLUE_HI = (96, 176, 226)
ORANGE_HI = (232, 106, 45)
MUTED = (120, 112, 104)
DIM = (66, 61, 56)


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
    every project here is looking for."""
    rng = random.Random(7)
    img = Image.new("RGB", (N, N), (250, 250, 249))
    d = ImageDraw.Draw(img)
    cx = cy = N / 2
    circle(d, cx, cy, N * 0.455, fill=INK)

    inner = N * 0.40
    pts, tries = [], 0
    while len(pts) < 19 and tries < 4000:
        tries += 1
        a = rng.uniform(0, 2 * math.pi)
        r = inner * math.sqrt(rng.uniform(0.05, 1.0))
        p = (cx + r * math.cos(a), cy + r * math.sin(a))
        if all(math.hypot(p[0] - q[0], p[1] - q[1]) > N * 0.105 for q in pts):
            pts.append(p)

    clus = ring(cx + N * 0.045, cy - N * 0.030, N * 0.105, 6, phase=0.4)

    for i, p in enumerate(pts):
        for q in pts[i + 1:]:
            if math.hypot(p[0] - q[0], p[1] - q[1]) < N * 0.155 and rng.random() < 0.45:
                d.line([p[0], p[1], q[0], q[1]], fill=(70, 64, 58), width=int(2.4 * F))
    for i in range(len(clus)):
        for j in range(i + 1, len(clus)):
            d.line([clus[i][0], clus[i][1], clus[j][0], clus[j][1]],
                   fill=(194, 65, 12), width=int(4.6 * F))

    for p in pts:
        circle(d, p[0], p[1], 7.5 * F, fill=(120, 112, 104))
    for p in clus:
        circle(d, p[0], p[1], 14.0 * F, fill=ORANGE_HI)

    return img.resize((S, S), Image.LANCZOS)


def vaidyamitra() -> Image.Image:
    """Data around a masked core."""
    img = Image.new("RGB", (N, N), (250, 250, 249))
    d = ImageDraw.Draw(img)
    cx = cy = N / 2
    circle(d, cx, cy, N * 0.455, fill=INK)

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
        circle(d, p[0], p[1], 15 * F, outline=(150, 142, 134), width=int(3.0 * F))
    circle(d, cx, cy, 20 * F, fill=INK)
    circle(d, cx, cy, 20 * F, outline=(178, 170, 162), width=int(3.4 * F))

    return img.resize((S, S), Image.LANCZOS)


def btechproject() -> Image.Image:
    """A request that only crosses through the gate."""
    img = Image.new("RGB", (N, N), (250, 250, 249))
    d = ImageDraw.Draw(img)
    cx = cy = N / 2
    circle(d, cx, cy, N * 0.455, fill=INK)

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
    circle(d, lx, cy, 19 * F, fill=(160, 152, 144))
    for p in ring(rx - N * 0.005, cy, N * 0.098, 3, phase=-math.pi / 2):
        img = add_glow(img, p[0], p[1], 15 * F, BLUE, 0.32)
        d = ImageDraw.Draw(img)
        circle(d, p[0], p[1], 12.5 * F, fill=BLUE_HI)

    # blocked attempt: it does not get past the gate
    for sy in (-1, 1):
        y = cy + sy * N * 0.125
        d.line([lx + 6 * F, y, gx - 26 * F, y], fill=(96, 64, 60), width=int(3.0 * F))
        x = gx - 22 * F
        for dx, dy in ((-1, -1), (-1, 1)):
            d.line([x, y, x + dx * 12 * F, y + dy * 12 * F],
                   fill=(176, 88, 76), width=int(3.4 * F))

    return img.resize((S, S), Image.LANCZOS)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name, im in (("avatar", me()),
                     ("org-vaidyamitra", vaidyamitra()),
                     ("org-btechproject", btechproject())):
        p = OUT / f"{name}.png"
        im.save(p)
        print("wrote", p)
