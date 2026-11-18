"""Original standalone tests for the PUBLIC manual-only workflow gitlink gate.

No GitHub Actions workflow is dispatched, and no genuine clone is claimed.
"""
from pathlib import Path
import subprocess
import tempfile
import unittest

WORKFLOW = Path(__file__).resolve().parents[1] / '.github/workflows/p0-trusted-public-checkout.yml'


def workflow_script():
    text = WORKFLOW.read_text(encoding='utf-8')
    assert '  workflow_dispatch:' in text
    assert 'on:\n  workflow_dispatch:\n' in text
    assert '    runs-on: ubuntu-24.04' in text
    script = text.split('        run: |\n', 1)[1]
    return '\n'.join(line[10:] if line.startswith('          ') else line
                     for line in script.splitlines())


def gate_script():
    script = workflow_script()
    start = script.index('# Fail closed if main moved')
    start = script.index('test "$HEAD_SHA" = "$GITHUB_SHA"', start) + len('test "$HEAD_SHA" = "$GITHUB_SHA"')
    end = script.index('git fsck --full --strict --no-reflogs', start)
    return script[start:end]


def gate_case(lines, exit_code):
    gate = gate_script()
    with tempfile.TemporaryDirectory() as tmp:
        text = f'''set -Eeuo pipefail
ROOT={tmp!r}
git() {{
  [[ "$*" == 'ls-files --stage' ]] || return 90
  printf '%s' {lines!r}
  return {exit_code}
}}
{gate}
echo __AFTER_GATE__
'''
        return subprocess.run(['bash', '-c', text], capture_output=True, text=True, timeout=8)


class WorkflowGitlinkFailClosed(unittest.TestCase):
    def test_manual_only_is_read_only(self):
        content = WORKFLOW.read_text('utf-8')
        self.assertEqual(content.count('  workflow_dispatch:'), 1)
        for forbidden in ('  push:', '  pull_request:', '  schedule:', '  workflow_run:', 'contents: write'):
            self.assertNotIn(forbidden, content)

    def test_good_index_without_gitlink_continues(self):
        r = gate_case('100644 deadbeef 0\tREADME.md\n', 0)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('__AFTER_GATE__', r.stdout)

    def test_gitlink_blocks(self):
        r = gate_case('160000 deadbeef 0\tvendor\n', 0)
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertNotIn('__AFTER_GATE__', r.stdout)

    def test_producer_failure_with_gitlink_blocks(self):
        r = gate_case('160000 deadbeef 0\tvendor\n', 42)
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertNotIn('__AFTER_GATE__', r.stdout)

    def test_producer_failure_without_gitlink_blocks(self):
        r = gate_case('100644 deadbeef 0\tREADME.md\n', 42)
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertNotIn('__AFTER_GATE__', r.stdout)

    def test_no_index_output_on_producer_failure_blocks(self):
        r = gate_case('', 42)
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertNotIn('__AFTER_GATE__', r.stdout)

    def test_gitlink_scan_is_explicitly_bounded_to_complete_index(self):
        gate = gate_script()
        self.assertIn('git ls-files --stage >', gate)
        self.assertIn('scan_status=', gate)
        self.assertIn('"$scan_status"', gate)
        self.assertNotIn('git ls-files --stage | awk', gate)


if __name__ == '__main__':
    unittest.main()
