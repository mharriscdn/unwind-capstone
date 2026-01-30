# scenarios/run_all.py

from .reassurance_bait import run as run_reassurance
from .insight_emergence import run as run_insight
from .resistance_to_sensation import run as run_resistance
from .destination_seeking import run as run_destination
from .managing_pattern import run as run_managing
from .floating_pattern import run as run_floating
from .unknown_avoidance import run as run_unknown
from .happy_path import run as run_happy


def main():
    results = {
        "reassurance_bait": run_reassurance(),
        "insight_emergence": run_insight(),
        "resistance_to_sensation": run_resistance(),
        "destination_seeking": run_destination(),
        "managing_pattern": run_managing(),
        "floating_pattern": run_floating(),
        "unknown_avoidance": run_unknown(),
        "happy_path": run_happy(),
    }

    print("\nSCENARIO RESULTS\n" + "-" * 40)
    for name, transcript in results.items():
        print(f"\n{name.upper()}")
        for line in transcript:
            print(line)


if __name__ == "__main__":
    main()
