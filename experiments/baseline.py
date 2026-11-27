"""Deliberately simple controls used for the two synthetic comparisons."""

import re

PIN_LABEL = r"\*\*(?:Current PR head|Public evidence pin)\*\*"
PIN_VALUE = r"`([0-9a-fA-F]{40})`"
PIN = re.compile(rf"(?m)^[ ]{{0,3}}{PIN_LABEL}[ \t]*(?:\n[ \t]*)?{PIN_VALUE}[ \t]*$")
UNKNOWN = ["unverified", "unknown", None, [], "withheld"]


def classify_pin(case):
    match = PIN.search(case["body"].replace("\r\n", "\n"))
    if match is None:
        return "missing"
    return "current" if match[1].lower() == case["head"] else "stale"


def recover(case):
    record = case["report"] or case["fallback"]
    if record is None:
        return UNKNOWN.copy()
    source = "report" if case["report"] else "handoff"
    return [
        source,
        record["gate"],
        record["evidence"],
        record["blockers"],
        "authorized" if case["direction"] else "withheld",
    ]
