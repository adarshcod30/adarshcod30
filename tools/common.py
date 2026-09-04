"""Shared plumbing: load the repository snapshot, and find a real font.

`make refresh` rewrites data/repos.json from the GitHub API. Everything drawn
from it is therefore a fact about the account rather than something I typed
into a template - the same rule I hold my project READMEs to.
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import ImageFont

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
    """Every public, non-fork repository, oldest first."""
    raw = json.loads(DATA.read_text())
    nodes = raw["data"]["user"]["repositories"]["nodes"]
    out = [r for r in nodes if not r.get("isFork")]
    out.sort(key=lambda r: r["createdAt"])
    return out


def projects() -> list[dict]:
    """The substantive projects: everything except the four learning repos."""
    from themes import LEARNING, THEME
    return [r for r in repos()
            if r["name"] not in LEARNING and r["name"] in THEME]
