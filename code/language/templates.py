# language/templates.py
"""Locked strings for UNWIND v2 (CLI).

Aligned to:
- Orientation_FINAL_v4.docx
- Mirror_Mode_FINAL_v5.docx (with Layer 7: Spaciousness Check)
- QA_FINAL_v5.docx (informational reference; not shown during Mirror Mode)

Guardrails:
- Mirror Mode uses doc-approved phrases and does not explain the deep mechanism.
- Somatic checkpoints use forced choice (1/2/3) — NOT free-text classifier
- Layer 7 (Spaciousness Check) only triggers after 3+ successful stays, once per session
"""

from __future__ import annotations

from typing import List, Tuple

from controller.patterns import Pattern

# -----------------------------------------------------------------------------
# Orientation screens (13) — exact text from Orientation_FINAL_v4.docx
# -----------------------------------------------------------------------------
_ORIENTATION: List[Tuple[str, str, str]] = [
    # Screen 1 — WELCOME
    [
        "UNWIND",
        "A training tool for noticing how you leave\n\nThis app is not here to help you feel better. It's here to show you how you avoid feeling.\nIf you're willing to see that, this can help. If not, it won't.",
        "Type YES to continue / Type QUIT to exit"
    ],
    # Screen 2 — SAFETY
    [
        "Before We Begin",
        "This tool is not for people currently experiencing:\n• active abuse or unsafe environments\n• acute crisis or suicidal ideation\n• unresolved trauma that still has teeth\nIf that describes you, please work with a therapist first.\nThis app will NOT soothe you or calm you down. It will show you how you avoid feeling.",
        "Type YES to continue / Type QUIT to exit"
    ],
    # Screen 3 — THE CATEGORY ERROR (NEW)
    [
        "Why This Exists",
        "Here's what's underneath all of it:\n\nThe nervous system is applying protective logic to internal sensations as if they were physical threats.\n\nIn the external world, the body can be hit. A car can strike you. Protection makes sense.\n\nBut internally? There's nothing localized that can be damaged. The \"me\" that needs protecting is part of the projection.\n\nThe gun is real as experience. The bullets are blanks. They fire and hit nothing — because there's nothing there to hit.\n\nThat's the category error. The rules of being hit are being applied where nothing can be hit.\n\nThis app exists to help you verify that through contact.",
        "Type YES to continue"
    ],
    # Screen 4 — THE RAIL SWITCH
    [
        "How It Works",
        "Most of the time, we don't experience life directly.\nWhen something uncomfortable appears, a rail switch flips. Experience gets routed from direct perception to filtered mental experience.\nThat switch is the clench — existential bracing.\nWhen the switch flips, the blinds close. You're no longer looking at reality directly. The mind fills the vacuum — backfilling threats, futures, catastrophes.\nNot because the mind is lying. But because the body is mobilized and the mind needs to justify the mobilization.\nThis app shows you that switch — as it flips.",
        "Type YES to continue"
    ],
    # Screen 5 — THE CORE LOOP
    [
        "The Loop",
        "Here's the basic sequence:\n1. Trigger (something happens)\n2. Arousal (body mobilizing — the hum, not yet suffering)\n3. System checks windshield — no lion, but arousal still there\n4. Rail switch flips — the clench (existential bracing)\n5. Blinds close — direct experience filtered through mind\n6. Mind fills vacuum — backfills threats to justify mobilization\n7. Beachball appears (sensation + story fused, loud and urgent)\n8. Mind holds you at gunpoint — managing the projections\n9. Manager appears to handle the \"threat\"\n\nWhen the clench is felt FULLY (both poles — the arousal AND the bracing against it), the switch flips back. Blinds open. Direct experience resumes.\nWhen felt PARTIALLY (just enough to trigger, not enough to feel safe), the blinds stay closed. Mind keeps projecting. Questions generate.\nThis app helps you notice when the switch flips and feel the clench fully before the mind takes over.",
        "Type YES to continue"
    ],
    # Screen 6 — WHY ESCAPE HAPPENS
    [
        "Why You Escape",
        "At some point — often very early — your nervous system learned: \"This feeling is too much.\"\nThat learning may be decades old.\nThe system learned to apply protective logic to internal sensation — as if the feeling itself could destroy you. But internally, there's nothing that can be hit.\nThe fear is real as experience. But it's shooting blanks. The consequences never come.\nWhat remains is a habit: Switch flips → blinds close → react to projections → repeat\nThe mind's authority depends on you never finding out what happens if you stop watching the movie and open the blinds.\nYou won't understand your way out of this. Your system has to learn something new.\nThat only happens through contact.",
        "Type YES to continue"
    ],
    # Screen 7 — THE SOCK
    [
        "One Important Thing",
        "You do not need to find the origin. You do not need to know why this started. You do not need to relive the past.\nIf this happened when you were two and you're forty now — you're not running from a monster.\nYou're running from a sock you once thought was one.\nYou kept the blinds closed to make it convincing. The mind kept projecting threats onto those blinds. The gun felt real. But it was shooting blanks — because internally, there's nothing to hit.\nThis app is designed to open the blinds.\nThe only thing that updates the system is discovering: \"I can feel this — and nothing bad happens.\"",
        "Type YES to continue"
    ],
    # Screen 8 — CENTRAL VIEW
    [
        "Central View",
        "When sensation arises, attention automatically moves one of two directions:\nLEFT: toward the projections on the blinds — story, explanation, threat management\nRIGHT: toward the sensation itself — direct experience\nThe app will show you when you've gone left.\nCentral view is not a special state. It's just: what's most pressing right now — before the mind fills the vacuum?\nWhen you notice you've drifted left into the movie, you can return to center — to what's actually arising.",
        "Type YES to continue"
    ],
    # Screen 9 — CURIOSITY POSTURE
    [
        "Curiosity",
        "The app will guide you to feel sensation with curiosity — not management.\nCuriosity means: \"What is this, actually?\"\nNot: \"How do I fix this?\" Not: \"What does this mean?\" Not: \"When will this end?\"\nJust: direct contact with what's arising.\nWithout the word \"dangerous.\" Without the word \"unbearable.\" Without trying to change it.",
        "Type YES to continue"
    ],
    # Screen 10 — SENSATION ATTRIBUTES
    [
        "What To Notice",
        "When you feel sensation directly, you might notice:\n• Location (where in the body?)\n• Quality (tight? warm? heavy? electric?)\n• Movement (spreading? pulsing? static?)\n• Intensity (faint? strong? fluctuating?)\nYou're not analyzing. You're making contact.\nThe beachball (sensation + story fused) is loud — it's what you notice first. But it's downstream.\nThe clench is underneath it. That's where the work happens.\nThe app will help you notice sensation precisely, then drop beneath it to the clench.",
        "Type YES to continue"
    ],
    # Screen 11 — HOW THE BLINDS OPEN (EXPANDED with two-switch insight)
    [
        "What Actually Changes Things",
        "The blinds can only open one way: by feeling the clench fully.\nThe clench contains two poles:\n• The arousal (the sensation, the hum, the activation)\n• The bracing AGAINST that arousal (the fear of it, the holding)\nWhen both poles are felt simultaneously — the sensation AND the bracing against it — the charge discharges. The switch flips back. The blinds open.\nThrough titration — staying when you wanted to run — you discover the projections were shooting blanks. The gun was real as experience. The consequences never came. Because internally, there was nothing to hit.\nWhen you call the bluff and feel the clench fully, direct experience resumes. The arousal underneath reveals itself as just aliveness. The thing you were running from was harmless. A sock.\nOnce the bluff has been called enough times, the projector loses credibility. The blinds don't stay open because you hold them open. They stay open because there's no incentive left to close them.\n\nAnd sometimes, after repeated contact, something else becomes obvious: while contraction is happening, spaciousness is also present. Not after the contraction. Not instead of it. At the same time.\nYou're spacious while contracted.\nWhen you notice that, you might also notice: there's no solid someone sitting with the contraction. Just experience happening. Contraction and awareness of contraction — but no one in between.\nThat's not something to seek. It's what reveals itself when you stop running.",
        "Type YES to continue"
    ],
    # Screen 12 — THE 8 ESCAPE PATTERNS
    [
        "How You Leave",
        "The app watches for these 8 escape patterns — ways you go left into the movie instead of staying with sensation:\n1. STORY — narrative about what happened or what comes next\n2. CERTAINTY-SEEKING — \"Am I doing this right?\"\n3. PROBLEM-SOLVING — turning sensation into puzzle to solve\n4. CLAIMING/INSIGHT — \"I get it now!\"\n5. MANAGING — monitoring the staying\n6. DESTINATION-SEEKING — waiting for shift\n7. FLOATING — dissociative witnessing\n8. UNKNOWN-AVOIDANCE — scrambling when uncertain\nThese are exactly as documented in Clear Seeing (Chapter 15).\nWhen the app detects one, it mirrors it back briefly. Then redirects you to sensation. Then helps you drop beneath the beachball to the clench.",
        "Type YES to continue"
    ],
    # Screen 13 — MIRROR MODE (UPDATED)
    [
        "What Happens Next",
        "You'll now enter Mirror Mode.\nThe app will:\n• Listen as you speak\n• Detect when you've gone left into the movie (escaped into one of the 8 patterns)\n• Mirror the pattern back (one word)\n• Redirect you to central view\n• Help you notice the beachball (sensation + story)\n• Help you drop beneath it to the clench (both poles)\n• Check temporal qualities (what has changed or stayed the same)\n• After repeated contact, check if spaciousness is present while contracted\n• Stay quiet while you feel\nNo fixing. No teaching. No soothing.\nJust: noticing escape, returning to sensation, dropping to the clench, feeling both poles, staying in contact.\nThe container holds. You do the feeling. The blinds open on their own.",
        "Type YES to begin Mirror Mode"
    ]
]

def orientation_screen_count() -> int:
    return len(_ORIENTATION)

def orientation_screen_text(index: int) -> str:
    title, body, action = _ORIENTATION[index]
    return f"{title}\n\n{body}\n\nAction: {action}"

# -----------------------------------------------------------------------------
# Entry routing prompts (Mirror_Mode_FINAL_v4)
# -----------------------------------------------------------------------------
def route_used_before_prompt() -> str:
    return "Have you used UNWIND before?\n\nType YES or NO."

def route_returning_choice_prompt() -> str:
    return "Would you like to:\n1. Review Orientation\n2. Go to Mirror Mode\n\nType 1 or 2."

# -----------------------------------------------------------------------------
# Mirror Mode phrases (Mirror_Mode_FINAL_v4)
# -----------------------------------------------------------------------------
def mirror_central_view_prompt() -> str:
    return "What's most pressing in your central view right now?"

def mirror_domain_prompt() -> str:
    return "Which best matches what's present right now?"

def mirror_refinement_prompt() -> str:
    return "Which fits best?"

def mirror_pick_number_or_name() -> str:
    return "Type the number (or name)."

def mirror_pick_number_or_word() -> str:
    return "Type the number (or word)."

def mirror_echo_and_word(refinement: str, domain: str) -> str:
    return f"Notice that {refinement} {domain}. If you had to use one word to describe it, what would it be?"

def mirror_remove_word(user_word: str) -> str:
    return f"Now feel that sensation without the word '{user_word}.' Just the raw sensation itself."

# -----------------------------------------------------------------------------
# CLENCH QUESTION — FORCED CHOICE (v4 FIX)
# -----------------------------------------------------------------------------
def mirror_clench_question() -> str:
    """Forced 1/2/3 choice — NOT free-text. Prevents false escape classification."""
    return """Beneath that sensation, can you feel where you're bracing against it?
The tightness holding against it?

1) Yes
2) I think so
3) Not sure / unclear

Type 1, 2, or 3."""

def mirror_clench_instruction() -> str:
    return "Feel that clench — the whole charged tension. The sensation AND the bracing against it. Both at once. Stay with it for about a minute."

def mirror_raw_sensation_minute() -> str:
    return "That's okay. Stay with the raw sensation itself for about a minute."

def mirror_stay_whats_here_minute() -> str:
    return "Stay with what's here for about a minute."

# -----------------------------------------------------------------------------
# FORCED SENSORY FORK — AFTER SILENCE (v4 FIX)
# -----------------------------------------------------------------------------
def mirror_sensory_fork() -> str:
    """Forced 1/2/3 choice — NOT open 'What happened?' question."""
    return """As you stayed with it, what happened in the sensation itself?

1) More dense / tighter
2) Less dense / more spacious
3) No real change

Type 1, 2, or 3."""

# -----------------------------------------------------------------------------
# DENSE PATH — LAYERED (v4)
# -----------------------------------------------------------------------------
def mirror_dense_layer1() -> str:
    """Layer 1: Both poles, no teaching yet."""
    return """Okay. Don't fix it.
See if you can feel both poles at once:
the sensation and the bracing against it.
Stay with it for about a minute."""

def mirror_dense_layer2() -> str:
    """Layer 2: Curiosity (first teaching moment)."""
    return """Okay. Don't chase spaciousness.
Don't fight density.
Just stay curious about what's here.

Density isn't a problem.
It's just sensation.

Stay with it for about another minute."""

def mirror_dense_layer3() -> str:
    """Layer 3: Mechanism clarification (earned teaching)."""
    return """Okay. This is important.

Fear is real as sensation —
but the threats are empty.

This is all bark. No bite.
There are no daggers here.

You're not facing danger.
You're facing energy the body learned to brace against.

Nothing bad is happening.

Stay with it — not to change it —
just to see that nothing happens.

Stay for about a minute."""

def mirror_dense_layer4() -> str:
    """Layer 4: Rest here (valid terminal state)."""
    return """Okay. You don't need to get past this.

See how long you can rest right here —
not there, not after — here.

This is just fear with no bite.
And you're discovering that you can feel it.

Through staying — slowly, gently —
your nervous system learns: this is safe.

That's what flips the switch.
From the movie back to reality.
From Bullshit Valley to what's actually here.

You can rest here."""

def mirror_intensity_edge() -> str:
    """Intensity check: edge work if overwhelmed."""
    return """If the intensity feels above 8 out of 10,
don't feel the whole thing.

Find the edge of it.
Feel just the edge.

Stay there.
Notice: nothing bad happens."""

def mirror_continue_or_stop() -> str:
    return "Would you like to continue or stop here for today?"

# -----------------------------------------------------------------------------
# SPACIOUS PATH (v4)
# -----------------------------------------------------------------------------
def mirror_spacious_stay() -> str:
    """Spacious path: stay with spaciousness directly."""
    return "Feel that more spacious quality directly — not as an idea.\nStay with it for about another minute."

def mirror_spacious_rest() -> str:
    return "Rest in that. Nothing to do. When you're ready, let me know."

def mirror_whats_here_now() -> str:
    return "What's here now?"

# -----------------------------------------------------------------------------
# Session end
# -----------------------------------------------------------------------------
def mirror_completion() -> str:
    return "Okay. See you next time."

def mirror_offapp_handoff() -> str:
    return "Off-app: when urgency hits, that's the switch flipping. Feel what's underneath. If it's dense — stay, nothing happens. If it's spacious — you're already home. Either way, the dog has no teeth."

# -----------------------------------------------------------------------------
# Pattern mirroring
# -----------------------------------------------------------------------------
def mirror_pattern_first_time(p: Pattern) -> str:
    return f"That's {p.label} — leaving sensation.\nIt doesn't work because it moves attention away from what's actually here.\n\n{mirror_central_view_prompt()}"

def mirror_pattern_one_word(p: Pattern) -> str:
    return f"{p.label}.\n\n{mirror_central_view_prompt()}"

# -----------------------------------------------------------------------------
# SPACIOUSNESS CHECK — LAYER 7 (v5)
# Only after 3+ successful stays, once per session max
# -----------------------------------------------------------------------------
def mirror_spaciousness_check_1() -> str:
    """First prompt: is spaciousness present while contracted?"""
    return """As you stay with the density... is spaciousness also present right now?
Not after the contraction — but with it?

1) Yes, both are here
2) Only contraction
3) Not sure

Type 1, 2, or 3."""

def mirror_spaciousness_check_2() -> str:
    """Second prompt (only if they answered 1): is there a solid someone?"""
    return "Is there a solid someone feeling this — or is sensation just happening?"

def mirror_spaciousness_check_fallback() -> str:
    """If they answered 2 or 3 on first prompt."""
    return "That's fine. Stay with what's here."
