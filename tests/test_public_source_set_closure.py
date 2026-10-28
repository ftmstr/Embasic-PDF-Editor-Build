"""Synthetic negative and positive tests for metadata-only source-set intake."""
import copy
import unittest

from public_source_set_closure import IntakeError, check_intake

ROOTS = {
    "recovered-source/androidApp/src/main/kotlin/": (7, 57915),
    "recovered-source/shared/src/androidMain/kotlin/": (6, 7107),
    "recovered-source/shared/src/commonMain/kotlin/": (22, 69750),
}


def fixture():
    rows = []
    for root, (count, total) in ROOTS.items():
        per, rem = divmod(total, count)
        for i in range(count):
            rows.append({
                "path": root + "example/F%02d.kt" % i,
                "historical_git_blob_sha1": "%040x" % (i + 1),
                "historical_tree_size": per + (rem if i == 0 else 0),
                "rights_review": "NOT VERIFIED", "license_review": "NOT VERIFIED",
                "privacy_review": "NOT VERIFIED", "secret_review": "NOT VERIFIED",
                "provenance_review": "NOT VERIFIED", "admission": "BLOCKED",
                "byte_exact_recovery": False, "source_bytes_included": False,
            })
    return {"schema_version": 1, "canonical_public_repo": "ftmstr/Embasic-PDF-Editor-Build",
            "historical_source_ref": "e4e4b4f6ccd9d838b5ac5434b45fb8202d4ba786",
            "source_set_mode": "COMPLETE_HISTORICAL_ROOTS_NOT_BUILD_PROOF", "files": rows}


class ClosureGateTests(unittest.TestCase):
    def assert_blocked(self, change):
        x = fixture()
        change(x)
        with self.assertRaises(IntakeError):
            check_intake(x)

    def test_baseline(self):
        out = check_intake(fixture())
        self.assertEqual(out["candidate_count"], 35)
        self.assertEqual(out["blocked_count"], 35)
        self.assertEqual(out["historical_tree_bytes"], 134772)
        self.assertEqual(out["product_gradle_build"], "NOT RUN")

    def test_missing_file(self):
        self.assert_blocked(lambda x: x["files"].pop())

    def test_duplicate_file(self):
        self.assert_blocked(lambda x: x["files"].__setitem__(1, copy.deepcopy(x["files"][0])))

    def test_wrong_group_size(self):
        self.assert_blocked(lambda x: x["files"][0].__setitem__("historical_tree_size", 1))

    def test_path_traversal(self):
        self.assert_blocked(lambda x: x["files"][0].__setitem__("path", "../escape.kt"))

    def test_unapproved_root(self):
        self.assert_blocked(lambda x: x["files"][0].__setitem__("path", "product/shared/src/main/kotlin/F.kt"))

    def test_bad_sha(self):
        self.assert_blocked(lambda x: x["files"][0].__setitem__("historical_git_blob_sha1", "bad"))

    def test_unverified_rights_must_remain_blocked(self):
        self.assert_blocked(lambda x: x["files"][0].__setitem__("admission", "ADMITTED"))

    def test_cannot_promote_byte_exact(self):
        self.assert_blocked(lambda x: x["files"][0].__setitem__("byte_exact_recovery", True))

    def test_no_private_bytes(self):
        self.assert_blocked(lambda x: x["files"][0].__setitem__("source_bytes_included", True))

    def test_noncanonical_repo(self):
        self.assert_blocked(lambda x: x.__setitem__("canonical_public_repo", "ftmstr/uygulama-baslangic-sablonu"))

    def test_wrong_source_ref(self):
        self.assert_blocked(lambda x: x.__setitem__("historical_source_ref", "main"))

    def test_missing_scope_qualification(self):
        self.assert_blocked(lambda x: x.__setitem__("source_set_mode", "COMPLETE"))

    def test_license_promotion_blocked(self):
        self.assert_blocked(lambda x: x["files"][0].__setitem__("license_review", "PASS"))

    def test_wrong_schema(self):
        self.assert_blocked(lambda x: x.__setitem__("schema_version", 2))

    def test_reject_bool_size(self):
        self.assert_blocked(lambda x: x["files"][0].__setitem__("historical_tree_size", True))


if __name__ == "__main__":
    unittest.main()
