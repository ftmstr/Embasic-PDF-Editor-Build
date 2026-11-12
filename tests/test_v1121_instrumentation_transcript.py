import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from v1121_instrumentation_transcript import check_transcript

GOOD = b"\n".join([
    b"INSTRUMENTATION_RESULT: v1121_protocol=1",
    b"INSTRUMENTATION_RESULT: v1121_run=2",
    b"INSTRUMENTATION_RESULT: v1121_passed=2",
    b"INSTRUMENTATION_RESULT: v1121_failed=0",
    b"INSTRUMENTATION_RESULT: v1121_outcome=PASS",
    b"INSTRUMENTATION_CODE: -1",
]) + b"\n"

class TranscriptProtocolTests(unittest.TestCase):
    def bad(self, data, rc=0):
        result, reason = check_transcript(data, rc)
        self.assertFalse(result, reason)

    def test_good_local_format_is_not_android_pass(self):
        result, msg = check_transcript(GOOD, 0)
        self.assertTrue(result)
        self.assertIn("NOT_ANDROID_PROVENANCE", msg)

    def test_missing_code(self): self.bad(GOOD.replace(b"INSTRUMENTATION_CODE: -1\n", b""))
    def test_nonzero_instrumentation_code(self): self.bad(GOOD.replace(b"-1\n", b"0\n"))
    def test_duplicate_instrumentation_code(self): self.bad(GOOD + b"INSTRUMENTATION_CODE: -1\n")
    def test_adb_failure(self): self.bad(GOOD, rc=1)
    def test_duplicate_test_count(self): self.bad(GOOD + b"INSTRUMENTATION_RESULT: v1121_run=2\n")
    def test_missing_test_count(self): self.bad(GOOD.replace(b"INSTRUMENTATION_RESULT: v1121_run=2\n", b""))
    def test_skipped_one_test(self): self.bad(GOOD.replace(b"v1121_run=2", b"v1121_run=1"))
    def test_one_failed_test(self): self.bad(GOOD.replace(b"v1121_passed=2", b"v1121_passed=1").replace(b"v1121_failed=0", b"v1121_failed=1"))
    def test_false_outcome(self): self.bad(GOOD.replace(b"v1121_outcome=PASS", b"v1121_outcome=FAIL"))
    def test_error_type_despite_success(self): self.bad(GOOD + b"INSTRUMENTATION_RESULT: v1121_error_type=IOException\n")
    def test_malformed_result_line(self): self.bad(GOOD + b"INSTRUMENTATION_RESULT: v1121_run NO_EQUALS\n")
    def test_unknown_v1121_field(self): self.bad(GOOD + b"INSTRUMENTATION_RESULT: v1121_secret=hello\n")
    def test_explicit_instrumentation_failure(self): self.bad(GOOD + b"INSTRUMENTATION_FAILED: something\n")
    def test_control_byte(self): self.bad(GOOD + b"\x00")
    def test_oversize(self): self.bad(GOOD + b" " * 1_048_576)
    def test_bad_utf8(self): self.bad(GOOD + b"\xff")
    def test_empty(self): self.bad(b"")
    def test_invalid_code_line(self): self.bad(GOOD + b"INSTRUMENTATION_CODE: ok\n")
    def test_nonstandard_protocol(self): self.bad(GOOD.replace(b"v1121_protocol=1", b"v1121_protocol=2"))

if __name__ == "__main__": unittest.main()
