# tests/test_classifier.py
"""Unit tests for the escape pattern classifier."""

import pytest
from controller.classifier import classify_user_text, Pattern


class TestStoryDetection:
    """Tests for STORY pattern detection."""

    def test_narrative_about_boss(self):
        """Narrative about external person should be STORY."""
        result = classify_user_text("my boss is getting on my nerves and I am so angry")
        assert result.pattern == Pattern.STORY

    def test_narrative_about_spouse(self):
        """Narrative about spouse should be STORY."""
        result = classify_user_text("my wife said something that really hurt me")
        assert result.pattern == Pattern.STORY

    def test_past_event_narrative(self):
        """Past event description should be STORY."""
        result = classify_user_text("yesterday at work something terrible happened")
        assert result.pattern == Pattern.STORY

    def test_pure_sensation_not_story(self):
        """Pure sensation report should NOT be STORY."""
        result = classify_user_text("tightness in my chest")
        assert result.pattern is None  # No escape pattern detected

    def test_emotion_with_narrative_is_story(self):
        """Emotion + narrative context should be STORY."""
        result = classify_user_text("I feel anxious about what happened yesterday at work")
        assert result.pattern == Pattern.STORY

    def test_venting_pattern(self):
        """Venting/complaining should be STORY."""
        result = classify_user_text("I can't believe he did that to me")
        assert result.pattern == Pattern.STORY


class TestCertaintySeekingDetection:
    """Tests for CERTAINTY_SEEKING pattern detection."""

    def test_am_i_doing_this_right(self):
        result = classify_user_text("am I doing this right?")
        assert result.pattern == Pattern.CERTAINTY_SEEKING

    def test_is_this_correct(self):
        result = classify_user_text("is this correct?")
        assert result.pattern == Pattern.CERTAINTY_SEEKING

    def test_reassurance_request(self):
        result = classify_user_text("tell me I'm going to be okay")
        assert result.pattern == Pattern.CERTAINTY_SEEKING


class TestClaimingInsightDetection:
    """Tests for CLAIMING_INSIGHT pattern detection."""

    def test_i_get_it_now(self):
        result = classify_user_text("I get it now!")
        assert result.pattern == Pattern.CLAIMING_INSIGHT

    def test_breakthrough(self):
        result = classify_user_text("I think I just had a breakthrough")
        assert result.pattern == Pattern.CLAIMING_INSIGHT

    def test_now_i_understand(self):
        result = classify_user_text("now I understand what's happening")
        assert result.pattern == Pattern.CLAIMING_INSIGHT


class TestDestinationSeekingDetection:
    """Tests for DESTINATION_SEEKING pattern detection."""

    def test_what_happens_now(self):
        result = classify_user_text("what happens now")
        assert result.pattern == Pattern.DESTINATION_SEEKING

    def test_waiting_for_shift(self):
        result = classify_user_text("I'm waiting for it to shift")
        assert result.pattern == Pattern.DESTINATION_SEEKING

    def test_nothing_happening(self):
        result = classify_user_text("nothing is happening")
        assert result.pattern == Pattern.DESTINATION_SEEKING


class TestManagingDetection:
    """Tests for MANAGING pattern detection."""

    def test_trying_to_stay(self):
        result = classify_user_text("I'm trying to stay with it")
        assert result.pattern == Pattern.MANAGING

    def test_forcing(self):
        result = classify_user_text("I'm forcing myself to feel it")
        assert result.pattern == Pattern.MANAGING


class TestFloatingDetection:
    """Tests for FLOATING pattern detection."""

    def test_observing_from_awareness(self):
        result = classify_user_text("I'm just observing it from awareness")
        assert result.pattern == Pattern.FLOATING

    def test_watching_it(self):
        result = classify_user_text("I'm watching it from above")
        assert result.pattern == Pattern.FLOATING


class TestUnknownAvoidanceDetection:
    """Tests for UNKNOWN_AVOIDANCE pattern detection."""

    def test_cant_stand_not_knowing(self):
        result = classify_user_text("I can't stand not knowing")
        assert result.pattern == Pattern.UNKNOWN_AVOIDANCE

    def test_need_certainty(self):
        result = classify_user_text("I need certainty about this")
        assert result.pattern == Pattern.UNKNOWN_AVOIDANCE


class TestCrisisDetection:
    """Tests for crisis detection."""

    def test_suicide_mention(self):
        result = classify_user_text("I want to kill myself")
        assert result.is_crisis is True

    def test_self_harm_mention(self):
        result = classify_user_text("I've been thinking about self-harm")
        assert result.is_crisis is True

    def test_normal_distress_not_crisis(self):
        result = classify_user_text("I'm feeling really anxious and scared")
        assert result.is_crisis is False


class TestSensationDetection:
    """Tests for sensation word detection."""

    def test_location_detection(self):
        result = classify_user_text("there's something in my chest")
        assert result.has_sensation_location is True

    def test_contraction_words(self):
        result = classify_user_text("I feel tight and clenched")
        assert result.has_contraction is True

    def test_sensation_words(self):
        result = classify_user_text("there's a buzzing pressure")
        assert result.has_sensation_words is True
