from ._runner import ScenarioSpec, run_scenario


SPEC = ScenarioSpec(
    name="destination_seeking",
    user_inputs=[
        "what happens now",     # should be mirrored as DESTINATION_SEEKING
        "gut clench",           # central view after mirror
        "9",                    # domain: Intensity
        "7",                    # refinement: Steady
        "tight",                # one word
        "1",                    # clench choice: Yes (forced 1/2/3)
        # [silence 75s]
        "3",                    # sensory fork: No real change
        # [dense layer 1, then silence 60s]
        "2",                    # sensory fork: spacious
        # [spacious stay, then silence 60s]
        "done",                 # finish
    ],
    wait_inputs=[
        None,  # main silence
        None,  # dense layer 1 silence
        None,  # spacious silence
    ],
)


def run() -> list[dict]:
    return run_scenario(SPEC)

