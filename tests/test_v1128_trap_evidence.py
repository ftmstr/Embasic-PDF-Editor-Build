"""V1128 regression: missing/truncated evidence must never yield a PASS exit.
Runs the real source-bound Bash complete() function, with isolated stub tools.
These are scoped local tests, NOT a trusted clone or product release tests.
"""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'tools' / 'p0_public_checkout_once.sh'


def completion_function():
    source = SCRIPT.read_text(encoding='utf-8')
    return source.split('complete() {\n', 1)[1].split('\n}\ntrap complete EXIT', 1)[0]


def exercise(failed_tool=None, runner_exit=0):
    with tempfile.TemporaryDirectory(prefix='embasic-v1128-') as temp:
        directory = Path(temp)
        out = directory / 'evidence'
        out.mkdir()
        (out / 'runner.log').write_text('sentinel log\n', encoding='utf-8')
        stubbin = directory / 'bin'
        stubbin.mkdir()
        if failed_tool:
            stub = stubbin / failed_tool
            stub.write_text('#!/bin/sh\nexit 42\n', encoding='utf-8')
            stub.chmod(0o755)
        shell = '''set -Eeuo pipefail
OUT="$1"
LOG="$OUT/runner.log"
STAGE="SUCCESS_SCOPED_ONLY"
HEAD_SHA="synthetic"
REMOTE_SHA="synthetic"
VERIFIER="PASS (scoped only)"
KOTLIN="NOT RUN"
STARTED="2026-11-22T00:00:00Z"
PUBLIC_REPO="ftmstr/Embasic-PDF-Editor-Build"
exec 3>&1 4>&2
complete() {
''' + completion_function() + '\n}\ntrap complete EXIT\nexit "$2"\n'
        env = dict(os.environ, PATH=str(stubbin) + ':' + os.environ['PATH'])
        result = subprocess.run(['bash', '-c', shell, 'bash', str(out), str(runner_exit)],
                                capture_output=True, text=True, env=env, timeout=8)
        report = out / 'checkout-evidence.json'
        sums = out / 'SHA256SUMS.txt'
        return result.returncode, report.exists(), sums.exists(), (
            json.loads(report.read_text('utf-8')) if report.exists() else None)


class CompletionEvidenceGateTest(unittest.TestCase):
    def test_normal_success_writes_complete_evidence(self):
        code, report, sums, payload = exercise()
        self.assertEqual(code, 0)
        self.assertTrue(report and sums)
        self.assertEqual(payload['status'], 'PASS')

    def test_runner_failure_remains_failure(self):
        code, report, sums, payload = exercise(runner_exit=17)
        self.assertEqual(code, 17)
        self.assertTrue(report and sums)
        self.assertEqual(payload['status'], 'FAIL')

    def test_json_writer_failure_cannot_report_pass(self):
        code, report, sums, payload = exercise(failed_tool='python3')
        self.assertNotEqual(code, 0)
        self.assertFalse(report)

    def test_checksum_writer_failure_cannot_report_pass_or_leave_valid_json(self):
        code, report, sums, payload = exercise(failed_tool='sha256sum')
        self.assertNotEqual(code, 0)
        self.assertFalse(report)


if __name__ == '__main__':
    unittest.main()
