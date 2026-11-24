"""Run actual pre/post status gate excerpts with real local Git fixtures.

The Git producer failure and truncated-record cases inject only ls-files output.
No network, hosted run, or product build is performed.
"""
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    'runner': ROOT / 'tools/p0_public_checkout_once.sh',
    'hosted': ROOT / '.github/workflows/p0-trusted-public-checkout.yml',
}


def git(cwd, *args):
    return subprocess.run(['git', *args], cwd=cwd, check=True,
                          capture_output=True).stdout


def gate(source, phase):
    lines = source.read_text(encoding='utf-8').splitlines()
    index = next(i for i, line in enumerate(lines)
                 if line.strip().startswith('git status --porcelain=v1 ')
                 and f'status-{phase}.txt' in line)
    block = lines[index:index + 2]
    if lines[index - 1].strip().startswith('check_index_flags '):
        block.insert(0, lines[index - 1])
    helper = re.search(r'^\s*check_index_flags\(\) \{\n.*?^\s*\}',
                       '\n'.join(lines), re.M | re.S)
    return (helper.group(0) + '\n' if helper else '') + '\n'.join(block)


class ShellIndexFlags(unittest.TestCase):
    def exercise(self, source, phase, case):
        with tempfile.TemporaryDirectory(prefix='embasic-v1132-') as temp:
            root = Path(temp)
            work = root / 'work'
            work.mkdir()
            git(work, 'init', '-b', 'main')
            git(work, 'config', 'user.name', 'Synthetic Fixture')
            git(work, 'config', 'user.email', 'fixture@example.invalid')
            (work / 'file.txt').write_bytes(b'original\n')
            (work / 'line\nS misleading.txt').write_bytes(b'newline name\n')
            git(work, 'add', '--all')
            git(work, 'commit', '-m', 'fixture')
            if case in ('assume-unchanged', 'skip-worktree'):
                git(work, 'update-index', '--' + case, '--', 'file.txt')
                (work / 'file.txt').write_bytes(b'changed\n')
                self.assertEqual(git(work, 'status', '--porcelain=v1',
                                     '--untracked-files=all'), b'')
            elif case == 'dirty':
                (work / 'file.txt').write_bytes(b'changed\n')
            injection = ''
            if case == 'producer-failure':
                injection = ('git() { if [[ "$*" == "ls-files -v -z" ]]; then '
                             'return 42; fi; command git "$@"; }\n')
            elif case == 'truncated-record':
                injection = ('git() { if [[ "$*" == "ls-files -v -z" ]]; then '
                             'printf "H file.txt"; return 0; fi; command git "$@"; }\n')
            script = ('set -Eeuo pipefail\nOUT="$1"\nROOT="$1"\n' + injection
                      + gate(source, phase) + '\n')
            run = subprocess.run(['bash', '-c', script, 'bash', str(root)],
                                 cwd=work, capture_output=True, text=True, timeout=10)
            if case == 'clean':
                self.assertEqual(run.returncode, 0, run.stderr)
            else:
                self.assertNotEqual(run.returncode, 0,
                                    f'{source.name} {phase} accepted {case}')


def scenario(source, phase, case):
    def test(self):
        self.exercise(SOURCES[source], phase, case)
    return test


for source in SOURCES:
    for phase in ('pre', 'post'):
        for case in ('clean', 'dirty', 'assume-unchanged', 'skip-worktree',
                     'producer-failure', 'truncated-record'):
            name = f'test_{source}_{phase}_{case.replace("-", "_")}'
            setattr(ShellIndexFlags, name, scenario(source, phase, case))


if __name__ == '__main__':
    unittest.main()
