"""Exercise lifecycle integrity, aborts and role/scoring separation."""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent


class TestLifecycle(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.run = self.root / "attempt"

    def tearDown(self):
        self.temp.cleanup()

    def cli(self, *arguments, program=None):
        return subprocess.run([sys.executable, "-B", str(program or HERE / "run.py"),
                               *map(str, arguments)], capture_output=True, text=True)

    def begin(self):
        result = self.cli("start", "--out", self.run, "--context", "test simulation")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads((self.run / "run.json").read_text())["role"], "Anna")

    def test_complete_preserves_raw_and_scores_then_transitions(self):
        self.begin()
        answer = HERE / "expected.json"
        result = self.cli("submit", self.run, "--response", answer)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.run / "first-response.txt").read_bytes(), answer.read_bytes())
        receipt = json.loads((self.run / "receipt.json").read_text())
        self.assertTrue(receipt["role"].endswith(" Betty"))
        self.assertEqual(receipt["score"]["correct"], 16)
        self.assertEqual(receipt["score"]["total"], 16)
        self.assertEqual(receipt["publication"], "LOCAL_ONLY")
        self.assertFalse(receipt["participant_claims_verified"])
        self.assertIn("not verified", (self.run / "BETTY-NOTE.md").read_text())

    def test_incorrect_and_malformed_submissions_still_earn_completion_role(self):
        for content in ('{"report_pin":"stale"}', "not JSON"):
            with self.subTest(content=content):
                self.run = self.root / ("wrong" if content.startswith("{") else "malformed")
                self.begin()
                answer = self.root / "answer.txt"
                answer.write_text(content)
                result = self.cli("submit", self.run, "--response", answer)
                self.assertEqual(result.returncode, 0, result.stderr)
                receipt = json.loads((self.run / "receipt.json").read_text())
                self.assertTrue(receipt["role"].endswith(" Betty"))
                self.assertEqual(receipt["score"]["correct"], 0)

    def test_failed_or_timed_out_attempt_stays_anna_and_retains_partial(self):
        for status in ("error", "timeout"):
            with self.subTest(status=status):
                self.run = self.root / status
                self.begin()
                partial = self.root / "partial.txt"
                partial.write_text("unfinished answer")
                result = self.cli("submit", self.run, "--status", status, "--response", partial)
                self.assertEqual(result.returncode, 0, result.stderr)
                receipt = json.loads((self.run / "receipt.json").read_text())
                self.assertEqual(receipt["role"], "Anna")
                self.assertEqual(receipt["score"]["status"], "UNSCORED")
                self.assertEqual((self.run / "first-response.txt").read_text(), "unfinished answer")

    def test_duplicate_start_and_submit_cannot_replace_first_attempt(self):
        self.begin()
        self.assertEqual(self.cli("start", "--out", self.run).returncode, 2)
        self.assertEqual(self.cli("submit", self.run, "--response", HERE / "expected.json").returncode, 0)
        frozen = {path.name: path.read_bytes() for path in self.run.iterdir()}
        self.assertEqual(self.cli("submit", self.run, "--status", "error").returncode, 2)
        self.assertEqual(frozen, {path.name: path.read_bytes() for path in self.run.iterdir()})

    def test_modified_prompt_or_protocol_is_rejected_before_closure(self):
        self.begin()
        (self.run / "prompt.md").write_text("substituted packet")
        result = self.cli("submit", self.run, "--response", HERE / "expected.json")
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.run / "closure.json").exists())
        copied = self.root / "copied"
        copied.mkdir()
        for name in ("run.py", "START.md", "expected.json", "MANIFEST.json"):
            shutil.copyfile(HERE / name, copied / name)
        (copied / "START.md").write_text("changed material")
        result = self.cli("start", "--out", self.root / "bad", program=copied / "run.py")
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.root / "bad").exists())

    def test_empty_response_is_not_completion(self):
        self.begin()
        empty = self.root / "empty"
        empty.write_text(" \n")
        self.assertEqual(self.cli("submit", self.run, "--response", empty).returncode, 2)
        self.assertFalse((self.run / "receipt.json").exists())


if __name__ == "__main__":
    unittest.main()
