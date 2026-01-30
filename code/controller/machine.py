# controller/machine.py
"""UNWIND v2 controller (CLI).

Single source of behavioral truth.

Aligned to:
- Orientation_FINAL_v4.docx
- Mirror_Mode_FINAL_v5.docx (with Layer 7: Spaciousness Check)
- QA_FINAL_v5.docx (informational; not shown during Mirror Mode)

v5 Changes:
- Orientation now has 13 screens (added THE CATEGORY ERROR)
- Added Layer 7: Spaciousness Check after 3+ successful stays
- Spaciousness check is once per session, lightly offered
- Two-switch insight planted in orientation, available in late-stage practice

Mirror Mode guardrails:
- Not teaching / explanation / regulation (except earned teaching at failure points)
- Escape detection is continuous (state-aware exemptions for forced-choice states)
- First-time pattern clarifier shown once per pattern, ever (persisted)
- Timed silence is the container (no prompts during silence)
- Spaciousness check only after repeated successful contact
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Callable, Optional

from controller.classifier import classify_user_text
from controller.patterns import Pattern
from controller.sensation_tree import (
    DOMAINS,
    parse_domain_choice,
    parse_refinement_choice,
    get_domain_name,
)
from controller.states import State
from controller.timed_input import timed_input

from language.templates import (
    route_used_before_prompt,
    route_returning_choice_prompt,
    orientation_screen_text,
    orientation_screen_count,
    mirror_central_view_prompt,
    mirror_domain_prompt,
    mirror_refinement_prompt,
    mirror_pick_number_or_name,
    mirror_pick_number_or_word,
    mirror_echo_and_word,
    mirror_remove_word,
    mirror_clench_question,
    mirror_clench_instruction,
    mirror_raw_sensation_minute,
    mirror_stay_whats_here_minute,
    mirror_sensory_fork,
    mirror_dense_layer1,
    mirror_dense_layer2,
    mirror_dense_layer3,
    mirror_dense_layer4,
    mirror_intensity_edge,
    mirror_continue_or_stop,
    mirror_spacious_stay,
    mirror_spacious_rest,
    mirror_whats_here_now,
    mirror_offapp_handoff,
    mirror_completion,
    mirror_pattern_first_time,
    mirror_pattern_one_word,
    mirror_spaciousness_check_1,
    mirror_spaciousness_check_2,
    mirror_spaciousness_check_fallback,
)

_PATTERN_MEMORY_PATH = os.path.join("logs", "pattern_memory.json")


def _is_done(text: str) -> bool:
    t = (text or "").strip().lower()
    return t in {"done", "finished", "im finished", "i'm finished", "stop", "that's enough", "thats enough"}


def _looks_like_one_word(text: str) -> bool:
    t = (text or "").strip()
    return bool(t) and len(t.split()) == 1


def _parse_123(text: str) -> Optional[int]:
    """Parse forced 1/2/3 choice. Returns 1, 2, or 3, or None if invalid."""
    t = (text or "").strip()
    if t in {"1", "2", "3"}:
        return int(t)
    # Also accept words
    t_lower = t.lower()
    if t_lower in {"yes", "y"}:
        return 1
    if t_lower in {"i think so", "think so", "maybe yes", "sort of"}:
        return 2
    if t_lower in {"no", "n", "not sure", "unclear", "unsure", "maybe", "i don't know", "idk"}:
        return 3
    return None


def _parse_sensory_fork(text: str) -> Optional[int]:
    """Parse sensory fork 1/2/3 choice. Returns 1, 2, or 3, or None if invalid."""
    t = (text or "").strip()
    if t in {"1", "2", "3"}:
        return int(t)
    # Also accept descriptive words
    t_lower = t.lower()
    if any(k in t_lower for k in ["dense", "tight", "more dense", "tighter", "heavier", "worse"]):
        return 1
    if any(k in t_lower for k in ["spacious", "less dense", "lighter", "open", "better", "released"]):
        return 2
    if any(k in t_lower for k in ["same", "no change", "unchanged", "nothing"]):
        return 3
    return None


@dataclass
class SessionMemory:
    used_before: Optional[bool] = None
    orientation_idx: int = 0  # 0-based
    pattern_explained: set[Pattern] = field(default_factory=set)

    # Mirror context
    last_sensation_report: Optional[str] = None
    last_domain_key: Optional[str] = None
    last_domain_label: Optional[str] = None
    last_refinement_label: Optional[str] = None
    last_user_word: Optional[str] = None
    
    # Dense path tracking (v4)
    dense_layer_count: int = 0  # how many times through dense path this session
    
    # Spaciousness check tracking (v5)
    successful_stays_count: int = 0  # count of times sensation reduced (spacious fork)
    spaciousness_check_done: bool = False  # once per session max
    
    # off-app handoff (once per session)
    offapp_given: bool = False

    transcript: list[dict] = field(default_factory=list)


class UnwindController:
    def __init__(self) -> None:
        self.state: State = State.ROUTE_USED_BEFORE
        self.mem = SessionMemory()
        self._wait_input_provider: Callable[[str, int], str | None] = timed_input
        self._load_pattern_memory()

    def set_wait_input_provider(self, provider: Callable[[str, int], str | None]) -> None:
        self._wait_input_provider = provider

    def _wait(self, prompt: str, seconds: int) -> str | None:
        return self._wait_input_provider(prompt, seconds)

    def _log(self, who: str, text: str, note: str | None = None) -> None:
        self.mem.transcript.append({"who": who, "text": text, "note": note})

    def ensure_logs_dir(self) -> None:
        os.makedirs("logs", exist_ok=True)

    def _load_pattern_memory(self) -> None:
        try:
            if os.path.exists(_PATTERN_MEMORY_PATH):
                with open(_PATTERN_MEMORY_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                names = set(data.get("explained", []))
                for p in Pattern:
                    if p.name in names:
                        self.mem.pattern_explained.add(p)
        except Exception:
            pass

    def _save_pattern_memory(self) -> None:
        try:
            self.ensure_logs_dir()
            with open(_PATTERN_MEMORY_PATH, "w", encoding="utf-8") as f:
                json.dump({"explained": sorted([p.name for p in self.mem.pattern_explained])}, f, indent=2)
        except Exception:
            pass

    # --- public API ---
    def start(self) -> str:
        msg = route_used_before_prompt()
        self._log("system", msg, note="start")
        return msg

    def tick_wait_states_if_needed(self) -> str | None:
        """Advance timed silence states (no user input required)."""
        
        # Main silence after clench (75s)
        if self.state == State.MIRROR_SILENCE:
            user = self._wait("", 75)
            if user is not None and user.strip():
                self._log("user", user, note="during_silence")
                return self.step(user)
            self.state = State.MIRROR_SENSORY_FORK
            msg = mirror_sensory_fork()
            self._log("system", msg, note="sensory_fork")
            return msg

        # Dense layer silences (60s each)
        if self.state == State.DENSE_SILENCE_1:
            user = self._wait("", 60)
            if user is not None and user.strip():
                self._log("user", user, note="during_dense_silence_1")
                return self.step(user)
            self.state = State.MIRROR_SENSORY_FORK
            msg = mirror_sensory_fork()
            self._log("system", msg, note="sensory_fork_after_dense1")
            return msg

        if self.state == State.DENSE_SILENCE_2:
            user = self._wait("", 60)
            if user is not None and user.strip():
                self._log("user", user, note="during_dense_silence_2")
                return self.step(user)
            self.state = State.MIRROR_SENSORY_FORK
            msg = mirror_sensory_fork()
            self._log("system", msg, note="sensory_fork_after_dense2")
            return msg

        if self.state == State.DENSE_SILENCE_3:
            user = self._wait("", 60)
            if user is not None and user.strip():
                self._log("user", user, note="during_dense_silence_3")
                return self.step(user)
            self.state = State.MIRROR_SENSORY_FORK
            msg = mirror_sensory_fork()
            self._log("system", msg, note="sensory_fork_after_dense3")
            return msg

        if self.state == State.DENSE_SILENCE_4:
            user = self._wait("", 60)
            if user is not None and user.strip():
                self._log("user", user, note="during_dense_silence_4")
                return self.step(user)
            self.state = State.DENSE_CONTINUE_OR_STOP
            msg = mirror_continue_or_stop()
            self._log("system", msg, note="continue_or_stop")
            return msg

        # Intensity check silence (45s)
        if self.state == State.INTENSITY_SILENCE:
            user = self._wait("", 45)
            if user is not None and user.strip():
                self._log("user", user, note="during_intensity_silence")
                return self.step(user)
            self.state = State.MIRROR_SENSORY_FORK
            msg = mirror_sensory_fork()
            self._log("system", msg, note="sensory_fork_after_intensity")
            return msg

        # Spacious silence (60s)
        if self.state == State.SPACIOUS_SILENCE:
            user = self._wait("", 60)
            if user is not None and user.strip():
                self._log("user", user, note="during_spacious_silence")
                return self.step(user)
            self.state = State.MIRROR_SPACIOUS_WHATS_HERE
            msg = mirror_whats_here_now()
            self._log("system", msg, note="whats_here_now")
            return msg

        # Spaciousness check silence (60s) — after "who sits with it" question
        if self.state == State.SPACIOUSNESS_SILENCE:
            user = self._wait("", 60)
            if user is not None and user.strip():
                self._log("user", user, note="during_spaciousness_check_silence")
                return self.step(user)
            # After silence, return to central view
            self.state = State.MIRROR_CENTRAL_VIEW
            msg = mirror_central_view_prompt()
            self._log("system", msg, note="central_view_after_spaciousness_check")
            return msg

        return None

    def step(self, user_text: str) -> str:
        self._log("user", user_text)

        if user_text.strip().lower() in {"quit", "exit"}:
            self.state = State.EXIT
            msg = mirror_completion()
            self._log("system", msg, note="exit")
            return msg

        c = classify_user_text(user_text)

        if c.is_crisis:
            self.state = State.EXIT
            msg = mirror_completion()
            self._log("system", msg, note="crisis_exit")
            return msg

        # Termination (user says done/finished) — honored anywhere in Mirror Mode
        if _is_done(user_text) and self.state not in {State.ROUTE_USED_BEFORE, State.ROUTE_RETURNING_CHOICE, State.ORIENTATION_SCREEN}:
            return self._finish_session()

        # Escape detection (continuous) with state-aware exemptions
        if self._should_apply_escape_detection():
            if not (self.state == State.MIRROR_ONE_WORD and _looks_like_one_word(user_text)):
                if c.pattern is not None:
                    return self._handle_pattern(c.pattern)

        # --- Entry routing ---
        if self.state == State.ROUTE_USED_BEFORE:
            ans = user_text.strip().lower()
            if ans in ("no", "n"):
                self.mem.used_before = False
                self.mem.orientation_idx = 0
                self.state = State.ORIENTATION_SCREEN
                msg = orientation_screen_text(0)
                self._log("system", msg, note="orientation_start")
                return msg
            if ans in ("yes", "y"):
                self.mem.used_before = True
                self.state = State.ROUTE_RETURNING_CHOICE
                msg = route_returning_choice_prompt()
                self._log("system", msg, note="returning_choice")
                return msg
            msg = route_used_before_prompt()
            self._log("system", msg, note="repeat_used_before")
            return msg

        if self.state == State.ROUTE_RETURNING_CHOICE:
            ans = user_text.strip()
            if ans == "1":
                self.mem.orientation_idx = 0
                self.state = State.ORIENTATION_SCREEN
                msg = orientation_screen_text(0)
                self._log("system", msg, note="orientation_review")
                return msg
            if ans == "2":
                self.state = State.MIRROR_CENTRAL_VIEW
                msg = mirror_central_view_prompt()
                self._log("system", msg, note="mirror_entry")
                return msg
            msg = route_returning_choice_prompt()
            self._log("system", msg, note="repeat_returning_choice")
            return msg

        # --- Orientation ---
        if self.state == State.ORIENTATION_SCREEN:
            # Safety screen cannot skip (screen 2 = idx 1)
            if self.mem.orientation_idx == 1:
                ans = user_text.strip().lower()
                if ans not in ("yes", "quit"):
                    msg = orientation_screen_text(self.mem.orientation_idx)
                    self._log("system", msg, note="repeat_safety")
                    return msg
                if ans == "quit":
                    self.state = State.EXIT
                    msg = mirror_completion()
                    self._log("system", msg, note="quit_safety")
                    return msg

            self.mem.orientation_idx += 1
            if self.mem.orientation_idx >= orientation_screen_count():
                self.state = State.MIRROR_CENTRAL_VIEW
                msg = mirror_central_view_prompt()
                self._log("system", msg, note="mirror_after_orientation")
                return msg

            msg = orientation_screen_text(self.mem.orientation_idx)
            self._log("system", msg, note="orientation_next")
            return msg

        # --- Mirror Mode: Central View & Sensation Tree ---
        if self.state == State.MIRROR_CENTRAL_VIEW:
            if _is_done(user_text):
                return self._finish_session()
            self.mem.last_sensation_report = user_text.strip()
            self.state = State.MIRROR_DOMAIN
            msg = self._render_domain_menu()
            self._log("system", msg, note="domain_menu")
            return msg

        if self.state == State.MIRROR_DOMAIN:
            domain_key = parse_domain_choice(user_text)
            if domain_key is None:
                msg = self._render_domain_menu()
                self._log("system", msg, note="repeat_domain_menu")
                return msg
            self.mem.last_domain_key = domain_key
            self.mem.last_domain_label = get_domain_name(domain_key)

            if self.mem.last_domain_label == "Neutral / Unclear":
                self.state = State.MIRROR_SILENCE
                msg = mirror_stay_whats_here_minute()
                self._log("system", msg, note="neutral_skip")
                return msg

            self.state = State.MIRROR_REFINEMENT
            msg = self._render_refinement_menu(domain_key)
            self._log("system", msg, note="refinement_menu")
            return msg

        if self.state == State.MIRROR_REFINEMENT:
            assert self.mem.last_domain_key is not None
            refinement = parse_refinement_choice(self.mem.last_domain_key, user_text)
            if refinement is None:
                msg = self._render_refinement_menu(self.mem.last_domain_key)
                self._log("system", msg, note="repeat_refinement_menu")
                return msg
            self.mem.last_refinement_label = refinement
            self.state = State.MIRROR_ONE_WORD
            msg = mirror_echo_and_word(refinement.lower(), (self.mem.last_domain_label or "").lower())
            self._log("system", msg, note="echo_and_word")
            return msg

        if self.state == State.MIRROR_ONE_WORD:
            # single-word answers should not be mirrored as Story
            self.mem.last_user_word = user_text.strip()
            self.state = State.MIRROR_CLENCH_CHOICE
            msg = mirror_remove_word(self.mem.last_user_word) + "\n\n" + mirror_clench_question()
            self._log("system", msg, note="remove_word_and_clench_q")
            return msg

        # --- Mirror Mode: Clench Question (FORCED 1/2/3 CHOICE) ---
        if self.state == State.MIRROR_CLENCH_CHOICE:
            choice = _parse_123(user_text)
            if choice is None:
                # Invalid input — just repeat the question
                msg = mirror_clench_question()
                self._log("system", msg, note="repeat_clench_choice")
                return msg
            
            # 1 = Yes, 2 = I think so → clench instruction
            # 3 = Not sure → raw sensation instruction
            if choice in {1, 2}:
                msg = mirror_clench_instruction()
            else:
                msg = mirror_raw_sensation_minute()
            
            self.state = State.MIRROR_SILENCE
            self._log("system", msg, note="contact_instruction")
            return msg

        # --- Mirror Mode: Sensory Fork (FORCED 1/2/3 CHOICE) ---
        if self.state == State.MIRROR_SENSORY_FORK:
            choice = _parse_sensory_fork(user_text)
            if choice is None:
                # Invalid input — just repeat
                msg = mirror_sensory_fork()
                self._log("system", msg, note="repeat_sensory_fork")
                return msg
            
            if choice == 1:  # More dense / tighter
                return self._route_to_dense_layer()
            elif choice == 2:  # Less dense / more spacious
                # Track successful stay (v5)
                self.mem.successful_stays_count += 1
                
                # Check if we should trigger spaciousness check (Layer 7)
                # Conditions: 3+ successful stays AND not done this session
                if self.mem.successful_stays_count >= 3 and not self.mem.spaciousness_check_done:
                    self.mem.spaciousness_check_done = True
                    self.state = State.SPACIOUSNESS_CHECK_1
                    msg = mirror_spaciousness_check_1()
                    self._log("system", msg, note="spaciousness_check_1")
                    return msg
                
                # Go directly to silence (like clench path) — no acknowledgment needed
                self.state = State.SPACIOUS_SILENCE
                msg = mirror_spacious_stay()
                self._log("system", msg, note="spacious_stay")
                return msg
            else:  # No real change (3) — treat as dense, continue contact
                return self._route_to_dense_layer()

        # --- Dense Path Layers ---
        if self.state == State.DENSE_LAYER_1:
            # User just saw layer 1 instruction, now silence
            self.state = State.DENSE_SILENCE_1
            return self.tick_wait_states_if_needed() or ""

        if self.state == State.DENSE_LAYER_2:
            self.state = State.DENSE_SILENCE_2
            return self.tick_wait_states_if_needed() or ""

        if self.state == State.DENSE_LAYER_3:
            self.state = State.DENSE_SILENCE_3
            return self.tick_wait_states_if_needed() or ""

        if self.state == State.DENSE_LAYER_4:
            self.state = State.DENSE_SILENCE_4
            return self.tick_wait_states_if_needed() or ""

        if self.state == State.DENSE_CONTINUE_OR_STOP:
            t = user_text.strip().lower()
            if any(k in t for k in ["stop", "done", "enough", "no", "quit"]):
                return self._finish_session()
            # Continue — reset dense layer count and go back to central view
            self.mem.dense_layer_count = 0
            self.state = State.MIRROR_CENTRAL_VIEW
            msg = mirror_central_view_prompt()
            self._log("system", msg, note="continue_after_dense4")
            return msg

        # --- Intensity Check ---
        if self.state == State.MIRROR_INTENSITY_CHECK:
            self.state = State.INTENSITY_SILENCE
            return self.tick_wait_states_if_needed() or ""

        # --- Spacious Path ---
        if self.state == State.MIRROR_SPACIOUS_STAY:
            # User acknowledged, now silence
            self.state = State.SPACIOUS_SILENCE
            return self.tick_wait_states_if_needed() or ""

        if self.state == State.MIRROR_SPACIOUS_WHATS_HERE:
            if _is_done(user_text):
                return self._finish_session()
            # user reports new sensation -> reset dense count, back to domain tree
            self.mem.dense_layer_count = 0
            self.mem.last_sensation_report = user_text.strip()
            self.state = State.MIRROR_DOMAIN
            msg = self._render_domain_menu()
            self._log("system", msg, note="domain_after_spacious")
            return msg

        # --- Layer 7: Spaciousness Check (v5) ---
        if self.state == State.SPACIOUSNESS_CHECK_1:
            choice = _parse_123(user_text)
            if choice is None:
                # Invalid input — just repeat
                msg = mirror_spaciousness_check_1()
                self._log("system", msg, note="repeat_spaciousness_check_1")
                return msg
            
            if choice == 1:  # Yes, both are here
                # Ask the second question: is there a solid someone?
                self.state = State.SPACIOUSNESS_CHECK_2
                msg = mirror_spaciousness_check_2()
                self._log("system", msg, note="spaciousness_check_2")
                return msg
            else:  # Only contraction (2) or Not sure (3)
                # Fallback — stay with what's here, back to silence
                self.state = State.MIRROR_SILENCE
                msg = mirror_spaciousness_check_fallback()
                self._log("system", msg, note="spaciousness_check_fallback")
                return msg

        if self.state == State.SPACIOUSNESS_CHECK_2:
            # Whatever they say, we just go silent. No validation. No follow-up.
            # This is the "who sits with it" moment — let them sit with whatever they noticed.
            self.state = State.SPACIOUSNESS_SILENCE
            # No prompt — just silence
            return self.tick_wait_states_if_needed() or ""

        # fallback
        self.state = State.MIRROR_CENTRAL_VIEW
        msg = mirror_central_view_prompt()
        self._log("system", msg, note="fallback")
        return msg

    # --- helpers ---
    def _should_apply_escape_detection(self) -> bool:
        """States where escape detection is BYPASSED (forced choice or menu states)."""
        return self.state not in {
            State.ROUTE_USED_BEFORE,
            State.ROUTE_RETURNING_CHOICE,
            State.ORIENTATION_SCREEN,
            State.MIRROR_DOMAIN,
            State.MIRROR_REFINEMENT,
            # v4: bypass for ALL forced-choice states
            State.MIRROR_CLENCH_CHOICE,
            State.MIRROR_SENSORY_FORK,
            State.DENSE_CONTINUE_OR_STOP,
            # v5: bypass for spaciousness check states
            State.SPACIOUSNESS_CHECK_1,
            State.SPACIOUSNESS_CHECK_2,
        }

    def _handle_pattern(self, p: Pattern) -> str:
        if p not in self.mem.pattern_explained:
            self.mem.pattern_explained.add(p)
            self._save_pattern_memory()
            msg = mirror_pattern_first_time(p)
        else:
            msg = mirror_pattern_one_word(p)
        self.state = State.MIRROR_CENTRAL_VIEW
        self._log("system", msg, note="pattern_mirror")
        return msg

    def _render_domain_menu(self) -> str:
        lines = [mirror_domain_prompt()]
        for i, d in enumerate(DOMAINS, start=1):
            lines.append(f"{i}) {d.label}")
        lines.append(mirror_pick_number_or_name())
        return "\n".join(lines)

    def _render_refinement_menu(self, domain_key: str) -> str:
        domain = next(d for d in DOMAINS if d.key == domain_key)
        lines = [mirror_refinement_prompt()]
        for i, r in enumerate(domain.refinements, start=1):
            lines.append(f"{i}) {r}")
        lines.append(mirror_pick_number_or_word())
        return "\n".join(lines)

    def _route_to_dense_layer(self) -> str:
        """Route to appropriate dense layer based on how many times we've been here."""
        self.mem.dense_layer_count += 1
        
        if self.mem.dense_layer_count == 1:
            self.state = State.DENSE_LAYER_1
            msg = mirror_dense_layer1()
            self._log("system", msg, note="dense_layer_1")
            # Immediately go to silence
            self.state = State.DENSE_SILENCE_1
            return msg
        elif self.mem.dense_layer_count == 2:
            self.state = State.DENSE_LAYER_2
            msg = mirror_dense_layer2()
            self._log("system", msg, note="dense_layer_2")
            self.state = State.DENSE_SILENCE_2
            return msg
        elif self.mem.dense_layer_count == 3:
            self.state = State.DENSE_LAYER_3
            msg = mirror_dense_layer3()
            self._log("system", msg, note="dense_layer_3")
            self.state = State.DENSE_SILENCE_3
            return msg
        else:  # 4+
            self.state = State.DENSE_LAYER_4
            msg = mirror_dense_layer4()
            self._log("system", msg, note="dense_layer_4")
            self.state = State.DENSE_SILENCE_4
            return msg

    def _finish_session(self) -> str:
        # Step 14 off-app handoff once per session
        if not self.mem.offapp_given:
            self.mem.offapp_given = True
            msg = mirror_offapp_handoff() + "\n\n" + mirror_completion()
        else:
            msg = mirror_completion()
        self.state = State.EXIT
        self._log("system", msg, note="completion")
        return msg
