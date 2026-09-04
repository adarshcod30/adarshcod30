"""Shared plumbing: load the repository snapshot, and find a real font.

`make refresh` rewrites data/repos.json from the GitHub API. Everything drawn
from it is therefore a fact about the account rather than something I typed
into a template - the same rule I hold my project READMEs to.
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "repos.json"
ASSETS = ROOT / "assets"

INK = (16, 15, 14)
INK2 = (30, 27, 25)
CREAM = (251, 250, 249)
ORANGE = (194, 65, 12)
ORANGE_HI = (232, 106, 45)
DIM = (58, 53, 49)
GREY = (150, 142, 134)

FONT_CANDIDATES_REGULAR = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/Library/Fonts/Arial.ttf",
]
FONT_CANDIDATES_BOLD = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
]


def font(size: int, bold: bool = False):
    for p in (FONT_CANDIDATES_BOLD if bold else FONT_CANDIDATES_REGULAR):
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


def repos() -> list[dict]:
    """Every public, non-fork repository I own or build under an organisation
    of mine, oldest first. Organisation repos carry their owner so the tables
    can show who they belong to."""
    raw = json.loads(DATA.read_text())["data"]["user"]
    out = [r for r in raw["repositories"]["nodes"] if not r.get("isFork")]
    for org in (raw.get("organizations") or {}).get("nodes", []):
        for r in org["repositories"]["nodes"]:
            if not r.get("isFork"):
                r = dict(r)
                r["org"] = org["login"]
                out.append(r)
    out.sort(key=lambda r: r["createdAt"])
    return out


def full_name(r: dict) -> str:
    """owner/name for an organisation repo, bare name for my own."""
    return f"{r['org']}/{r['name']}" if r.get("org") else r["name"]


def projects() -> list[dict]:
    """The substantive projects: everything except the four learning repos."""
    from themes import LEARNING, SKIP, THEME
    return [r for r in repos()
            if r["name"] not in LEARNING and r["name"] not in SKIP
            and r["name"] in THEME]


def add_glow(img, x, y, r, colour, strength=0.55):
    """Add light around a point. Additive, so it can only brighten - blending
    against an ink-filled layer dimmed everything already drawn."""
    layer = Image.new("RGB", img.size, (0, 0, 0))
    ImageDraw.Draw(layer).ellipse(
        [x - r, y - r, x + r, y + r],
        fill=tuple(int(c * strength) for c in colour))
    return ImageChops.add(img, layer.filter(ImageFilter.GaussianBlur(r * 0.45)))
