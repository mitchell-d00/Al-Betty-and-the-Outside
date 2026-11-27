"""Validate committed Al Notes records and the fresh-participant navigation."""

import argparse
from html import unescape
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote

CHANNEL = "al-notes"
TEMPLATE = "0000.v00.json"
VERSION = re.compile(r"[0-9]{4}\.v[0-9]{2}\.json")
SHA = re.compile(r"[0-9a-f]{40}")
ENTRY_END = "<!-- end: participant entry -->"
REPO = "https://github.com/mitchell-d00/Al-Betty-and-the-Outside"
RECORD_ID = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9_-]*\.json")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True).stdout.strip()


def record(path, fields):
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict) and data.keys() == set(fields.split()), f"{path.name}: invalid fields")
    return data


def text(value):
    return isinstance(value, str) and bool(value.strip()) and "<" not in value[:1]


def text_list(value):
    return isinstance(value, list) and all(map(text, value))


def full_sha(value):
    return isinstance(value, str) and SHA.fullmatch(value) is not None


def pinned_version(root, path):
    name = str(path.relative_to(root))
    history = git(root, "log", "--format=%H", "HEAD", "--", name).splitlines()
    require(len(history) == 1, f"{name}: records must be committed once; use a new version or record ID")
    commit, = history
    require(git(root, "hash-object", str(path)) == git(root, "rev-parse", f"{commit}:{name}"),
            f"{name}: record differs from the pinned Git version")
    return commit


def authorization(root, path, note_path, target, ids):
    if path is None:
        return {"Betty": [], "Al": []}
    directory = f"{CHANNEL}/authorizations/"
    require(isinstance(path, str) and path.startswith(directory)
            and RECORD_ID.fullmatch(path[len(directory):]), "invalid authorization record path")
    require((root / path).is_file(), f"missing authorization record: {path}")
    pinned_version(root, root / path)
    data = record(root / path, "approved_by source note_path reviewed_commit grants")
    require(data["approved_by"] == "Mitchell" and text(data["source"]), f"{path}: missing Mitchell direction")
    require(data["note_path"] == note_path and data["reviewed_commit"] == target,
            f"{path}: stale or unrelated authorization")
    grants = data["grants"]
    require(isinstance(grants, dict) and grants.keys() == {"Betty", "Al"}, f"{path}: invalid roles")
    for items in grants.values():
        require(text_list(items) and set(items) <= ids, f"{path}: invalid advice scope")
    return grants


def validate_records(root):
    notes = {}
    for path in sorted((root / CHANNEL).glob("*.json")):
        if path.name == TEMPLATE:
            continue
        name = str(path.relative_to(root))
        require(VERSION.fullmatch(path.name) and path.name[:4] != "0000"
                and not path.name.endswith(".v00.json"), f"{name}: invalid note version")
        data = record(path, "author role reviewed_commit evidence advice open_questions authorization_source implementation_override")
        require(text(data["author"]) and data["role"] in {"Al", "Betty"}, f"{name}: invalid author or role")
        require(text_list(data["evidence"]) and data["evidence"] and text_list(data["open_questions"]),
                f"{name}: invalid evidence or questions")
        advice = data["advice"]
        require(isinstance(advice, list) and all(isinstance(item, dict) and item.keys() == {"id", "text"}
                and text(item["id"]) and text(item["text"]) for item in advice),
                f"{name}: advice may contain only an ID and proposal text; record outcomes separately")
        ids = {item["id"] for item in advice}
        require(len(ids) == len(advice), f"{name}: duplicated advice ID")
        commit = pinned_version(root, path)
        reviewed = data["reviewed_commit"]
        require(full_sha(reviewed), f"{name}: reviewed commit must be a full SHA")
        require(subprocess.run(["git", "merge-base", "--is-ancestor", reviewed, commit],
                               cwd=root, capture_output=True).returncode == 0,
                f"{name}: reviewed commit is unavailable or outside the note history")
        grants = authorization(root, data["authorization_source"], name, reviewed, ids)
        override = data["implementation_override"]
        require(override is None or (data["role"] == "Al" and text_list(override) and bool(override)),
                f"{name}: invalid Al implementation override")
        require(set(override or []) == set(grants["Al"]),
                f"{name}: Al override needs matching Mitchell authorization")
        notes[name] = (commit, reviewed, ids, grants)

    for path in sorted((root / CHANNEL / "acknowledgments").glob("*.json")):
        pinned_version(root, path)
        data = record(path, "author role note_path note_commit work_base independent_review outcomes")
        name = data["note_path"]
        require(isinstance(name, str) and name in notes, f"{path.name}: unknown note version")
        commit, reviewed, ids, grants = notes[name]
        require(data["note_commit"] == commit, f"{path.name}: stale or incorrect note commit")
        require(data["work_base"] == reviewed, f"{path.name}: stale or incorrect work base")
        role = data["role"]
        require(text(data["author"]) and role in {"Al", "Betty"} and data["independent_review"] is False,
                f"{path.name}: implementation records must label the actor and cannot claim independent review")
        require(isinstance(data["outcomes"], list) and data["outcomes"], f"{path.name}: missing outcomes")
        for item in data["outcomes"]:
            require(isinstance(item, dict) and item.keys() == {"advice_id", "status", "detail", "evidence"}
                    and text(item["advice_id"]) and item["advice_id"] in ids
                    and text(item["detail"]) and text_list(item["evidence"]), f"{path.name}: invalid outcome")
            status = item["status"]
            require(status in ("applied", "rejected", "deferred", "tested"), f"{path.name}: invalid disposition")
            if status in ("applied", "tested"):
                require(item["advice_id"] in grants[role], f"{path.name}: {status} requires Mitchell authorization")
                require(item["evidence"], f"{path.name}: {status} requires a revision or receipt")
    return len(notes)


def validate_current_note(root, name, target):
    path = Path(name)
    require(path.parent == Path(CHANNEL) and VERSION.fullmatch(path.name)
            and path.name != TEMPLATE and (root / path).is_file(), "select a committed note version")
    versions = sorted((root / CHANNEL).glob(f"{path.name[:4]}.v[0-9][0-9].json"))
    require(path.name == versions[-1].name, "stale note version; select the latest revision")
    pinned_version(root, root / path)
    require(full_sha(target) and json.loads((root / path).read_text(encoding="utf-8"))["reviewed_commit"] == target,
            "stale reviewed commit; select or write a note for this target")


def validate_navigation(root):
    routes = (
        ("README.md", ENTRY_END, {"test_x/START.md", REPO}),
        ("AGENTS.md", ENTRY_END, {"test_x/START.md"}),
        ("test_x/START.md", "## 2 · Close the first submission", set()),
        ("pilot/participant-instructions.txt", None, set()),
    )
    for path, boundary, allowed in routes:
        document = (root / path).read_text(encoding="utf-8")
        if boundary is None:
            entry = document
        else:
            require(document.count(boundary) == 1, f"{path}: missing or ambiguous participant boundary")
            entry = document.split(boundary, 1)[0]
        entry, document = unescape(entry), unescape(document)
        definitions = re.findall(r"(?m)^ {0,3}\[([^\]]+)\]:\s*<?([^\s>]+)", document)
        links = re.findall(r"\]\(\s*<?([^\s)>]+)|href\s*=\s*[\"']([^\"']+)", entry, re.IGNORECASE)
        destinations = {first or second for first, second in links}
        destinations.update(re.findall(
            r"\b(?:href|src)\s*=\s*([^\s\"'<>]+)", entry, re.IGNORECASE,
        ))
        destinations.update(re.findall(r"https?://[^\s<>)\"'`]+", entry))
        destinations.update(uri for label, uri in definitions if f"[{label}]".casefold() in entry.casefold())
        for uri in destinations:
            require(unquote(uri).rstrip("/") in allowed, f"{path}: pre-submission destination {uri}")
        require(not re.search(r"(?:al-notes/|test_x/(?:NOTES\.md|expected\.json|runs/)|"
                              r"pilot/(?:scoring-key\.json|allocation\.json|replay/)|papers/archive/)",
                              unquote(entry), re.IGNORECASE),
                f"{path}: protected route before submission")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--note", help="numbered note path to verify before work")
    parser.add_argument("--target", help="exact live source commit this work targets")
    args = parser.parse_args()
    if bool(args.note) != bool(args.target):
        parser.error("--note and --target must be supplied together")
    try:
        repo = Path(__file__).resolve().parent.parent
        validate_navigation(repo)
        count = validate_records(repo)
        if args.note:
            validate_current_note(repo, args.note, args.target)
    except (OSError, ValueError, TypeError, subprocess.CalledProcessError) as exc:
        sys.exit(f"Al Notes check failed: {exc}")
    print(f"Al Notes: {count} committed note version(s), fresh-participant routes checked")
