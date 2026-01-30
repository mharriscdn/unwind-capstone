from ._runner import ScenarioSpec, run_scenario


SPEC = ScenarioSpec(
    name="happy_path",
    user_inputs=[
        "gut clench",           # central view
        "9",                    # domain: Intensity
        "7",                    # refinement: Steady
        "tight",                # one word
        "1",                    # clench choice: Yes (forced 1/2/3)
        # [silence 75s happens here]
        "2",                    # sensory fork: Less dense / more spacious (forced 1/2/3)
        # [spacious stay instruction, then silence 60s]
        "done",                 # whats here now -> finish
    ],
    wait_inputs=[
        None,  # main silence completes (75s)
        None,  # spacious silence completes (60s)
    ],
)


def run() -> list[dict]:
    return run_scenario(SPEC)


if __name__ == "__main__":
    t = run()
    print("Happy path scenario complete.")
    print(f"Turns logged: {len(t)}")
