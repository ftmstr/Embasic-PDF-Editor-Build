"""Stdlib-only regression checks for the manual, read-only P0 workflow."""
import pathlib
import re
import unittest

WORKFLOW = pathlib.Path(__file__).resolve().parents[1] / '.github' / 'workflows' / 'p0-trusted-public-checkout.yml'


class ManualWorkflowPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = WORKFLOW.read_text(encoding='utf-8')

    def test_manual_only_trigger(self):
        m = re.search(r'^on:\s*\n((?:^[ \t]+.*\n|^\s*$)*)', self.content, re.M)
        self.assertIsNotNone(m)
        self.assertEqual(re.findall(r'^  ([a-z_]+):', m.group(1), re.M), ['workflow_dispatch'])

    def test_read_only_token_permissions(self):
        self.assertRegex(self.content, r'(?m)^permissions:\s*\n  contents: read\s*$')
        self.assertNotRegex(self.content, r'(?m)^\s*(?:actions|issues|pull-requests|contents): write\s*$')

    def test_canonical_origin_only(self):
        self.assertIn('https://github.com/ftmstr/Embasic-PDF-Editor-Build.git', self.content)
        self.assertNotIn('uygulama-baslangic-sablonu', self.content)
        self.assertIn('git remote get-url origin', self.content)

    def test_complete_checkout_and_fsck_required(self):
        for marker in ('--no-single-branch', '--is-shallow-repository',
                       'git fsck --full --strict', 'git status --porcelain',
                       'refs/remotes/origin/main', 'git ls-remote --exit-code'):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.content)

    def test_no_external_action_or_remote_write(self):
        for forbidden in ('uses:', 'git push', 'git reset --hard', 'git submodule update',
                          'curl ', 'wget ', 'gh workflow run', 'gh api -X POST'):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, self.content)

    def test_trigger_sha_bound_to_checked_out_head(self):
        """The evidence must be tied to the workflow_dispatch event commit."""
        self.assertIn('GITHUB_SHA', self.content)
        self.assertRegex(self.content, r'test "\$HEAD_SHA" = "\$GITHUB_SHA"')

    def test_scoped_test_reporting_not_final(self):
        self.assertIn('test_p0_public_checkout.py', self.content)
        self.assertIn('test_public_migration_preflight.py', self.content)
        self.assertIn('PRODUCTION NOT FINAL', self.content)
        self.assertIn('NOT RUN', self.content)


if __name__ == '__main__':
    unittest.main()
