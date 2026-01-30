# UNWIND v3: What Changed

## V3.1 FIXES (User Testing Feedback)

### Fix 1: Orientation Screens — Consistent Input Format
All orientation screens now use "Type YES to continue" instead of mixed "[Continue]" / "[Next]" / "Type YES".

### Fix 2: Story Detection — Narrative Markers
Added NARRATIVE_MARKERS to catch story/venting even when emotion words are present:
- "my boss is getting on my nerves and I am so angry" → now correctly detected as STORY
- Detects references to other people: "my boss", "my wife", "he said", etc.
- Detects situational descriptions: "at work", "yesterday", "happened", etc.

### Fix 3: Spacious Path — Direct to Silence
After sensory fork choice "less dense / more spacious":
- OLD: showed message, waited for user acknowledgment, then silence
- NEW: shows message, goes directly to silence (like clench path)
- After silence, asks "What's here now?"

---

## TEST SUITE (For Capstone)

### Running Tests
```bash
cd unwind_v2
pip install pytest pytest-cov
python -m pytest tests/ -v --cov=controller --cov=language --cov-report=term-missing
```

### Test Coverage: 72%
- **60 tests total**
- `test_classifier.py` — 27 tests for escape pattern detection
- `test_machine.py` — 33 tests for state machine behavior

### Test Categories
| Category | Tests | What's Covered |
|----------|-------|----------------|
| Story Detection | 6 | Narrative markers, emotion+context, venting |
| Pattern Detection | 14 | All 8 escape patterns |
| Crisis Handling | 3 | Suicide/self-harm detection |
| Entry Routing | 4 | New vs returning user flow |
| Orientation | 4 | Screen count, safety gate, flow |
| Mirror Mode | 7 | Pattern mirroring, sensation tree |
| Sensation Tree | 5 | Domain/refinement selection |
| Clench Path | 3 | Yes/think so/not sure branching |
| Sensory Fork | 3 | Dense/spacious/no change routing |
| Dense Layers | 1 | Layer progression through 4 stages |
| Spaciousness Check | 2 | Trigger conditions, once-per-session |
| Session End | 3 | Done/quit handling, offapp handoff |

---

## Alignment Update

Aligned to:
- Orientation_FINAL_v4.docx (13 screens now)
- Mirror_Mode_FINAL_v5.docx (with Layer 7: Spaciousness Check)
- QA_FINAL_v5.docx
- Chapter 15 (two-switch awakening structure)

---

## V3 CHANGES (from V2)

### 1. Orientation: Added "The Category Error" Screen

New Screen 3: **"Why This Exists"**

> The nervous system is applying protective logic to internal sensations as if they were physical threats.
> That's the category error. The rules of being hit are being applied where nothing can be hit.

This names the core insight upfront, matching the book's introduction.

---

### 2. Orientation: Expanded "What Actually Changes Things" (Screen 11)

Added the two-switch insight at the end:

> And sometimes, after repeated contact, something else becomes obvious: while contraction is happening, spaciousness is also present. Not after the contraction. Not instead of it. At the same time.
>
> You're spacious while contracted.
>
> When you notice that, you might also notice: there's no solid someone sitting with the contraction. Just experience happening. Contraction and awareness of contraction — but no one in between.
>
> That's not something to seek. It's what reveals itself when you stop running.

---

### 3. Mirror Mode: Layer 7 — Spaciousness Check

**When it triggers:**
- After 3+ successful stays (user chose "less dense / more spacious" on sensory fork)
- Only once per session (flag prevents repeat)
- Not in early practice — only after fear/urgency has dropped

**Prompt sequence:**

First prompt:
```
As you stay with the density... is spaciousness also present right now?
Not after the contraction — but with it?

1) Yes, both are here
2) Only contraction
3) Not sure
```

If answer is 1 (yes, both):
```
Is there a solid someone feeling this — or is sensation just happening?
```

Then: silence. No follow-up. No validation. Let them sit with whatever they noticed.

If answer is 2 or 3:
```
That's fine. Stay with what's here.
```
→ Back to silence

**Critical design principles:**
- Do NOT explain what they should see
- Do NOT confirm or validate any answer
- Do NOT turn this into teaching
- If they see it, they see it. If they don't, nothing breaks.

---

### 4. Screen 13 Updated

Added reference to spaciousness check in "What Happens Next":
> After repeated contact, check if spaciousness is present while contracted

---

## STATES ADDED

| State | Purpose |
|-------|---------|
| `SPACIOUSNESS_CHECK_1` | "Is spaciousness also present?" forced choice |
| `SPACIOUSNESS_CHECK_2` | "Is there a solid someone?" question |
| `SPACIOUSNESS_SILENCE` | Silence after the check |

---

## SESSION MEMORY ADDED

| Field | Purpose |
|-------|---------|
| `successful_stays_count` | Tracks how many times user reported reduced intensity |
| `spaciousness_check_done` | Prevents repeating the check (once per session) |

---

## ALIGNMENT WITH BOOK

The two-switch structure from Chapter 15 is now present:

1. **Switch 1: Unhittable** (category error) — Fear drops when you see nothing internal can be hit
2. **Switch 2: No sitter** — Preference drops when you see there's no one whose job it is to sit correctly

Both are now planted in orientation and available in late-stage practice.

---

## PREVIOUS CHANGES (V2 FIXES)

### Clench Question → Forced 1/2/3 Choice

```
1) Yes
2) I think so
3) Not sure / unclear
```

### Sensory Fork → Forced 1/2/3 Choice

```
1) More dense / tighter
2) Less dense / more spacious
3) No real change
```

### Dense Path: 4 Layers with Earned Teaching

| Layer | Teaching |
|-------|----------|
| 1 | None — "feel both poles" |
| 2 | Curiosity — "density isn't a problem" |
| 3 | Mechanism — "all bark, no bite" |
| 4 | Rest here — "from Bullshit Valley to what's actually here" |

---

## KEY PRINCIPLE

**The "who sits with it" insight cannot be taught. It can only be noticed.**

The app's job is to create conditions where the question can arise naturally — after enough contact, after enough successful stays, after fear has quieted. Then ask once, lightly, and let them see whatever they see.
