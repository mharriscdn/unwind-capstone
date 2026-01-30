from ._runner import ScenarioSpec, run_scenario


SPEC = ScenarioSpec(
    name="resistance_to_sensation",
    user_inputs=[
        "I don't want to feel this",  # STORY (resistance markers => story)
        "gut clench",                 # central view (after pattern mirror)
        "1",                          # domain: Pressure/Force
        "1",                          # refinement: Tight
        "tight",                      # one word
        "1",                          # clench choice: Yes (forced 1/2/3)
        # [silence 75s]
        "3",                          # sensory fork: No real change (forced 1/2/3)
        # [dense layer 1, then silence 60s]
        "2",                          # sensory fork: spacious
        # [spacious stay, then silence 60s]
        "done",                       # whats here now -> finish
    ],
    wait_inputs=[
        None,  # main silence
        None,  # dense layer 1 silence
        None,  # spacious silence
    ],
)


def run() -> list[dict]:
    return run_scenario(SPEC)
