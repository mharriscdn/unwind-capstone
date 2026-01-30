"""Sensation awareness decision tree (Mirror Mode).

Phenomenological vocabulary to increase perceptual resolution.
Aligned to Mirror_Mode_REVISED.docx (domain list + refinements).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class Domain:
    key: str
    label: str
    refinements: Tuple[str, ...]


DOMAINS: Tuple[Domain, ...] = (
    Domain("pressure", "Pressure / Force", (
        "Tight",
        "Compressed",
        "Expanding",
        "Contracting",
        "Squeezing",
        "Pressing outward",
        "Pulling inward",
        "Pulsing pressure",
    )),
    Domain("texture", "Texture", (
        "Smooth",
        "Rough",
        "Sharp",
        "Dull",
        "Grainy",
        "Sticky",
        "Slippery",
        "Prickly",
        "Fibrous",
        "Thick",
        "Thin",
        "Muddy",
        "Clear",
    )),
    Domain("movement", "Movement", (
        "Still",
        "Trembling",
        "Vibrating",
        "Swirling",
        "Rising",
        "Sinking",
        "Flickering",
        "Spreading",
        "Contracting",
        "Jerky",
        "Flowing",
    )),
    Domain("temperature", "Temperature", (
        "Warm",
        "Cool",
        "Hot",
        "Cold",
        "Fluctuating",
        "Neutral",
        "Localized warmth",
        "Radiating heat",
    )),
    Domain("density", "Density / Weight", (
        "Heavy",
        "Light",
        "Thick",
        "Thin",
        "Dense",
        "Hollow",
        "Solid",
        "Airy",
        "Weighted",
        "Pressurized",
    )),
    Domain("energy", "Vibration / Energy", (
        "Buzzing",
        "Humming",
        "Tingling",
        "Electric",
        "Static",
        "Fizzing",
        "Pulsing",
        "Quiet energy",
        "Diffuse energy",
    )),
    Domain("shape", "Shape / Boundary", (
        "Tight ball",
        "Band",
        "Knot",
        "Cloud",
        "Sheet",
        "Line",
        "Block",
        "Ring",
        "Undefined shape",
        "No clear edge",
    )),
    Domain("location", "Location / Spread", (
        "Localized",
        "Central",
        "Peripheral",
        "Spreading outward",
        "Moving location",
        "Fixed spot",
        "Diffuse",
        "Whole-body",
        "Front / back / sides",
    )),
    Domain("intensity", "Intensity", (
        "Faint",
        "Moderate",
        "Strong",
        "Surging",
        "Peaking",
        "Diminishing",
        "Steady",
        "Fluctuating",
    )),
    Domain("neutral", "Neutral / Unclear", (
        "Hard to describe",
        "Vague",
        "Blank",
        "Quiet",
        "Numb-adjacent",
        "Indistinct",
        "Nothing specific",
    )),
)

# --- Formatting helpers (CLI) ---

def format_domain_options() -> str:
    lines = []
    for i, d in enumerate(DOMAINS, start=1):
        lines.append(f"{i}) {d.label}")
    return "\n".join(lines)

def format_refinement_options(domain_key: str) -> str:
    d = _get_domain(domain_key)
    lines = []
    for i, r in enumerate(d.refinements, start=1):
        lines.append(f"{i}) {r}")
    return "\n".join(lines)

# --- Parsing helpers ---

def parse_domain_choice(user_text: str) -> Optional[str]:
    """Return domain_key or None."""
    t = user_text.strip().lower()
    # number choice
    if t.isdigit():
        n = int(t)
        if 1 <= n <= len(DOMAINS):
            return DOMAINS[n-1].key
        return None
    # label match
    for d in DOMAINS:
        if t == d.label.lower():
            return d.key
    # allow partial label match (e.g. 'intensity')
    for d in DOMAINS:
        if t in d.label.lower():
            return d.key
    return None

def parse_refinement_choice(domain_key: str, user_text: str) -> Optional[str]:
    """Return refinement label (exact) or None."""
    d = _get_domain(domain_key)
    t = user_text.strip()
    tl = t.lower()
    if tl == "skip":
        return None
    if tl.isdigit():
        n = int(tl)
        if 1 <= n <= len(d.refinements):
            return d.refinements[n-1]
        return None
    for r in d.refinements:
        if tl == r.lower():
            return r
    # allow partial
    for r in d.refinements:
        if tl in r.lower():
            return r
    return None

def infer_domain_from_free_text(user_text: str) -> Optional[str]:
    """Very light heuristic: map free text to a domain if obvious."""
    t = user_text.lower()
    keywords = {
        "pressure": ["pressure", "tight", "squeeze", "squeezing", "compress", "compressed", "clench", "bracing"],
        "texture": ["rough", "smooth", "sharp", "dull", "grainy", "sticky", "slippery", "prickly", "fibrous", "muddy"],
        "movement": ["move", "moving", "spreading", "rising", "sinking", "swirl", "swirling", "tremble", "vibrate", "vibrating", "flow"],
        "temperature": ["warm", "cool", "hot", "cold", "heat"],
        "density": ["heavy", "light", "dense", "hollow", "solid", "airy", "weighted", "pressurized"],
        "energy": ["buzz", "buzzing", "hum", "humming", "tingle", "tingling", "electric", "static", "fizz", "fizzing"],
        "shape": ["ball", "band", "knot", "cloud", "sheet", "line", "block", "ring", "edge", "boundary"],
        "location": ["where", "left", "right", "center", "central", "peripheral", "spread", "spreading", "whole-body", "front", "back", "sides"],
        "intensity": ["intense", "intensity", "strong", "faint", "moderate", "surging", "peaking", "diminishing", "steady", "fluctuating"],
        "neutral": ["unclear", "vague", "blank", "quiet", "numb", "nothing"],
    }
    for k, words in keywords.items():
        for w in words:
            if w in t:
                return k
    return None

def get_domain_name(domain_key: str) -> str:
    return _get_domain(domain_key).label

def get_refinement_name(domain_key: str, refinement_label: str) -> str:
    # refinement_label already exact label
    return refinement_label

def _get_domain(domain_key: str) -> Domain:
    for d in DOMAINS:
        if d.key == domain_key:
            return d
    raise KeyError(domain_key)


def domain_menu() -> str:
    """Return the full domain menu prompt (Step 5)."""
    return (
        "Which best matches what's present right now?\n"
        f"{format_domain_options()}\n"
        "Type the number (or name)."
    )

def refinement_menu(domain_key: str) -> str:
    """Return the full refinement menu prompt (Step 6)."""
    domain_label = get_domain_name(domain_key)
    return (
        f"{domain_label}: which fits best?\n"
        f"{format_refinement_options(domain_key)}\n"
        "Reply with a number (or type SKIP)."
    )
