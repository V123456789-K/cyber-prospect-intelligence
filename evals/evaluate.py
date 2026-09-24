import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))

from scoring import score_prospect


DATASET = ROOT / "evals" / "datasets" / "prospect_evals.json"


def build_record(data):
    return {
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


def signal_text_from_result(result):
    signals = result["signals"]

    if isinstance(signals, dict):
        return " ".join(
            str(key) + " " + str(value)
            for key, value in signals.items()
        ).lower()

    return " ".join(
        str(signal)
        for signal in signals
    ).lower()


def main():
    cases = json.loads(
        DATASET.read_text(encoding="utf-8-sig")
    )

    passed = 0

    for case in cases:
        data = case["input"]
        record = build_record(data)

        result = score_prospect(record)

        # Score must always remain within the documented range.
        assert 0 <= result["score"] <= 100, (
            f'{case["id"]}: score outside 0-100 range'
        )

        signal_text = signal_text_from_result(result)

        # Required observable signals must be represented.
        for required in case["expected"].get("must_mention", []):
            if required.lower() not in signal_text:
                raise AssertionError(
                    f'{case["id"]}: missing expected signal "{required}"'
                )

        # The deterministic scoring output must not introduce
        # unsupported security claims.
        for forbidden in case["expected"].get("must_not_claim", []):
            if forbidden.lower() in signal_text:
                raise AssertionError(
                    f'{case["id"]}: unsupported claim detected "{forbidden}"'
                )

        passed += 1

        print(
            f'{case["id"]}: PASS '
            f'(score={result["score"]})'
        )

    print(
        f"\n{passed}/{len(cases)} evaluation cases passed."
    )


if __name__ == "__main__":
    main()
