import json
from datetime import datetime

from controller.machine import UnwindController
from controller.states import State


def main() -> None:
    ctrl = UnwindController()

    print("\nUNWIND-v1 (CLI) — Build Mode")
    print("Type 'quit' to exit.\n")

    # Required first prompt (safety warning / onboarding)
    first = ctrl.start()
    print(f"UNWIND: {first}\n")

    while True:
        # If in a wait state, the controller handles timed waits internally.
        resp = ctrl.tick_wait_states_if_needed()
        if resp is not None:
            print(f"UNWIND: {resp}\n")
            continue

        user = input("YOU: ").strip()
        if user.lower() in ("quit", "exit"):
            break

        resp = ctrl.step(user)
        print(f"UNWIND: {resp}\n")
        
        # Exit loop when session ends
        if ctrl.state == State.EXIT:
            break

    ctrl.ensure_logs_dir()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = f"logs/transcript_{ts}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(ctrl.mem.transcript, f, indent=2)

    print(f"Saved transcript to {out_path}\n")


if __name__ == "__main__":
    main()
    