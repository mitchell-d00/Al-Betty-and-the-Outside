"""Regression controls for Al Notes and pre-submission navigation."""

import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest

from check_al_notes import REPO, validate_current_note, validate_navigation, validate_records


class AlNotes(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.git("init", "--quiet")
        self.commit()
        self.source = self.git("rev-parse", "HEAD")
        self.note = "al-notes/0001.v01.json"
        self.direction = "al-notes/authorizations/d001.json"
        self.ack = "al-notes/acknowledgments/a001.json"

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, check=True,
                              capture_output=True, text=True).stdout.strip()

    def commit(self):
        self.git("add", "-A")
        self.git("-c", "user.name=Test", "-c", "user.email=test@local.invalid",
                 "-c", "commit.gpgSign=false", "commit", "--quiet", "--allow-empty", "-m", "fixture")

    def write(self, path, data):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(data if isinstance(data, str) else json.dumps(data), encoding="utf-8")

    def note_with(self, **changes):
        self.write(self.note, {
            "author": "Reviewer", "role": "Al", "reviewed_commit": self.source,
            "evidence": ["pinned receipt"], "advice": [{"id": "a1", "text": "Try a test"}],
            "open_questions": [], "authorization_source": None,
            "implementation_override": None, **changes,
        })
        self.commit()
        return self.git("rev-parse", "HEAD")

    def grant(self, role="Betty", **changes):
        self.write(self.direction, {
            "approved_by": "Mitchell", "source": "maintainer message 1",
            "note_path": self.note, "reviewed_commit": self.source,
            "grants": {"Betty": ["a1"] if role == "Betty" else [], "Al": ["a1"] if role == "Al" else []},
            **changes,
        })

    def acknowledge(self, note_commit, status="applied", **changes):
        self.write(self.ack, {
            "author": "Implementer", "role": "Betty", "note_path": self.note, "note_commit": note_commit,
            "work_base": self.source, "independent_review": False,
            "outcomes": [{"advice_id": "a1", "status": status, "detail": "Disposition", "evidence": ["receipt"]}],
            **changes,
        })
        self.commit()

    def test_exact_authorized_acknowledgment_and_historical_version(self):
        self.grant()
        old_pin = self.note_with(authorization_source=self.direction)
        self.acknowledge(old_pin)
        self.note = "al-notes/0001.v02.json"
        self.note_with()
        self.assertEqual(validate_records(self.root), 2)

    def test_stale_acknowledged_revision_and_work_base_are_rejected(self):
        self.grant()
        pin = self.note_with(authorization_source=self.direction)
        self.acknowledge(self.source)
        with self.assertRaisesRegex(ValueError, "stale or incorrect note commit"):
            validate_records(self.root)
        (self.root / self.ack).unlink()
        self.ack = "al-notes/acknowledgments/a002.json"
        self.acknowledge(pin, work_base=pin)
        with self.assertRaisesRegex(ValueError, "stale or incorrect work base"):
            validate_records(self.root)

    def test_preflight_rejects_superseded_versions_and_changed_targets(self):
        self.note_with()
        first_version = self.note
        self.note = "al-notes/0001.v02.json"
        second_pin = self.note_with()
        validate_current_note(self.root, self.note, self.source)
        with self.assertRaisesRegex(ValueError, "stale note version"):
            validate_current_note(self.root, first_version, self.source)
        with self.assertRaisesRegex(ValueError, "stale reviewed commit"):
            validate_current_note(self.root, self.note, second_pin)

    def test_authorization_file_is_required_when_cited(self):
        self.note_with(authorization_source=self.direction)
        with self.assertRaisesRegex(ValueError, "missing authorization record"):
            validate_records(self.root)

    def test_unrelated_authorization_target_is_rejected(self):
        self.grant(reviewed_commit="a" * 40)
        self.note_with(authorization_source=self.direction)
        with self.assertRaisesRegex(ValueError, "stale or unrelated authorization"):
            validate_records(self.root)

    def test_advice_cannot_mark_itself_applied(self):
        self.note_with(advice=[{"id": "a1", "text": "Try a test", "status": "applied"}])
        with self.assertRaisesRegex(ValueError, "record outcomes separately"):
            validate_records(self.root)

    def test_acknowledgment_cannot_apply_unapproved_advice(self):
        pin = self.note_with()
        self.acknowledge(pin)
        with self.assertRaisesRegex(ValueError, "applied requires Mitchell authorization"):
            validate_records(self.root)

    def test_unauthorized_advice_can_be_deferred(self):
        self.acknowledge(self.note_with(), "deferred")
        self.assertEqual(validate_records(self.root), 1)

    def test_al_may_implement_only_with_explicit_override_and_no_independence(self):
        self.grant("Al")
        pin = self.note_with(authorization_source=self.direction, implementation_override=["a1"])
        self.acknowledge(pin, role="Al")
        self.assertEqual(validate_records(self.root), 1)
        self.ack = "al-notes/acknowledgments/a002.json"
        self.acknowledge(pin, role="Al", independent_review=True)
        with self.assertRaisesRegex(ValueError, "cannot claim independent review"):
            validate_records(self.root)

    def test_al_override_without_matching_grant_is_rejected(self):
        self.note_with(implementation_override=["a1"])
        with self.assertRaisesRegex(ValueError, "Al override needs matching"):
            validate_records(self.root)

    def test_protected_material_is_detected_only_on_the_fresh_route(self):
        boundary = "<!-- end: participant entry -->"
        self.write("README.md", f"{REPO}\n{boundary}\n[Notes](al-notes/README.md)")
        self.write("AGENTS.md", f"[Start](test_x/START.md)\n{boundary}\n[Notes](al-notes/README.md)")
        self.write("test_x/START.md", "Begin\n## 2 · Close the first submission\n[Archive](NOTES.md)")
        self.write("pilot/participant-instructions.txt", "Use only the assigned packet.")
        validate_navigation(self.root)
        for link in (
            "[Notes](al-notes/README.md)", "[Scores][prior]\n" + boundary + "\n[prior]: test_x/expected.json",
            "<a href=pilot/scoring-key.json>key</a>", "`test_x/expected.json`",
        ):
            with self.subTest(link=link):
                self.write("README.md", link if boundary in link else f"{link}\n{boundary}")
                with self.assertRaisesRegex(ValueError, "pre-submission destination|protected route"):
                    validate_navigation(self.root)
