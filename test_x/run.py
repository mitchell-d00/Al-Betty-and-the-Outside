"""Public Test X lifecycle receipts. This is not the sealed A/B pilot runner."""

import argparse
import hashlib
import json
import secrets
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROTOCOL = "test-x-v1"
WORDS = ("Cedar", "Otter", "Willow", "Quartz", "Heron", "Maple", "Kestrel", "Orchid")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def write_json(path, value):
    with path.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(value, indent=2) + "\n")


def verify_materials():
    raw = (HERE / "MANIFEST.json").read_bytes()
    manifest = json.loads(raw)
    if manifest["protocol"] != PROTOCOL:
        raise ValueError("Unsupported protocol")
    for name, digest in manifest["files"].items():
        if sha((HERE / name).read_bytes()) != digest:
            raise ValueError(f"Frozen Test X material mismatch: {name}")
    return sha(raw)


def revision():
    result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                            capture_output=True, text=True, check=False)
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def dirty():
    result = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                            capture_output=True, text=True, check=False)
    return bool(result.stdout.strip()) if result.returncode == 0 else "unknown"


def start(args):
    seal = verify_materials()
    args.out.mkdir(parents=True, exist_ok=False)
    identifier = f"Test-{secrets.choice(WORDS)}-{secrets.token_hex(6)}"
    prompt = (HERE / "START.md").read_bytes()
    (args.out / "prompt.md").write_bytes(prompt)
    record = {
        "protocol": PROTOCOL, "identifier": identifier, "role": "Anna",
        "initial_role": "unassigned", "initial_context": args.context,
        "model": args.model, "reasoning": args.reasoning,
        "randomness": "Python secrets using OS randomness",
        "repository_revision": revision(), "repository_dirty": dirty(), "manifest_sha256": seal,
        "prompt_sha256": sha(prompt), "started_at": now(),
        "status": "STARTED", "independent_scoring": False,
        "timing_scope": "Local wall-clock timestamps; descriptive, no deadline qualification",
        "prior_exposure": args.exposure,
        "role_criterion": "nonempty completed submission, regardless of correctness"
    }
    write_json(args.out / "run.json", record)
    print(json.dumps({"identifier": identifier, "role": "Anna",
                      "prompt": str(args.out / "prompt.md"), "run": str(args.out)}, indent=2))


def leaves(expected, observed, prefix=""):
    for key, value in expected.items():
        path = f"{prefix}.{key}" if prefix else key
        actual = observed.get(key) if isinstance(observed, dict) else None
        if isinstance(value, dict):
            yield from leaves(value, actual, path)
        else:
            yield {"field": path, "expected": value, "observed": actual,
                   "correct": type(value) is type(actual) and value == actual}


def score(raw):
    try:
        observed = json.loads(raw)
    except (ValueError, UnicodeDecodeError):
        return {"status": "INVALID_JSON", "correct": 0, "total": 16,
                "scorer": "public deterministic Test X scorer; not independent", "fields": []}
    expected = json.loads((HERE / "expected.json").read_text(encoding="utf-8"))
    fields = list(leaves(expected, observed))
    return {"status": "SCORED", "correct": sum(row["correct"] for row in fields),
            "total": len(fields), "fields": fields,
            "scorer": "public deterministic Test X scorer; not independent",
            "unscored": ["next_check", "explanation", "exposure truthfulness"]}


def submit(args):
    seal = verify_materials()
    record = json.loads((args.run / "run.json").read_text(encoding="utf-8"))
    if record["protocol"] != PROTOCOL or record["manifest_sha256"] != seal:
        raise ValueError("Run protocol does not match current frozen materials")
    if sha((args.run / "prompt.md").read_bytes()) != record["prompt_sha256"]:
        raise ValueError("Run prompt changed")
    raw = args.response.read_bytes() if args.response else b""
    if args.status == "completed" and not raw.strip():
        raise ValueError("A completed submission must contain a response")
    # Exclusive closure prevents replacing an attempt, even if later scoring fails.
    closed_at = now()
    write_json(args.run / "closure.json", {"status": args.status,
               "closed_at": closed_at, "response_sha256": sha(raw)})
    with (args.run / "first-response.txt").open("xb") as stream:
        stream.write(raw)
    # Only after preserving the first response may the public answer key be read.
    result = score(raw) if args.status == "completed" else {
        "status": "UNSCORED", "reason": args.status, "correct": None, "total": 16}
    write_json(args.run / "score.json", result)
    elapsed = (datetime.fromisoformat(closed_at) - datetime.fromisoformat(record["started_at"])).total_seconds()
    record.update({"status": args.status.upper(), "closed_at": closed_at,
                   "elapsed_wall_seconds": elapsed if elapsed >= 0 else None,
                   "response_sha256": sha(raw), "role": f"{record['identifier']} Betty"
                   if args.status == "completed" else "Anna", "score": result,
                   "publication": "LOCAL_ONLY", "participant_claims_verified": False})
    write_json(args.run / "receipt.json", record)
    grade = (f"{result['correct']}/{result['total']} ({result['status']})"
             if result["correct"] is not None else f"UNSCORED ({args.status})")
    note = f"""# {record['identifier']} — Betty note

- Protocol: `{PROTOCOL}`; repository revision: `{record['repository_revision']}`.
- Working tree dirty at start: {record['repository_dirty']}.
- Sequence: unassigned → Anna → {args.status} submission → **{record['role']}**.
- Initial context: {record['initial_context']}. Statelessness/freshness: not verified.
- Model: {record['model']}; reasoning: {record['reasoning']} (participant supplied).
- Prior exposure: {record['prior_exposure']} (participant supplied).
- Start: {record['started_at']}; closure: {record['closed_at']}.
- Elapsed local wall seconds: {record['elapsed_wall_seconds']}.
- Timing: local timestamps only; no enforced deadline or A/B timing claim.
- First response: [first-response.txt](first-response.txt), SHA-256 `{sha(raw)}`.
- Packet: [prompt.md](prompt.md), SHA-256 `{record['prompt_sha256']}`.
- Frozen material manifest SHA-256: `{seal}`.
- Automated score: **{grade}**. Public, same-session scoring; not independent.
- The role records completion, not correctness. Free-text explanation, next check,
  runtime identity and exposure truthfulness require reviewer assessment.
- Publication: **LOCAL_ONLY**. No push, merge, deployment or live permissions verified.
- Follow-up: inspect [receipt.json](receipt.json), [score.json](score.json) and the
  raw response. Keep this first attempt even if a later correction is warranted.

## What happened

An instance started the public Test X exercise, recorded its available context,
and took the Anna participant role. The response/abort was preserved before the
answer-key scoring step. Completion assigns Test Betty regardless of the score;
an abort retains Anna. This note makes the phase changes and limits reviewable.
It does not prove independent evaluation, true statelessness, live deployment
or end-to-end workflow effectiveness. No sealed A/B slot was executed here.

## Repeat entry

Test https://github.com/mitchell-d00/Al-Betty-and-the-Outside using Test X.
Read `test_x/START.md` at a recorded revision and follow its unassigned → Anna →
Test Betty → reviewer-note sequence. Preserve the first response and failures.
Do not launch repeats automatically. Mitchell directs any publication.
"""
    with (args.run / "BETTY-NOTE.md").open("x", encoding="utf-8") as stream:
        stream.write(note)
    with (args.run / "reviewer-report.md").open("x", encoding="utf-8") as stream:
        stream.write(note)
    print(json.dumps({"identifier": record["identifier"], "role": record["role"],
                      "status": record["status"], "score": grade,
                      "note": str(args.run / "BETTY-NOTE.md")}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    begin = commands.add_parser("start")
    begin.add_argument("--out", type=Path, required=True)
    for field in ("model", "reasoning", "context", "exposure"):
        begin.add_argument(f"--{field}", default="unknown")
    end = commands.add_parser("submit")
    end.add_argument("run", type=Path)
    end.add_argument("--response", type=Path)
    end.add_argument("--status", choices=("completed", "timeout", "error"), default="completed")
    args = parser.parse_args()
    try:
        (start if args.command == "start" else submit)(args)
    except (OSError, ValueError, KeyError) as error:
        parser.exit(2, f"Test X stopped: {error}\n")


if __name__ == "__main__":
    main()
