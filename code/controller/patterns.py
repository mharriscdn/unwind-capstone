# controller/patterns.py
"""Escape patterns (8) exactly as defined in Mirror_Mode_REVISED.

Mirror Mode uses ONLY the pattern name (one word).
First-time detection adds one short clarifier (handled in templates).
"""

from __future__ import annotations

from enum import Enum, auto


class Pattern(Enum):
    STORY = auto()
    CERTAINTY_SEEKING = auto()
    PROBLEM_SOLVING = auto()
    CLAIMING_INSIGHT = auto()
    MANAGING = auto()
    DESTINATION_SEEKING = auto()
    FLOATING = auto()
    UNKNOWN_AVOIDANCE = auto()

    @property
    def label(self) -> str:
        return {
            Pattern.STORY: "Story",
            Pattern.CERTAINTY_SEEKING: "Certainty-Seeking",
            Pattern.PROBLEM_SOLVING: "Problem-Solving",
            Pattern.CLAIMING_INSIGHT: "Claiming/Insight",
            Pattern.MANAGING: "Managing",
            Pattern.DESTINATION_SEEKING: "Destination-Seeking",
            Pattern.FLOATING: "Floating",
            Pattern.UNKNOWN_AVOIDANCE: "Unknown-Avoidance",
        }[self]
