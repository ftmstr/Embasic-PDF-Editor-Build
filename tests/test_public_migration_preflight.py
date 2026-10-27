"""Synthetic, isolated tests; no PRIVATE source or production release claims."""
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from public_migration_preflight import AdmissionError, preflight, unique_keys


class MigrationPreflightTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / "candidate"
        self.root.mkdir()
        self.file = self.root / "src" / "Editor.kt"
        self.file.parent.mkdir()
        self.file.write_text("package example\nclass Editor\n", encoding="utf-8")
        self.manifest = self.base / "manifest.json"
        self.entry = {"path": "src/Editor.kt", "sha256": hashlib.sha256(self.file.read_bytes()).hexdigest(), "source_kind": "new_implementation", "license_spdx": "Apache-2.0", "rights_reviewed": True, "privacy_reviewed": True}
        self.save()

    def save(self):
        self.manifest.write_text(json.dumps({"schema_version": 1, "files": [self.entry]}), encoding="utf-8")

    def fails(self):
        with self.assertRaises((AdmissionError, ValueError)):
            preflight(self.root, self.manifest)

    def test_valid_synthetic_file(self):
        result = preflight(self.root, self.manifest)
        self.assertEqual(result["result"], "MECHANICAL_PREFLIGHT_PASS_ONLY")
        self.assertTrue(result["human_approval_required"])

    def test_hash_tampering(self):
        self.file.write_text("tampered", encoding="utf-8")
        self.fails()

    def test_path_traversal(self):
        self.entry["path"] = "../secret.kt"
        self.save()
        self.fails()

    def test_symlink(self):
        self.file.unlink()
        self.file.symlink_to(self.base / "outside.kt")
        self.fails()

    def test_gpl_not_preapproved(self):
        self.entry["license_spdx"] = "GPL-3.0-only"
        self.save()
        self.fails()

    def test_missing_privacy_review(self):
        self.entry["privacy_reviewed"] = False
        self.save()
        self.fails()

    def test_secret_marker(self):
        self.file.write_text("api_key = 'abcdefgh1234567890'\n", encoding="utf-8")
        self.entry["sha256"] = hashlib.sha256(self.file.read_bytes()).hexdigest()
        self.save()
        self.fails()

    def test_extra_unlisted_file(self):
        (self.root / "unlisted.md").write_text("not reviewed")
        self.fails()

    def test_sensitive_filename(self):
        self.entry["path"] = "local.properties"
        self.save()
        self.fails()

    def test_duplicate_json_key(self):
        with self.assertRaises(AdmissionError):
            json.loads('{"schema_version":1,"schema_version":1}', object_pairs_hook=unique_keys)

    def test_duplicate_manifest_path(self):
        self.manifest.write_text(json.dumps({"schema_version":1,"files":[self.entry,self.entry]}))
        self.fails()

    def test_invalid_utf8(self):
        self.file.write_bytes(b"\xff\xfe")
        self.entry["sha256"] = hashlib.sha256(self.file.read_bytes()).hexdigest()
        self.save()
        self.fails()

    def test_hidden_path(self):
        self.entry["path"] = ".hidden.kt"
        self.save()
        self.fails()


if __name__ == "__main__":
    unittest.main()
