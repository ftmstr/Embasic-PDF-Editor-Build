"""Original V1124 regression tests for SDK probe path/identity pinning.

All tests are LOCAL mocked SDK outputs, not real Android/Gradle/provenance tests.
"""
import contextlib
import hashlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import v1123_android_sdk_probe as probe


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class V1124FileIdentityTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.bin = self.root / 'approved-sdk'
        self.bin.mkdir()
        self.data = self.root / 'artifacts'
        self.data.mkdir()
        self.aapt = self.bin / 'aapt2'
        self.apksigner = self.bin / 'apksigner'
        self.app = self.data / 'product.apk'
        self.test = self.data / 'instrumentation.apk'
        self.aapt.write_bytes(b'local only mock aapt2 binary: not an SDK executable')
        self.apksigner.write_bytes(b'local only mock apksigner binary: not an SDK executable')
        self.app.write_bytes(b'not real app APK bytes')
        self.test.write_bytes(b'not real test APK bytes')

    def argv(self):
        return ['--aapt2', str(self.aapt), '--apksigner', str(self.apksigner),
                '--app-apk', str(self.app), '--test-apk', str(self.test),
                '--expected-package', 'org.embasic.pdfeditor',
                '--expected-test-package', 'org.embasic.pdfeditor.test',
                '--expected-runner', 'org.embasic.platformtest.Probe',
                '--app-signer-sha256', 'a'*64,
                '--test-signer-sha256', 'b'*64,
                '--aapt2-sha256', sha(self.aapt),
                '--apksigner-sha256', sha(self.apksigner)]

    def fake_sdk(self, tool, args, label, timeout):
        if args[0] == 'dump':
            if 'app ' in label:
                return "package: name='org.embasic.pdfeditor' versionCode='1'\n"
            return ("package: name='org.embasic.pdfeditor.test' versionCode='1'\n"
                    "instrumentation: name='org.embasic.platformtest.Probe' "
                    "targetPackage='org.embasic.pdfeditor'\n")
        if args[0] == 'verify':
            digest = 'a'*64 if 'app ' in label else 'b'*64
            return f'Signer #1 certificate SHA-256 digest: {digest}\n'
        raise AssertionError('Unexpected SDK command')

    def run_probe(self, *, on_sdk_call=None):
        calls = 0
        def fake(tool, args, label, timeout):
            nonlocal calls
            calls += 1
            if on_sdk_call is not None:
                on_sdk_call(calls)
            return self.fake_sdk(tool, args, label, timeout)
        buf = io.StringIO()
        with patch.object(probe, 'sdk_call', fake), contextlib.redirect_stdout(buf):
            code = probe.main(self.argv())
        result = json.loads(buf.getvalue())
        return code, result, calls

    def assertBlocked(self, **kwargs):
        code, record, _ = self.run_probe(**kwargs)
        self.assertEqual(code, 65, record)
        self.assertEqual(record['result'], 'BLOCKED')
        self.assertEqual(record['production_gate'], 'NOT RUN')
        self.assertFalse(record['production_final'])

    def test_clean_unchanged_independent_files_local_format_only(self):
        code, rec, calls = self.run_probe()
        self.assertEqual(code, 0, rec)
        self.assertEqual(calls, 4)
        self.assertEqual(rec['result'], 'LOCAL_SDK_OUTPUT_PREFLIGHT_ONLY')
        self.assertEqual(rec['production_gate'], 'NOT RUN')
        self.assertEqual(rec['android_test_execution'], 'NOT RUN')
        self.assertFalse(rec['production_final'])

    def test_ancestor_symlink_aapt_tool_must_fail_closed(self):
        alias = self.root / 'sdk-alias'
        alias.symlink_to(self.bin, target_is_directory=True)
        self.aapt = alias / 'aapt2'
        self.assertBlocked()

    def test_ancestor_symlink_apksigner_tool_must_fail_closed(self):
        alias = self.root / 'signer-alias'
        alias.symlink_to(self.bin, target_is_directory=True)
        self.apksigner = alias / 'apksigner'
        self.assertBlocked()

    def test_ancestor_symlink_app_apk_must_fail_closed(self):
        alias = self.root / 'app-alias'
        alias.symlink_to(self.data, target_is_directory=True)
        self.app = alias / 'product.apk'
        self.assertBlocked()

    def test_ancestor_symlink_test_apk_must_fail_closed(self):
        alias = self.root / 'test-alias'
        alias.symlink_to(self.data, target_is_directory=True)
        self.test = alias / 'instrumentation.apk'
        self.assertBlocked()

    def test_distinct_names_hardlinked_same_apk_must_fail_closed(self):
        self.test.unlink()
        os.link(self.app, self.test)
        self.assertNotEqual(self.app, self.test)
        self.assertTrue(os.path.samefile(self.app, self.test))
        self.assertBlocked()

    def test_distinct_files_identical_apk_bytes_must_fail_closed(self):
        self.test.write_bytes(self.app.read_bytes())
        self.assertFalse(os.path.samefile(self.app, self.test))
        self.assertBlocked()

    def test_approved_tool_mutates_during_probe_must_fail_closed(self):
        def mutate(call):
            if call == 2:
                self.aapt.write_bytes(b'changed after initial pin verification')
        self.assertBlocked(on_sdk_call=mutate)

    def test_tool_replaced_same_bytes_different_inode_must_fail_closed(self):
        def replace(call):
            if call == 2:
                content = self.apksigner.read_bytes()
                tmp = self.bin / 'temporary-replacement'
                tmp.write_bytes(content)
                os.replace(tmp, self.apksigner)
        self.assertBlocked(on_sdk_call=replace)

    def test_apk_replaced_same_bytes_different_inode_must_fail_closed(self):
        def replace(call):
            if call == 3:
                contents = self.app.read_bytes()
                tmp = self.data / 'temporary-app'
                tmp.write_bytes(contents)
                os.replace(tmp, self.app)
        self.assertBlocked(on_sdk_call=replace)

    def test_rejected_tool_does_not_mutate_legitimate_apk(self):
        expected = sha(self.app)
        absent = self.root / 'absent-sdk-tool'
        with self.assertRaises(probe.ProbeBlocked):
            probe.checked_file(str(absent), 'aapt2', 100 * 1024 * 1024)
        self.assertEqual(sha(self.app), expected)


if __name__ == '__main__':
    unittest.main()
