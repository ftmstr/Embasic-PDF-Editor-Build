"""Original V1127 source-bound checkout cleanliness producer-failure regressions.

Local stub Git only. Does not clone, dispatch GitHub Actions or qualify product.
"""
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    'manual': ROOT / '.github/workflows/p0-trusted-public-checkout.yml',
    'one_shot': ROOT / 'tools/p0_public_checkout_once.sh',
}


def status_guards(source: str) -> list[str]:
    # The workflow is YAML; all status guard lines are in its run block.
    guards = []
    lines = source.splitlines()
    for i, line in enumerate(lines):
        if 'git status --porcelain=v1 --untracked-files=all' in line:
            next_line = lines[i + 1].strip() if i + 1 < len(lines) else ''
            guard = line.strip()
            if next_line.startswith(('test ! -s ', '[[ ! -s ')):
                guard += '\n' + next_line
            guards.append(guard)
    return guards


def run_status_gate(guard: str, status_output: str, git_exit: int) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory(prefix='v1127-check-') as tmp:
        # ROOT/OUT both point to a trusted temp evidence directory outside the repo.
        # Use a stub rather than invoking the real Git executable.
        program = '''set -Eeuo pipefail
ROOT="$1"
OUT="$1"
STUB_OUTPUT="$2"
STUB_EXIT="$3"
git() {
  [[ "$*" == 'status --porcelain=v1 --untracked-files=all' ]] || return 90
  printf '%s' "$STUB_OUTPUT"
  return "$STUB_EXIT"
}
''' + guard + '\nprintf "__AFTER_STATUS_GUARD__\\n"\n'
        return subprocess.run(['bash', '-c', program, 'bash', tmp, status_output, str(git_exit)],
                              capture_output=True, text=True, timeout=5)


class CheckoutStatusFailClosed(unittest.TestCase):
    def test_both_files_have_exactly_two_clean_tree_gates(self):
        for label, source in SOURCES.items():
            with self.subTest(label=label):
                self.assertEqual(len(status_guards(source.read_text('utf-8'))), 2)

    def test_both_files_have_no_shell_pipeline_to_status(self):
        for label, source in SOURCES.items():
            with self.subTest(label=label):
                self.assertNotIn('git status --porcelain=v1 --untracked-files=all |', source.read_text('utf-8'))

    def test_clean_git_status_passes_both_gates(self):
        for label, source in SOURCES.items():
            for gate in status_guards(source.read_text('utf-8')):
                with self.subTest(label=label, gate=gate):
                    result = run_status_gate(gate, '', 0)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn('__AFTER_STATUS_GUARD__', result.stdout)

    def test_dirty_git_status_blocks_both_gates(self):
        for label, source in SOURCES.items():
            for gate in status_guards(source.read_text('utf-8')):
                with self.subTest(label=label, gate=gate):
                    result = run_status_gate(gate, ' M docs/STATUS.md\n', 0)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertNotIn('__AFTER_STATUS_GUARD__', result.stdout)

    def test_nonzero_git_status_with_empty_output_blocks_both_gates(self):
        for label, source in SOURCES.items():
            for gate in status_guards(source.read_text('utf-8')):
                with self.subTest(label=label, gate=gate):
                    result = run_status_gate(gate, '', 42)
                    self.assertNotEqual(result.returncode, 0, result.stdout)
                    self.assertNotIn('__AFTER_STATUS_GUARD__', result.stdout)

    def test_nonzero_git_status_with_partial_clean_text_blocks_both_gates(self):
        for label, source in SOURCES.items():
            for gate in status_guards(source.read_text('utf-8')):
                with self.subTest(label=label, gate=gate):
                    result = run_status_gate(gate, '?[ÛÛ\]WËBÙ[\ÜÙ\Ý\]X[
\Ý[]\ÛÙK
BÙ[\ÜÙ\Ý[	××ÐQTÔÕUT×ÑÕPT×ÉË\Ý[ÝÝ]
BY\ÝÜÝ]\×ÜÙXÙ\×Ø\WØÚXÚÙYØYÜWØÛÛÝ[Y\Ù[NÜX[ÛÝ\ÙH[ÓÕTÑTË][\Ê
NÜÝX\[Ý]\×ÙÝX\ÊÛÝ\ÙKXYÝ^
	Ý]N	ÊJNÚ]Ù[ÝX\Ý
X[[X[Ø]OYÝX\
NÙ[\ÜÙ\YÙ^
ÝX\×Ú]Ý]\ÈK\ÜÙ[Z[]HK][XÚÙYY[\ÏX[È	×IÊBÙ[\ÜÙ\Ý[	É
Ú]Ý]\ÉËÝX\
BY\ÝÜÝ]\×ÜÛ\ÚÝÛÝÜÝÜYÚ[Ü\ÊÙ[NÜX[ÛÝ\ÙH[ÓÕTÑTË][\Ê
NÜÝX\[Ý]\×ÙÝX\ÊÛÝ\ÙKXYÝ^
	Ý]N	ÊJNÚ]Ù[ÝX\Ý
X[[X[Ø]OYÝX\
NÙ[\ÜÙ\YÙ^
ÝX\×	ÏÊ¥$ôõGÄõUBÇÓòòr  ¦bõöæÖUõòÓÒuõöÖåõòs ¢VæGFW7BæÖâ