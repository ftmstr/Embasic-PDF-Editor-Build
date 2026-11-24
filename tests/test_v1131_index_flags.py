"""Real local Git fixtures: hidden index flags must not certify a clean tree."""
from pathlib import Path
import subprocess
import tempfile
import unittest

from p0_public_checkout import CheckoutFailure, checkout, verify_checkout


def git(*args, cwd=None):
    return subprocess.run(['git', *args], cwd=cwd, check=True,
                          capture_output=True, text=True).stdout.strip()


class HiddenIndexFlags(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix='embasic-v1131-')
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        source = root / 'source'
        git('init', '-b', 'main', str(source))
        git('config', 'user.name', 'Fixture', cwd=source)
        git('config', 'user.email', 'fixture@example.invalid', cwd=source)
        (source / 'file.txt').write_text('original\n', encoding='utf-8')
        git('add', 'file.txt', cwd=source)
        git('commit', '-m', 'synthetic source', cwd=source)
        self.url = source.as_uri()
        self.dest = root / 'clone'
        self.initial = checkout(self.dest, source_url=self.url, local_fixture=True)

    def verify(self):
        return verify_checkout(self.dest, expected_url=self.url, local_fixture=True)

    def hidden_change(self, flag):
        git('update-index', flag, '--', 'file.txt', cwd=self.dest)
        (self.dest / 'file.txt').write_text('modified bytes\n', encoding='utf-8')
        self.assertEqual(git('status', '--porcelain=v1', '--untracked-files=all', cwd=self.dest), '')
        self.assertNotEqual((self.dest / 'file.txt').read_bytes(), b'original\n')
        self.assertNotEqual(git('ls-files', '-v', cwd=self.dest)[0], 'H')
        with self.assertRaisesRegex(CheckoutFailure, 'index flags'):
            self.verify()

    def test_assume_unchanged_cannot_hide_modified_bytes(self):
        self.hidden_change('--assume-unchanged')

    def test_skip_worktree_cannot_hide_modified_bytes(self):
        self.hidden_change('--skip-worktree')

    def test_clean_unflagged_checkout_remains_eligible(self):
        self.assertEqual(self.verify()['status'], 'PASS')

    def test_clean_but_flagged_checkout_is_rejected(self):
        git('update-index', '--assume-unchanged', '--', 'file.txt', cwd=self.dest)
        with self.assertRaisesRegex(CheckoutFailure, 'index flags'):
            self.verify()


if __name__ == '__main__':
    unittest.main()
