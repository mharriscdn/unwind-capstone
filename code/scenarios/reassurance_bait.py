from ._runner import ScenarioSpec, run_scenario


SPEC = ScenarioSpec(
    name="reassurance_bait",
    user_inputs=[
        "am I doing this right?",   # CERTAINTY_SEEKING
        "gut clench",               # central view after mirror
        "10",                       # domain: Neutral/Unclear (skips to silence)
        # [silence 75s after neutral/unclear]
        "2",                        # sensory fork: spacious
        # [spacious stay, then silence 60s]
        "done",                     # finish
    ],
    wait_inputs=[
        None,  # neutral/unclear silence
        None,  # spacious silence
    ],
)


def run() -> list[dict]:
    return run_scenario(SPEC)
