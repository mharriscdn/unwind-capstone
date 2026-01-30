from ._runner import ScenarioSpec, run_scenario


SPEC = ScenarioSpec(
    name="insight_emergence",
    user_inputs=[
        "I get it now!",            # CLAIMING_INSIGHT
        "gut clench",               # central view after mirror
        "9",                        # domain: Intensity
        "7",                        # refinement: Steady
        "tight",                    # one word
        "1",                        # clench choice: Yes (forced 1/2/3)
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
