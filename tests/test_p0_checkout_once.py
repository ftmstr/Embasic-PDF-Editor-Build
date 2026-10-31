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
