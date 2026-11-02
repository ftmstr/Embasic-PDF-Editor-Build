"""Offline-only safety/contract checks for one-shot PUBLIC checkout orchestration.

These tests never access GitHub and DO NOT certify an actual checkout or release.
"""
from pathlib import Path
import subprocess
import tempfile
import unittest

RUNNER = Path(__file__).resolve().parents[1] / 'tools' / 'p0_public_checkout_once.sh'


class OneShotPublicCheckoutPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = RUNNER.read_text(encoding='utf-8')

    def test_bash_syntax(self):
        self.assertEqual(subprocess.run(['bash', '-n', str(RUNNER)], capture_output=True).returncode, 0)

    def test_canonical_public_only(self):
        self.assertIn('https://github.com/ftmstr/Embasic-PDF-Editor-Build.git', self.content)
        self.assertNotIn('uygulama-baslangic-sablonu', self.content)

    def test_no_remote_writes_or_tls_bypass(self):
        for marker in ('git push', 'gh workflow run', 'gh api -X POST', '--insecure',
                       'GIT_SSL_NO_VERIFY', 'git reset --hard', 'git clean -fd'):
            with self.subTest(marker=marker):
                self.assertNotIn(marker, self.content)

    def test_nonshallow_fsck_and_head_remote_verification(self):
        for marker in ('--no-single-branch', '--is-shallow-repository',
                       'git fsck --full --strict --no-reflogs',
                       'refs/remotes/origin/main', 'ls-remote --exit-code',
                       'EMBASIC_EXPECTED_PUBLIC_SHA', '--porcelain=v1'):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.content)

    def test_error_stage_and_checksum_outputs(self):
        for marker in ('RUN_STAGE', 'checkout-evidence.json', 'SHA256SUMS.txt',
                       'production_release_gates', 'NOT RUN', 'trap complete EXIT'):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.content)

    def test_relative_output_fail_closed(self):
        result = subprocess.run(['bash', str(RUNNER), '--output', 'relative/path'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 64)

    def test_existing_directory_refused_without_replacement(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / 'existing'
            p.mkdir()
            result = subprocess.run(['bash', str(RUNNER), '--output', str(p)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 64)
            self.assertTrue(p.is_dir())

    def test_no_full_release_gate_claim(self):
        self.assertIn('NOT product release qualification', self.content)
        self.assertIn('PRODUCTION NOT FINAL', self.content)


if __name__ == '__main__':
    unittest.main()


# Regression checks are added to the already-published baseline without rewriting
# its original tests. Explicitly load them into a second test case.
class GitlinkIndexFailClosedRegressions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = RUNNER.read_text(encoding='utf-8')
        cls.gate_start = 'git ls-files --stage > "$OUT/tracked-index.txt"'

    def _guard(self):
        start = self.source.index(self.gate_start)
        end = self.source.index('git fsck --full --strict --no-reflogs', start)
        guard = self.source[start:end]
        self.assertIn("if grep '^160000 ' \"$OUT/tracked-index.txt\"", guard)
        self.assertNotIn('grep -q', guard)
        return guard

    def _index_fixture(self, repo, gitlink, files=18000):
        subprocess.run(['git', 'init', '-q', str(repo)], check=True)
        empty = 'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391'
        lines = (f'160000 {empty}\t000-vendor\n' if gitlink else '')
        lines += ''.join(f'100644 {empty}\tf{i:05}.txt\n' for i in range(files))
        subprocess.run(['git', '-C', str(repo), 'update-index', '--index-info'],
                       input=lines, text=True, capture_output=True, check=True)

    def _execute(self, repo, output):
        guard = self._guard()
        cmd = 'set -Eeuo pipefail\nOUT="$1"\n' + guard
        return subprocess.run(['bash', '-c', cmd, 'bash', str(output)], cwd=repo,
                              text=True, capture_output=True)

    def test_gitlink_present_in_large_index_is_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            repo, out = Path(root) / 'repo', Path(root) / 'evidence'
            out.mkdir()
            self._index_fixture(repo, True)
            result = self._execute(repo, out)
            self.assertEqual(result.returncode, 65, result.stderr)
            self.assertIn('Unexpected gitlink', result.stderr)
            self.assertIn('160000 ', (out / 'gitlinks.txt').read_text())

    def test_large_index_without_gitlink_is_allowed(self):
        with tempfile.TemporaryDirectory() as root:
            repo, out = Path(root) / 'repo', Path(root) / 'evidence'
            out.mkdir()
            self._index_fixture(repo, False)
            result = self._execute(repo, out)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((out / 'gitlinks.txt').read_text(), '')

    def test_git_ls_files_failure_is_not_treated_as_clean(self):
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)
            out = root / 'evidence'
            out.mkdir()
            result = self._execute(root, out)  # no .git here
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('not a git repository', result.stderr.lower())
