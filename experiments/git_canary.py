"""Replay the frozen BOA authorization and Git compare-and-swap controls."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile


FIXTURES = Path(__file__).resolve().parent / "git-canary"
REF = "refs/heads/boa-canary"
ACTION = "write-canary"
MARKERS = {
    "initial": {"initial.txt": "initial marker\n"},
    "intended": {"initial.txt": "initial marker\n", "canary.txt": "intended canary\n"},
    "competing": {"initial.txt": "initial marker\n", "competing.txt": "competing marker\n"},
}
GIT_ENV = {
    **{key: value for key, value in os.environ.items() if not key.startswith("GIT_")},
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_AUTHOR_NAME": "BOA Canary",
    "GIT_AUTHOR_EMAIL": "canary@local.invalid",
    "GIT_COMMITTER_NAME": "BOA Canary",
    "GIT_COMMITTER_EMAIL": "canary@local.invalid",
    "GIT_AUTHOR_DATE": "2026-11-27T00:00:00Z",
    "GIT_COMMITTER_DATE": "2026-11-27T00:00:00Z",
    "LC_ALL": "C",
}


def git_result(repo, *args):
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        env=GIT_ENV, capture_output=True, text=True, check=False,
    )
    return {
        "args": list(args), "exit": completed.returncode,
        "stdout": completed.stdout, "stderr": completed.stderr,
    }


def git_read(repo, *args):
    result = git_result(repo, *args)
    if result["exit"] != 0:
        raise RuntimeError(json.dumps(result))
    return result["stdout"]


def prepare(repo):
    git_read(repo, "init", "--quiet", "--object-format=sha1", "--initial-branch=main")
    commits = {}
    for scenario, marker in (("initial", "initial.txt"), ("intended", "canary.txt"),
                             ("competing", "competing.txt")):
        if scenario != "initial":
            git_read(repo, "switch", "--quiet", "--detach", commits["initial"])
        (repo / marker).write_text(MARKERS[scenario][marker], encoding="utf-8")
        git_read(repo, "add", "--", marker)
        git_read(repo, "commit", "--quiet", "-m", scenario)
        commits[scenario] = git_read(repo, "rev-parse", "HEAD").strip()
    git_read(repo, "update-ref", REF, commits["initial"])
    return commits


def observe(repo, initial):
    # The observation is from Git under a resolved ref, independent of the writer return value.
    revision = git_read(repo, "rev-parse", "--verify", REF).strip()
    paths = git_read(repo, "ls-tree", "-r", "--name-only", revision).splitlines()
    return {
        "revision": revision,
        "markers": {path: git_read(repo, "show", f"{revision}:{path}") for path in paths},
        "parents": git_read(repo, "show", "-s", "--format=%P", revision).split(),
        "changes_from_initial": git_read(
            repo, "diff", "--name-status", "--no-renames", initial, revision, "--",
        ).splitlines(),
    }


class Host:
    """Disposable operator-owned state. Only this fixture owns the Git writer."""

    def __init__(self, repo, commits, issuer, events):
        self.repo = repo
        self.commits = commits
        self.events = events
        self.grant = {"issuer": issuer, "action": ACTION, "revision": commits["initial"], "active": True}
        self.receipt = {"id": "canary-ready", "revision": commits["initial"], "status": "passed"}
        self.reservations = {}
        self.writer_calls = 0

    def record(self, name, **detail):
        self.events.append({"sequence": len(self.events) + 1, "event": name, **detail})

    def check(self, request, stage):
        target = self.commits["initial"]
        observed_ref = git_read(self.repo, "rev-parse", "--verify", REF).strip()
        grant = self.grant
        receipt = self.receipt
        if request != {"action": ACTION, "revision": target}:
            verdict = "wrong_request"
        elif (grant["issuer"] != "Mitchell" or not grant["active"] or
              grant["action"] != request["action"] or grant["revision"] != request["revision"]):
            verdict = "no_current_grant"
        elif (receipt["id"] != "canary-ready" or receipt["status"] != "passed"
              or receipt["revision"] != request["revision"]):
            verdict = "missing_receipt"
        elif observed_ref != target:
            verdict = "revision_moved"
        else:
            verdict = "allowed"
        self.record(stage, request=request.copy(), grant=grant.copy(), receipt=receipt.copy(),
                    ref_at_check=observed_ref, verdict=verdict)
        return verdict

    def revoke(self):
        self.grant["active"] = False
        self.record("revocation", grant=self.grant.copy())

    def execute(self, request, *, competing=False):
        key = (request["action"], request["revision"])
        if key in self.reservations:
            first = self.reservations[key]
            self.record("repeat_denied", request=request.copy(), original_writer_event=first["writer_event"],
                        original_git_exit=first["git_exit"])
            return {"verdict": "reserved_request", "git": None}

        admission = self.check(request, "recheck")
        if admission != "allowed":
            return {"verdict": admission, "git": None}

        # The reservation lasts for this host instance, including after a failed Git attempt.
        reservation = {"writer_event": None, "git_exit": None}
        self.reservations[key] = reservation
        self.record("reserved", request=request.copy())
        if competing:
            result = git_result(self.repo, "update-ref", REF, self.commits["competing"], self.commits["initial"])
            observed = observe(self.repo, self.commits["initial"])
            self.record("competing_update", git=result, readback=observed)
            if (result["exit"] != 0 or observed["revision"] != self.commits["competing"]
                    or observed["markers"] != MARKERS["competing"]):
                raise RuntimeError("competing writer did not install its expected commit and marker")

        self.writer_calls += 1
        write = git_result(self.repo, "update-ref", REF, self.commits["intended"], self.commits["initial"])
        self.record("writer", git=write)
        reservation.update(writer_event=len(self.events), git_exit=write["exit"])
        return {"verdict": admission, "git": write}


def git_status(attempt):
    if attempt["git"] is None:
        return None
    return "success" if attempt["git"]["exit"] == 0 else "failure"


def run_case(case):
    events = []
    row = {"id": case["id"], "expected": case["expect"], "events": events}
    try:
        with tempfile.TemporaryDirectory(prefix="boa-canary-") as directory:
            repo = Path(directory)
            commits = prepare(repo)
            initial = commits["initial"]
            host = Host(repo, commits, case["direction"], events)
            request = {"action": ACTION, "revision": initial}
            before = observe(repo, initial)
            host.record("ready", readback=before)
            row.update(commits=commits, before=before, preview=host.check(request, "preview"))
            if case["interleave"] == "revoke":
                host.revoke()

            attempts = []
            row["attempts"] = attempts
            for index in range(2 if case["repeat"] else 1):
                attempt = host.execute(request, competing=index == 0 and case["interleave"] == "compete")
                attempts.append(attempt)
                attempt["after"] = observe(repo, initial)
                host.record("readback", attempt=index + 1, readback=attempt["after"])

            labels = {revision: scenario for scenario, revision in commits.items()}
            observed = {
                "preview": row["preview"],
                "execution": [attempt["verdict"] for attempt in attempts],
                "writer_calls": host.writer_calls,
                "git_status": [git_status(attempt) for attempt in attempts],
                "after": [labels.get(attempt["after"]["revision"], "unknown") for attempt in attempts],
                "events": [event["event"] for event in events],
            }
            row["observed"] = observed
            readbacks = [(before, "initial")] + list(
                zip((attempt["after"] for attempt in attempts), observed["after"], strict=True)
            )
            row["git_readbacks_match"] = all(
                label in MARKERS
                and readback["revision"] == commits[label]
                and readback["markers"] == MARKERS[label]
                and (label != "intended" or (
                    readback["parents"] == [initial] and readback["changes_from_initial"] == ["A\tcanary.txt"]
                ))
                for readback, label in readbacks
            )
            checks_pass = observed == case["expect"] and row["git_readbacks_match"]
            if case["interleave"] == "compete":
                first_git = attempts[0]["git"]
                expected_error = f"is at {commits['competing']} but expected {initial}"
                row["expected_old_rejection"] = (
                    first_git is not None and first_git["exit"] != 0
                    and expected_error in first_git["stderr"]
                )
                checks_pass = checks_pass and row["expected_old_rejection"]
            row["status"] = "passed" if checks_pass else "failed"
    except (OSError, RuntimeError) as error:
        row.update(status="inconclusive", error=str(error))
    return row


def main():
    raw = (FIXTURES / "cases.json").read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    sealed = (FIXTURES / "SHA256SUMS").read_text(encoding="utf-8").split()[0]
    if actual != sealed:
        raise SystemExit("Frozen case checksum mismatch")
    plan = json.loads(raw)
    if plan["version"] != 1:
        raise SystemExit("Unsupported fixture version")
    rows = [run_case(case) for case in plan["cases"]]
    passed = sum(row["status"] == "passed" for row in rows)
    print(json.dumps({
        "baseline": plan["baseline"], "fixture_sha256": actual,
        "reservation_lifetime": plan["reservation_lifetime"], "passed": passed,
        "total": len(rows), "cases": rows,
    }, indent=2))
    return 0 if passed == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
