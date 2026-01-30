from ._runner import ScenarioSpec, run_scenario


SPEC = ScenarioSpec(
    name="floating_pattern",
    user_inputs=[
        "I'm just observing it from awareness",  # FLOATING
        "gut clench",               # central view after mirror
        "8",                        # domain: Location/Spread
        "1",                        # refinement: Localized
        "localized",                # one word
        "2",                        # clench choice: I think so (forced 1/2/3)
        # [silence 75s]
        "2",                        # sensory fork: spacious
        # [spacious stay, then silence 60s]
        "done",                     # finish
    ],
    wait_inputs=[
        None,  # main silence
        None,  # spacious silence
    ],
)


def run() -> list[dict]:
    return run_scenario(SPEC)
