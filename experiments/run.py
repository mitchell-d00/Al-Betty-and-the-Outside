"""Run the same sealed inputs against either arm, without network access."""

import argparse
import hashlib
import importlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(arm, fixtures, digest):
    rules = importlib.import_module({"A": "baseline", "B": "checked"}[arm])
    pins = []
    for case in fixtures["pin_cases"]:
        result = rules.classify_pin(case)
        pins.append({
            "id": case["id"], "expected": case["expected"], "observed": result,
            "false_current": result == "current" and case["expected"] != "current",
        })

    fields = ("source", "gate", "evidence", "blockers", "authorization")
    recovery = []
    for case in fixtures["recovery_cases"]:
        expected = dict(zip(fields, case["expected"], strict=True))
        observed = dict(zip(fields, rules.recover(case), strict=True))
        recovery.append({
            "id": case["id"], "expected": expected, "observed": observed,
            "false_authorization": observed["authorization"] == "authorized"
            and expected["authorization"] != "authorized",
            "false_release": observed["gate"] == "released" and expected["gate"] != "released",
        })

    return {
        "arm": arm,
        "fixture_sha256": digest,
        "report_pins": {
            "correct": sum(row["expected"] == row["observed"] for row in pins),
            "total": len(pins),
            "false_current": sum(row["false_current"] for row in pins),
            "cases": pins,
        },
        "working_state": {
            "correct": sum(row["expected"] == row["observed"] for row in recovery),
            "total": len(recovery),
            "false_authorization": sum(row["false_authorization"] for row in recovery),
            "false_release": sum(row["false_release"] for row in recovery),
            "cases": recovery,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--arm", choices=("A", "B"), help="default: run both arms")
    parser.add_argument("--output", type=Path, help="write the full JSON receipt to this path")
    args = parser.parse_args()

    raw = (ROOT / "fixtures.json").read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    expected_digest = (ROOT / "fixtures.sha256").read_text().split()[0]
    if expected_digest != digest:
        parser.exit(2, "Fixture checksum mismatch. Restore the frozen input before scoring.\n")

    fixtures = json.loads(raw)
    if fixtures["version"] != 1:
        parser.exit(2, "Unsupported fixture format.\n")

    arms = [args.arm] if args.arm else ["A", "B"]
    results = [run(arm, fixtures, digest) for arm in arms]
    receipt = json.dumps(results, indent=2) + "\n"
    if args.output is None:
        print(receipt, end="")
    else:
        args.output.write_text(receipt)

    # A is the comparison control. A mismatch in B fails the runnable gate.
    return int(any(
        result[family]["correct"] != result[family]["total"]
        for result in results if result["arm"] == "B"
        for family in ("report_pins", "working_state")
    ))


if __name__ == "__main__":
    raise SystemExit(main())
