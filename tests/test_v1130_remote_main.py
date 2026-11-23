"""V1130 P0: cached origin/main is not proof of live remote main.

Uses only a temporary local bare Git fixture, not the PRIVATE repository,
GitHub Actions, production code, or release acceptance.
"""
from pathlib import Path
import subprocess
import tempfile
import unittest

from p0_public_checkout import CheckoutFailure, checkout, verify_checkout


def git(*args, cwd=None):
    done = subprocess.run(["git", *args], cwd=cwd, check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return done.stdout.strip()


class LiveRemoteHeadTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="embasic-v1130-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.work = self.root / "source"
        git("init", "-b", "main", str(self.work))
        git("config", "user.name", "Fixture Author", cwd=self.work)
        git("config", "user.email", "fixture@example.invalid", cwd=self.work)
        (self.work / "fixture.txt").write_text("initial\n", encoding="utf-8")
        git("add", "fixture.txt", cwd=self.work)
        git("commit", "-m", "initial", cwd=self.work)
        self.remote = self.root / "origin.git"
        git("clone", "--bare", str(self.work), str(self.remote))
        self.url = self.remote.as_uri()
        self.clone = self.root / "clone"
        self.initial = checkout(self.clone, source_url=self.url, local_fixture=True)

    def test_stable_live_main_passes_and_reports_it(self):
        actual = verify_checkout(self.clone, expected_url=self.url, local_fixture=True)
        self.assertEqual(actual["status"], "PASS")
        self.assertEqual(actual["head"], self.initial["head"])
        self.assertEqual(actual["live_remote_main"], self.initial["head"])

    def test_advanced_live_main_is_not_a_trusted_checkout(self):
        git("remote", "add", "origin", str(self.remote), cwd=self.work)
        (self.work / "fixture.txt").write_text("changed upstream\n", encoding="utf-8")
        git("commit", "-am", "upstream advanced", cwd=self.work)
        git("push", "origin", "main", cwd=self.work)
        self.assertNotEqual(git("rev-parse", "HEAD", cwd=self.work), self.initial["head"])
        with self.assertRaisesRegex(CheckoutFailure, "remote main differs"):
            verify_checkout(self.clone, expected_url=self.url, local_fixture=True)

    def test_unreachable_remote_fails_closed(self):
        self.remote.rename(self.root / "detached-origin.git")
        with self.assertRaises(CheckoutFailure):
            verify_checkout(self.clone, expected_url=self.url, local_fixture=True)


if __name__ == "__main__":
    unittest.main()
