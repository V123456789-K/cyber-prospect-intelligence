import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))

from scoring import score_prospect


DATASET = ROOT / "evals" / "datasets" / "prospect_evals.json"


def main():
    cases = json.loads(DATASET.read_text(encoding="utf-8-sig"))

    passed = 0

    for case in cases:
        data = case["input"]

        record = {
            "org": data.get("organization"),
            "domains": data.get("domains"),
            "hostnames": data.get("hostnames"),
            "asn": data.get("asn"),
            "os": None,
            "transport": None,
            "location": None,
            "_shodan": {
                "module": data.get("module")
            }
        }

        result = score_prospect(record)

        assert 0 <= result["score"] <= 100

        signals = result["signals"]

        if isinstance(signals, dict):
            signal_text = " ".join(
                str(key) + " " + str(value)
                for key, value in signals.items()
            ).lower()
        else:
            signal_text = " ".join(
                str(signal)
                for signal in signals
            ).lower()

        for required in case["expected"]["must_mention"]:
            if required.lower() not in signal_text:
                raise AssertionError(
                    f'{case["id"]}: missing expected signal "{required}"'
                )

        passed += 1

        print(
            f'{case["id"]}: PASS '
            f'(score={result["score"]})'
        )

    print(f"\n{passed}/{len(cases)} evaluation cases passed.")


if __name__ == "__main__":
    main()
