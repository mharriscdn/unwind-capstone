# tests/test_machine.py
"""Unit tests for the UNWIND state machine."""

import pytest
from controller.machine import UnwindController
from controller.states import State


class TestEntryRouting:
    """Tests for entry routing (new vs returning user)."""

    def test_start_prompts_used_before(self):
        ctrl = UnwindController()
        msg = ctrl.start()
        assert "Have you used UNWIND before?" in msg

    def test_new_user_goes_to_orientation(self):
        ctrl = UnwindController()
        ctrl.start()
        ctrl.step("no")
        assert ctrl.state == State.ORIENTATION_SCREEN
        assert ctrl.mem.orientation_idx == 0

    def test_returning_user_gets_choice(self):
        ctrl = UnwindController()
        ctrl.start()
        ctrl.step("yes")
        assert ctrl.state == State.ROUTE_RETURNING_CHOICE

    def test_returning_user_can_skip_to_mirror(self):
        ctrl = UnwindController()
        ctrl.start()
        ctrl.step("yes")
        ctrl.step("2")  # Go to Mirror Mode
        assert ctrl.state == State.MIRROR_CENTRAL_VIEW


class TestOrientation:
    """Tests for orientation screen flow."""

    def test_orientation_has_13_screens(self):
        from language.templates import orientation_screen_count
        assert orientation_screen_count() == 13

    def test_safety_screen_requires_yes_or_quit(self):
        ctrl = UnwindController()
        ctrl.start()
        ctrl.step("no")  # new user
        ctrl.step("yes")  # screen 1
        # Now at safety screen (idx 1)
        assert ctrl.mem.orientation_idx == 1
        # Typing random text should repeat the screen
        resp = ctrl.step("maybe")
        assert "Type YES to continue / Type QUIT to exit" in resp

    def test_quit_at_safety_exits(self):
        ctrl = UnwindController()
        ctrl.start()
        ctrl.step("no")
        ctrl.step("yes")  # screen 1
        ctrl.step("quit")  # safety screen
        assert ctrl.state == State.EXIT

    def test_complete_orientation_enters_mirror(self):
        ctrl = UnwindController()
        ctrl.start()
        ctrl.step("no")
        for _ in range(13):
            ctrl.step("yes")
        assert ctrl.state == State.MIRROR_CENTRAL_VIEW


class TestMirrorModePatternDetection:
    """Tests for escape pattern detection in Mirror Mode."""

    def setup_method(self):
        """Skip orientation to get to Mirror Mode."""
        self.ctrl = UnwindController()
        self.ctrl.start()
        self.ctrl.step("no")
        for _ in range(13):
            self.ctrl.step("yes")
        assert self.ctrl.state == State.MIRROR_CENTRAL_VIEW

    def test_story_detected_and_mirrored(self):
        resp = self.ctrl.step("my boss is driving me crazy")
        assert "Story" in resp
        assert "What's most pressing" in resp

    def test_certainty_seeking_detected(self):
        resp = self.ctrl.step("am I doing this right?")
        assert "Certainty-Seeking" in resp

    def test_claiming_insight_detected(self):
        resp = self.ctrl.step("I get it now!")
        assert "Claiming/Insight" in resp

    def test_destination_seeking_detected(self):
        resp = self.ctrl.step("what happens now")
        assert "Destination-Seeking" in resp

    def test_managing_detected(self):
        resp = self.ctrl.step("I'm trying to stay with it")
        assert "Managing" in resp

    def test_floating_detected(self):
        resp = self.ctrl.step("I'm just observing from awareness")
        assert "Floating" in resp

    def test_sensation_report_proceeds(self):
        """Pure sensation should proceed to domain menu, not trigger pattern."""
        resp = self.ctrl.step("tightness in my chest")
        assert "Which best matches" in resp
        assert self.ctrl.state == State.MIRROR_DOMAIN


class TestSensationTree:
    """Tests for sensation tree navigation."""

    def setup_method(self):
        self.ctrl = UnwindController()
        self.ctrl.start()
        self.ctrl.step("no")
        for _ in range(13):
            self.ctrl.step("yes")
        self.ctrl.step("gut clench")  # central view -> domain

    def test_domain_selection_by_number(self):
        resp = self.ctrl.step("1")  # Pressure / Force
        assert "Which fits best?" in resp
        assert self.ctrl.state == State.MIRROR_REFINEMENT

    def test_domain_selection_by_name(self):
        resp = self.ctrl.step("pressure")
        assert "Which fits best?" in resp

    def test_neutral_skips_refinement(self):
        resp = self.ctrl.step("10")  # Neutral / Unclear
        assert "Stay with what's here" in resp
        assert self.ctrl.state == State.MIRROR_SILENCE

    def test_refinement_to_one_word(self):
        self.ctrl.step("9")  # Intensity
        resp = self.ctrl.step("7")  # Steady
        assert "one word to describe it" in resp
        assert self.ctrl.state == State.MIRROR_ONE_WORD

    def test_one_word_to_clench_question(self):
        self.ctrl.step("9")  # Intensity
        self.ctrl.step("7")  # Steady
        resp = self.ctrl.step("tight")
        assert "can you feel where you're bracing" in resp
        assert "1) Yes" in resp
        assert "2) I think so" in resp
        assert "3) Not sure" in resp


class TestClenchPath:
    """Tests for clench question and contact path."""

    def setup_method(self):
        self.ctrl = UnwindController()
        self.ctrl.start()
        self.ctrl.step("no")
        for _ in range(13):
            self.ctrl.step("yes")
        self.ctrl.step("gut clench")
        self.ctrl.step("9")  # Intensity
        self.ctrl.step("7")  # Steady
        self.ctrl.step("tight")
        assert self.ctrl.state == State.MIRROR_CLENCH_CHOICE

    def test_clench_yes_gives_instruction(self):
        resp = self.ctrl.step("1")  # Yes
        assert "Feel that clench" in resp
        assert "Both at once" in resp

    def test_clench_think_so_gives_instruction(self):
        resp = self.ctrl.step("2")  # I think so
        assert "Feel that clench" in resp

    def test_clench_not_sure_gives_raw_sensation(self):
        resp = self.ctrl.step("3")  # Not sure
        assert "Stay with the raw sensation" in resp


class TestSensoryFork:
    """Tests for sensory fork after silence."""

    def setup_method(self):
        self.ctrl = UnwindController()
        # Use a mock wait provider that returns None (simulates silence completing)
        self.ctrl.set_wait_input_provider(lambda prompt, seconds: None)
        self.ctrl.start()
        self.ctrl.step("no")
        for _ in range(13):
            self.ctrl.step("yes")
        self.ctrl.step("gut clench")
        self.ctrl.step("9")
        self.ctrl.step("7")
        self.ctrl.step("tight")
        self.ctrl.step("1")  # Clench choice
        # Tick to complete silence
        self.ctrl.tick_wait_states_if_needed()
        assert self.ctrl.state == State.MIRROR_SENSORY_FORK

    def test_fork_more_dense_goes_to_dense_layer(self):
        resp = self.ctrl.step("1")  # More dense
        assert "Don't fix it" in resp or "both poles" in resp

    def test_fork_more_spacious_goes_to_spacious(self):
        resp = self.ctrl.step("2")  # Less dense / more spacious
        assert "spacious quality" in resp

    def test_fork_no_change_goes_to_dense(self):
        resp = self.ctrl.step("3")  # No real change
        assert "Don't fix it" in resp or "both poles" in resp


class TestDenseLayers:
    """Tests for dense path layer progression."""

    def setup_method(self):
        self.ctrl = UnwindController()
        self.ctrl.set_wait_input_provider(lambda prompt, seconds: None)
        self.ctrl.start()
        self.ctrl.step("no")
        for _ in range(13):
            self.ctrl.step("yes")
        self.ctrl.step("gut clench")
        self.ctrl.step("9")
        self.ctrl.step("7")
        self.ctrl.step("tight")
        self.ctrl.step("1")
        self.ctrl.tick_wait_states_if_needed()  # -> sensory fork

    def test_dense_layer_progression(self):
        """Test that dense layers progress correctly."""
        # Layer 1
        self.ctrl.step("1")  # More dense
        self.ctrl.tick_wait_states_if_needed()
        assert self.ctrl.mem.dense_layer_count == 1

        # Layer 2
        self.ctrl.step("1")  # Still dense
        self.ctrl.tick_wait_states_if_needed()
        assert self.ctrl.mem.dense_layer_count == 2

        # Layer 3
        self.ctrl.step("1")  # Still dense
        self.ctrl.tick_wait_states_if_needed()
        assert self.ctrl.mem.dense_layer_count == 3

        # Layer 4
        resp = self.ctrl.step("1")  # Still dense
        self.ctrl.tick_wait_states_if_needed()
        assert self.ctrl.mem.dense_layer_count == 4
        # After layer 4, should ask continue or stop
        assert self.ctrl.state == State.DENSE_CONTINUE_OR_STOP


class TestSpaciousnessCheck:
    """Tests for Layer 7 spaciousness check."""

    def setup_method(self):
        self.ctrl = UnwindController()
        self.ctrl.set_wait_input_provider(lambda prompt, seconds: None)
        self.ctrl.start()
        self.ctrl.step("no")
        for _ in range(13):
            self.ctrl.step("yes")

    def _complete_one_cycle_spacious(self):
        """Helper to complete one cycle ending in spacious."""
        self.ctrl.step("gut clench")
        self.ctrl.step("9")
        self.ctrl.step("7")
        self.ctrl.step("tight")
        self.ctrl.step("1")  # Clench yes
        self.ctrl.tick_wait_states_if_needed()
        self.ctrl.step("2")  # Spacious
        self.ctrl.tick_wait_states_if_needed()
        self.ctrl.step("continuing")  # What's here now -> back to central view

    def test_spaciousness_check_triggers_after_3_stays(self):
        """After 3 successful stays, spaciousness check should trigger."""
        # First two cycles - no check yet
        for i in range(2):
            self.ctrl.step("gut clench")
            self.ctrl.step("9")
            self.ctrl.step("7")
            self.ctrl.step("tight")
            self.ctrl.step("1")
            self.ctrl.tick_wait_states_if_needed()
            self.ctrl.step("2")  # Spacious
            self.ctrl.tick_wait_states_if_needed()
            self.ctrl.step("something else")  # Continue
            assert self.ctrl.mem.spaciousness_check_done is False

        # Third cycle should trigger check
        self.ctrl.step("gut clench")
        self.ctrl.step("9")
        self.ctrl.step("7")
        self.ctrl.step("tight")
        self.ctrl.step("1")
        self.ctrl.tick_wait_states_if_needed()
        resp = self.ctrl.step("2")  # Third spacious
        assert "spaciousness also present" in resp
        assert self.ctrl.state == State.SPACIOUSNESS_CHECK_1

    def test_spaciousness_check_only_once_per_session(self):
        """Spaciousness check should only happen once per session."""
        # Complete 3 cycles to trigger check
        for i in range(3):
            self.ctrl.step("gut clench")
            self.ctrl.step("9")
            self.ctrl.step("7")
            self.ctrl.step("tight")
            self.ctrl.step("1")
            self.ctrl.tick_wait_states_if_needed()
            if i < 2:
                self.ctrl.step("2")
                self.ctrl.tick_wait_states_if_needed()
                self.ctrl.step("something")
            else:
                resp = self.ctrl.step("2")
                assert "spaciousness also present" in resp

        # Answer the check
        self.ctrl.step("2")  # Only contraction
        
        # Continue session - 4th spacious should NOT trigger check again
        self.ctrl.step("gut clench")
        self.ctrl.step("9")
        self.ctrl.step("7")
        self.ctrl.step("tight")
        self.ctrl.step("1")
        self.ctrl.tick_wait_states_if_needed()
        resp = self.ctrl.step("2")  # 4th spacious
        assert "spaciousness also present" not in resp  # No second check


class TestSessionEnd:
    """Tests for session termination."""

    def setup_method(self):
        self.ctrl = UnwindController()
        self.ctrl.set_wait_input_provider(lambda prompt, seconds: None)
        self.ctrl.start()
        self.ctrl.step("no")
        for _ in range(13):
            self.ctrl.step("yes")

    def test_done_ends_session(self):
        resp = self.ctrl.step("done")
        assert "See you next time" in resp
        assert self.ctrl.state == State.EXIT

    def test_quit_ends_session(self):
        resp = self.ctrl.step("quit")
        assert "See you next time" in resp
        assert self.ctrl.state == State.EXIT

    def test_offapp_handoff_given_once(self):
        resp = self.ctrl.step("done")
        assert "Off-app" in resp
        assert "the switch flipping" in resp


class TestCrisisHandling:
    """Tests for crisis detection and handling."""

    def setup_method(self):
        self.ctrl = UnwindController()
        self.ctrl.start()
        self.ctrl.step("no")
        for _ in range(13):
            self.ctrl.step("yes")

    def test_crisis_exits_immediately(self):
        resp = self.ctrl.step("I want to kill myself")
        assert self.ctrl.state == State.EXIT
