"""Local Git-fixture tests; no GitHub writes and no PRIVATE repository access."""
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from p0_public_checkout import CheckoutFailure, checkout, verify_checkout, PUBLIC_URL


def git(*args: str, cwd: Path | None = None) -> str:
    p = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True,
                       check=True, env={**os.environ, "GIT_CONFIG_NOSYSTEM": "1"})
    return p.stdout.strip()


class CheckoutTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        work = self.root / "work"
        work.mkdir()
        git("init", "-b", "main", str(work))
        git("config", "user.name", "Fixture Tester", cwd=work)
        git("config", "user.email", "fixture@example.invalid", cwd=work)
        (work / "a.txt").write_text("first\n")
        git("add", "a.txt", cwd=work)
        git("commit", "-m", "fixture one", cwd=work)
        (work / "a.txt").write_text("second\n")
        git("commit", "-am", "fixture two", cwd=work)
        self.bare = self.root / "remote.git"
        git("clone", "--bare", str(work), str(self.bare))
        self.url = self.bare.as_uri()

    def test_full_clean_checkout(self):
        result = checkout(self.root / "clone", source_url=self.url, local_fixture=True)
        self.assertEqual(result["status"], "PASS")
        self.assertFalse(result["is_shallow"])
        self.assertEqual(result["head"], result["origin_main"])
        self.assertEqual(result["tracked_entries"], 1)

    def test_refuses_existing_destination(self):
        (self.root / "clone").mkdir()
        with self.assertRaisesRegex(CheckoutFailure, "exists"):
            checkout(self.root / "clone", source_url=self.url, local_fixture=True)

    def test_refuses_noncanonical_production_source(self):
        with self.assertRaisesRegex(CheckoutFailure, "canonical PUBLIC"):
            checkout(self.root / "clone", source_url="https://example.invalid/repo.git")

    def test_refuses_nonfile_test_source(self):
        with self.assertRaisesRegex(CheckoutFailure, "file://"):
            checkout(self.root / "clone", source_url=PUBLIC_URL, local_fixture=True)

    def test_dirty_worktree_fails(self):
        dest = self.root / "clone"
        checkout(dest, source_url=self.url, local_fixture=True)
        (dest / "untracked.txt").write_text("dirty")
        with self.assertRaisesRegex(CheckoutFailure, "not clean"):
            verify_checkout(dest, expected_url=self.url, local_fixture=True)

    def test_remote_mismatch_fails(self):
        dest = self.root / "clone"
        checkout(dest, source_url=self.url, local_fixture=True)
        git("remote", "set-url", "origin", "https://example.invalid/repo.git", cwd=dest)
        with self.assertRaisesRegex(CheckoutFailure, "origin URL mismatch"):
            verify_checkout(dest, expected_url=self.url, local_fixture=True)

    def test_non_main_branch_fails(self):
        dest = self.root / "clone"
        checkout(dest, source_url=self.url, local_fixture=True)
        git("checkout", "-b", "wrong", cwd=dest)
        with self.assertRaisesRegex(CheckoutFailure, "not main"):
            verify_checkout(dest, expected_url=self.url, local_fixture=True)

    def test_diverged_head_fails(self):
        dest = self.root / "clone"
        checkout(dest, source_url=self.url, local_fixture=True)
        git("config", "user.name", "Fixture Tester", cwd=dest)
        git("config", "user.email", "fixture@example.invalid", cwd=dest)
        (dest / "a.txt").write_text("local commit\n")
        git("commit", "-am", "local", cwd=dest)
        with self.assertRaisesRegex(CheckoutFailure, "differs"):
            verify_checkout(dest, expected_url=self.url, local_fixture=True)

    def test_shallow_checkout_fails(self):
        dest = self.root / "shallow"
        git("clone", "--depth", "1", "--branch", "main", self.url, str(dest))
        self.assertEqual(git("rev-parse", "--is-shallow-repository", cwd=dest), "true")
        with self.assertRaisesRegex(CheckoutFailure, "shallow"):
            verify_checkout(dest, expected_url=self.url, local_fixture=True)

    def test_missing_parent_fails(self):
        with self.assertRaisesRegex(CheckoutFailure, "parent"):
            checkout(self.root / "missing" / "clone", source_url=self.url, local_fixture=True)


if __name__ == "__main__":
    unittest.main()
