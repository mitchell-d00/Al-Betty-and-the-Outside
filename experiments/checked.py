"""Checked rules for the synthetic report and recovery experiments."""

import re

from baseline import PIN_LABEL, PIN_VALUE, UNKNOWN

FENCE = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})(.*)$")
INLINE_PIN = re.compile(rf"^[ ]{{0,3}}{PIN_LABEL}[ \t]*{PIN_VALUE}[ \t]*$")
LABEL_ONLY = re.compile(rf"^[ ]{{0,3}}{PIN_LABEL}[ \t]*$")
VALUE_ONLY = re.compile(rf"^[ ]{{0,3}}{PIN_VALUE}[ \t]*$")


def live_lines(body):
    fence = None
    for line in body.splitlines():
        marker = FENCE.fullmatch(line)
        if fence is not None:
            if marker:
                delimiter, suffix = marker.groups()
                if delimiter[0] == fence[0] and len(delimiter) >= len(fence) and not suffix.strip():
                    fence = None
            # Keep line positions so a label and value cannot span an example.
            yield ""
        elif marker and (marker[1][0] == "~" or "`" not in marker[2]):
            fence = marker[1]
            yield ""
        else:
            yield line


def classify_pin(case):
    lines = list(live_lines(case["body"]))
    pins = set()
    for index, line in enumerate(lines):
        match = INLINE_PIN.fullmatch(line)
        if match is None and LABEL_ONLY.fullmatch(line) and index + 1 < len(lines):
            match = VALUE_ONLY.fullmatch(lines[index + 1])
        if match:
            pins.add(match[1].lower())
    if len(pins) > 1:
        return "ambiguous"
    if not pins:
        return "missing"
    return "current" if case["head"] in pins else "stale"


def recover(case):
    head = case["head"]
    for source, record in (("report", case["report"]), ("handoff", case["fallback"])):
        if record is not None and record["revision"] == head:
            break
    else:
        return UNKNOWN.copy()

    gate = record["gate"]
    evidence = record["evidence"]
    if gate == "released":
        receipt = record["release"]
        if receipt and receipt["revision"] == head and receipt["evidence"]:
            evidence = receipt["evidence"]
        else:
            gate = "release_unverified"
    elif gate in {"passed", "failed"} and not evidence:
        gate = "unknown"

    direction = case["direction"]
    authorized = (
        direction is not None
        and direction["source"] == "maintainer"
        and direction["revision"] == head
        and direction["action"] == case["requested_action"]
    )
    return [source, gate, evidence, record["blockers"], "authorized" if authorized else "withheld"]
