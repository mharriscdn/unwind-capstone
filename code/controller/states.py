# controller/states.py
"""State machine states for UNWIND v2 (CLI).

Implements:
- Entry routing (Have you used UNWIND before?)
- Orientation (13 screens; non-skippable safety)
- Mirror Mode (FINAL v5)

States mirror the doc's step structure and timed containers.

v5 Changes:
- Orientation now has 13 screens (added THE CATEGORY ERROR)
- Added SPACIOUSNESS_CHECK_1 and SPACIOUSNESS_CHECK_2 (Layer 7)
- Spaciousness check triggers after 3+ successful stays, once per session
"""

from enum import Enum, auto


class State(Enum):
    # Entry routing
    ROUTE_USED_BEFORE = auto()          # YES/NO
    ROUTE_RETURNING_CHOICE = auto()     # 1 review orientation, 2 mirror

    # Orientation
    ORIENTATION_SCREEN = auto()         # show screen index 1..13

    # Mirror Mode — Step 4-8
    MIRROR_CENTRAL_VIEW = auto()        # Step 4: "What's most pressing..."
    MIRROR_DOMAIN = auto()              # Step 5: domain selection
    MIRROR_REFINEMENT = auto()          # Step 6: refinement selection
    MIRROR_ONE_WORD = auto()            # Step 7: "one word to describe it"
    
    # Mirror Mode — Step 9: Clench question (FORCED CHOICE in v4)
    MIRROR_CLENCH_CHOICE = auto()       # Step 9: forced 1/2/3 choice
    
    # Mirror Mode — Step 10: Silence
    MIRROR_SILENCE = auto()             # 60-90s silence (default 75)
    
    # Mirror Mode — Step 11: Forced Sensory Fork (v4)
    MIRROR_SENSORY_FORK = auto()        # forced 1/2/3: denser / spacious / no change
    
    # Mirror Mode — Step 12: Dense Path Layers (v4)
    DENSE_LAYER_1 = auto()              # both poles, no teaching
    DENSE_SILENCE_1 = auto()            # 60s silence
    DENSE_LAYER_2 = auto()              # curiosity (first teaching)
    DENSE_SILENCE_2 = auto()            # 60s silence
    DENSE_LAYER_3 = auto()              # mechanism clarification (earned teaching)
    DENSE_SILENCE_3 = auto()            # 60s silence
    DENSE_LAYER_4 = auto()              # "rest here" (valid terminal)
    DENSE_SILENCE_4 = auto()            # 60s silence
    DENSE_CONTINUE_OR_STOP = auto()     # offer to continue or stop
    
    # Intensity check (for overwhelm)
    MIRROR_INTENSITY_CHECK = auto()     # edge work
    INTENSITY_SILENCE = auto()          # 45s silence
    
    # Mirror Mode — Step 13: Spacious Path
    MIRROR_SPACIOUS_STAY = auto()       # "feel that spacious quality..."
    SPACIOUS_SILENCE = auto()           # 60s silence
    MIRROR_SPACIOUS_WHATS_HERE = auto() # "What's here now?"
    
    # Layer 7: Spaciousness Check (v5) — after 3+ successful stays
    SPACIOUSNESS_CHECK_1 = auto()       # "is spaciousness also present?"
    SPACIOUSNESS_CHECK_2 = auto()       # "is there a solid someone?"
    SPACIOUSNESS_SILENCE = auto()       # silence after check
    
    # Mirror Mode — Step 14: Off-app handoff & exit
    MIRROR_OFFAPP_HANDOFF = auto()      # once per session
    EXIT = auto()
