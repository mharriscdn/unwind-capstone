# controller/classifier.py
import re
from dataclasses import dataclass
from typing import Optional

from controller.patterns import Pattern


DEBUG = False  # set False after verification


@dataclass
class Classification:
    is_confirmation: bool = False
    is_crisis: bool = False
    has_sensation_location: bool = False
    emotion_label: Optional[str] = None
    has_resistance: bool = False
    has_contraction: bool = False
    has_sensation_words: bool = False
    pattern: Optional[Pattern] = None


CONFIRM_PATTERNS = [
    r"\byes\b", r"\byep\b", r"\byup\b", r"\bexactly\b", r"\bthat's right\b", r"\bcorrect\b", r"\btrue\b"
]

LOCATION_WORDS = [
    "chest", "gut", "stomach", "throat", "neck", "jaw", "shoulders", "back",
    "heart", "belly", "solar plexus", "head"
]

EMOTION_WORDS = ["fear", "anxiety", "sadness", "anger", "shame", "panic", "stress"]

# Simple markers for training. We don't need perfect NLP; we need "good enough"
# detection to route the user into the right branch.
RESISTANCE_MARKERS = [
    "i don't want", "i dont want", "i can't", "i cant", "i shouldn't", "i shouldnt",
    "i hate", "this shouldn't", "this shouldnt", "i need this to stop", "make it stop",
    "get rid of", "go away", "can't stand", "cant stand",
]

CONTRACTION_WORDS = [
    "tight", "tightness", "bracing", "brace", "clench", "clenching", "contract", "contraction",
    "narrow", "narrowing", "pulling in", "closing", "compressed", "pressure",
]

SENSATION_WORDS = [
    "pressure", "heat", "cold", "vibration", "vibrating", "buzz", "buzzing", "tingle",
    "tingling", "flutter", "ache", "heavy", "light", "movement", "moving", "throb",
    "push", "pull", "push/pull", "bracing", "brace", "holding", "clench", "tension", "tightness",
]

TRIGGERS: dict[Pattern, list[str]] = {
    Pattern.CLAIMING_INSIGHT: [
        "i just realized", "oh wow", "i get it", "this is the answer", "now i understand",
        "breakthrough", "i'm seeing a pattern", "i see what i do"
    ],
    Pattern.CERTAINTY_SEEKING: [
        "am i doing", "doing this right", "how do i know", "what if", "is this correct",
        "is it working", "tell me if", "how can i be sure", "reassure me", "tell me i'm going to be okay"
    ],
    Pattern.PROBLEM_SOLVING: [
        "should i", "what should i do", "what's the answer", "how do i fix", "tell me what to do",
        "give me advice"
    ],
    Pattern.MANAGING: [
        "i'm trying to", "i keep trying", "i need to keep", "i have to stay", "am i doing it correctly",
        "i'm managing", "i'm forcing", "i'm controlling", "checking if i'm doing it right"
    ],
    Pattern.DESTINATION_SEEKING: [
        "what happens now", "is that it", "this isn't leading", "not leading anywhere",
        "nothing's happening", "nothing is happening", "i'm bored", "im bored",
        "when will this", "until it", "waiting for", "i'm waiting for", "waiting for it",
        "so it will", "so this resolves", "so it opens", "to get through", "to make it go away",
        "shift", "resolve"
    ],
    Pattern.FLOATING: [
        "i'm aware of", "i'm observing", "from awareness", "spacious", "just watching",
        "watching it", "the witness", "above it", "dissociated"
    ],
    Pattern.UNKNOWN_AVOIDANCE: [
        "i can't stand not knowing", "cant stand not knowing", "uncertainty is", "the uncertainty is",
        "not knowing is", "the unknown", "i need certainty", "i can't handle uncertainty"
    ],
    # STORY is default (with safeguards)
}


# Markers that indicate the user is adding meaning/explanation/narrative.
# This helps catch STORY even when a body location word is present.
STORY_MARKERS = [
    "meaning", "means", "because", "so that", "in the way", "wholeness", "should", "supposed to",
    "i think", "i feel it is", "this is not", "doesn't work", "not working", "why is", "why does",
]

# Markers that indicate narrative about external situations/people (not internal sensation)
# These trigger STORY even when emotion words are present
NARRATIVE_MARKERS = [
    # References to other people
    "my boss", "my wife", "my husband", "my partner", "my mom", "my dad", "my mother", "my father",
    "my friend", "my coworker", "my colleague", "my ex", "my sister", "my brother", "my family",
    "he said", "she said", "they said", "he did", "she did", "they did",
    "he is", "she is", "they are", "he was", "she was", "they were",
    # Situational/external descriptions
    "at work", "at home", "at school", "in the meeting", "on the phone",
    "getting on my nerves", "driving me crazy", "making me", "did to me", "said to me",
    "happened", "yesterday", "last week", "last night", "this morning", "earlier today",
    "when i was", "after i", "before i",
    # Complaint/venting patterns
    "i can't believe", "i cant believe", "can you believe", "it's so unfair", "its so unfair",
    "i'm so sick of", "im so sick of", "i'm tired of", "im tired of",
]


def classify_user_text(text: str) -> Classification:
    t = (text or "").lower().strip()

    # Minimal crisis detection (v1 exits)
    if any(x in t for x in ["suicide", "kill myself", "self-harm", "hurt myself", "hurt someone else"]):
        return Classification(is_crisis=True)

    is_confirmation = any(re.search(p, t) for p in CONFIRM_PATTERNS)
    has_location = any(w in t for w in LOCATION_WORDS)

    has_resistance = any(m in t for m in RESISTANCE_MARKERS)
    has_contraction = any(re.search(rf"\b{re.escape(w)}\b", t) for w in CONTRACTION_WORDS)
    has_sensation_words = any(re.search(rf"\b{re.escape(w)}\b", t) for w in SENSATION_WORDS)

    found_emotion = None
    for w in EMOTION_WORDS:
        if re.search(rf"\b{re.escape(w)}\b", t):
            found_emotion = w
            break

    detected_pattern: Optional[Pattern] = None
    matched_trigger: Optional[str] = None

    for pattern in [
        Pattern.CLAIMING_INSIGHT,
        Pattern.CERTAINTY_SEEKING,
        Pattern.PROBLEM_SOLVING,
        Pattern.MANAGING,
        Pattern.DESTINATION_SEEKING,
        Pattern.FLOATING,
        Pattern.UNKNOWN_AVOIDANCE,
    ]:
        for trigger in TRIGGERS.get(pattern, []):
            if trigger in t:
                detected_pattern = pattern
                matched_trigger = trigger
                break
        if detected_pattern is not None:
            break

    # STORY detection:
    # - We only default to STORY when there are no sensation indicators.
    # - If user mentions a location but also adds meaning/narrative markers, treat as STORY.
    # - If user is talking about external situations/people (NARRATIVE_MARKERS), treat as STORY.
    has_any_sensation_signal = has_location or has_contraction or has_sensation_words or (found_emotion is not None) or has_resistance
    has_narrative = any(m in t for m in NARRATIVE_MARKERS)

    if detected_pattern is None:
        if has_narrative:
            # Talking about external situations/people = STORY, even with emotion words
            detected_pattern = Pattern.STORY
        elif has_any_sensation_signal:
            # Only label as STORY if narrative markers appear.
            if any(m in t for m in STORY_MARKERS):
                detected_pattern = Pattern.STORY
        else:
            detected_pattern = Pattern.STORY

    if DEBUG:
        name = detected_pattern.name if detected_pattern is not None else "NONE"
        print(f"[DEBUG classify] text='{t[:80]}' -> {name} (trigger={matched_trigger})")

    return Classification(
        is_confirmation=is_confirmation,
        is_crisis=False,
        has_sensation_location=has_location,
        emotion_label=found_emotion,
        has_resistance=has_resistance,
        has_contraction=has_contraction,
        has_sensation_words=has_sensation_words,
        pattern=detected_pattern,
    )