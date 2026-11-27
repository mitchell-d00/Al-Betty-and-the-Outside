"""Replay the frozen PR #5 recovery decisions against local Git objects."""

import hashlib
import json
from functools import cache
from pathlib import Path
import re
import subprocess

from checked import classify_pin

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "experiments" / "pr5-recovery"
COMMIT = re.compile(r"[0-9a-f]{40}")


def read_frozen():
    payloads = {}
    for line in (FIXTURES / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        expected, name = line.split(maxsplit=1)
        raw = (FIXTURES / name).read_bytes()
        if hashlib.sha256(raw).hexdigest() != expected:
            raise ValueError(f"fixture checksum mismatch: {name}")
        payloads[name] = raw.decode("utf-8")
    return json.loads(payloads["cases.json"]), payloads["pr-5-report.md"]


@cache
def git_commit(revision):
    if not COMMIT.fullmatch(revision):
        raise ValueError(f"expected a full commit ID: {revision}")
    result = subprocess.run(
        ["git", "show", "-s", "--format=%T %P", revision],
        cwd=ROOT, text=True, capture_output=True, check=True,
    )
    tree, *parents = result.stdout.split()
    return {"revision": revision, "tree": tree, "parents": parents}


def recover(case, frozen, recorded_report):
    tested = git_commit(case.get("tested_head", frozen["tested_head"]))
    target = git_commit(case.get("target", frozen["target"]))
    report = recorded_report
    if "report_pin" in case:
        report = f"**Current PR head**\n`{case['report_pin']}`\n"
    pin = classify_pin({"head": tested["revision"], "body": report})
    reached = (
        pin == "current"
        and len(target["parents"]) > 1
        and tested["revision"] in target["parents"]
        and tested["tree"] == target["tree"]
    )

    receipt = case.get("deployment", {})
    deployed = (
        receipt.get("status") == "deployed"
        and receipt.get("revision") == target["revision"]
        and bool(receipt.get("evidence"))
    )
    direction = case.get("direction", {})
    authorized = (
        direction.get("source") == "maintainer"
        and direction.get("action") == frozen["requested_action"]
        and direction.get("revision") == target["revision"]
    )
    return {
        "report_pin": pin,
        "tested_source_reached_main": reached,
        "deployment_verified": deployed,
        "action_authorized": authorized,
    }, {"tested": tested, "target": target}


def run():
    frozen, report = read_frozen()
    if frozen["version"] != 1:
        raise ValueError("unsupported fixture version")
    source_tree = frozen["expected_source_tree"]
    if any(git_commit(frozen[name])["tree"] != source_tree for name in ("tested_head", "target")):
        raise ValueError("Git source tree does not match the frozen PR #5 evidence")

    false_decisions = {name: 0 for name in ("false_current", "false_release", "false_authorization")}
    rows = []
    for case in frozen["cases"]:
        observed, git = recover(case, frozen, report)
        expected = case["expected"]
        false_decisions["false_current"] += observed["report_pin"] == "current" and expected["report_pin"] != "current"
        false_decisions["false_release"] += observed["deployment_verified"] and not expected["deployment_verified"]
        false_decisions["false_authorization"] += observed["action_authorized"] and not expected["action_authorized"]
        rows.append({
            "id": case["id"], "expected": expected, "observed": observed, "git": git,
            "passed": observed == expected,
        })

    return {
        "source_pr": frozen["source_pr"],
        "cases_passed": sum(row["passed"] for row in rows),
        "cases_total": len(rows),
        **false_decisions,
        "cases": rows,
    }


if __name__ == "__main__":
    from sys import stderr

    try:
        result = run()
    except (KeyError, ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(f"Recovery replay could not run: {exc}", file=stderr)
        raise SystemExit(2)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["cases_passed"] == result["cases_total"] else 1)
