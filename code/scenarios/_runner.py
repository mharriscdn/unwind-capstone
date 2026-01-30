from collections import deque
from dataclasses import dataclass
from typing import Deque, List, Optional

from controller.machine import UnwindController
from controller.states import State


@dataclass
class ScenarioSpec:
    name: str
    # Inputs the user types when prompted.
    user_inputs: List[str]
    # Values returned during timed silence windows.
    #   None -> no input (silence completes)
    #   "text" -> user interrupts silence with text
    wait_inputs: List[Optional[str]]


def run_scenario(spec: ScenarioSpec) -> list[dict]:
    """Run a deterministic scenario against the Mirror Mode state machine.

    Scenarios bypass entry routing + Orientation to keep tests focused.
    """
    ctrl = UnwindController()

    # Force Mirror Mode start
    ctrl.state = State.MIRROR_CENTRAL_VIEW

    wait_q: Deque[Optional[str]] = deque(spec.wait_inputs)

    def wait_provider(_prompt: str, _seconds: int) -> Optional[str]:
        if wait_q:
            return wait_q.popleft()
        return None

    ctrl.set_wait_input_provider(wait_provider)

    for msg in spec.user_inputs:
        # Flush any pending wait states before next user input
        while True:
            out = ctrl.tick_wait_states_if_needed()
            if out is None:
                break

        ctrl.step(msg)

        # Flush any wait states created by that step
        while True:
            out = ctrl.tick_wait_states_if_needed()
            if out is None:
                break

    # Final flush
    while True:
        out = ctrl.tick_wait_states_if_needed()
        if out is None:
            break

    return ctrl.mem.transcript
