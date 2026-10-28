"""Metadata-only PUBLIC migration intake closure gate.

No source bytes are copied, and PASS means inventory-policy checks only.
It is not a Gradle, license, source-provenance or security acceptance gate.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

_SHA1 = re.compile(r"[0-9a-f]{40}\Z")
_ALLOWED_GROUPS = {
    "recovered-source/androidApp/src/main/kotlin/": (7, 57915),
    "recovered-source/shared/src/androidMain/kotlin/": (6, 7107),
    "recovered-source/shared/src/commonMain/kotlin/": (22, 69750),
}


class IntakeError(ValueError):
    pass


def check_intake(data: dict) -> dict:
    """Fail closed on missing or unapproved historical-source inventory entries."""
    if data.get("schema_version") != 1:
        raise IntakeError("Unsupported schema")
    if data.get("canonical_public_repo") != "ftmstr/Embasic-PDF-Editor-Build":
        raise IntakeError("Noncanonical PUBLIC target")
    if data.get("historical_source_ref") != "e4e4b4f6ccd9d838b5ac5434b45fb8202d4ba786":
        raise IntakeError("Unpinned historical source")
    if data.get("source_set_mode") != "COMPLETE_HISTORICAL_ROOTS_NOT_BUILD_PROOF":
        raise IntakeError("Missing explicit source-set qualification")
    rows = data.get("files")
    if not isinstance(rows, list) or len(rows) != 35:
        raise IntakeError("Incomplete historical source-set inventory")
    groups = Counter()
    bytes_by_group = Counter()
    seen_paths = set()
    for row in rows:
        if not isinstance(row, dict):
            raise IntakeError("Malformed file record")
        path = row.get("path")
        if not isinstance(path, str) or not path.endswith(".kt"):
            raise IntakeError("Invalid Kotlin path")
        if path.startswith("/") or "\\" in path or any(p in ("", ".", "..") for p in path.split("/")):
            raise IntakeError("Unsafe relative path")
        if path in seen_paths:
            raise IntakeError("Duplicate historical path")
        seen_paths.add(path)
        group = next((g for g in _ALLOWED_GROUPS if path.startswith(g)), None)
        if group is None:
            raise IntakeError("Unapproved source-set root")
        sha = row.get("historical_git_blob_sha1")
        if not isinstance(sha, str) or not _SHA1.fullmatch(sha):
            raise IntakeError("Missing historical Git blob identity")
        size = row.get("historical_tree_size")
        if not isinstance(size, int) or isinstance(size, bool) or size < 0:
            raise IntakeError("Invalid historical size")
        for flag in ("rights_review", "license_review", "privacy_review", "secret_review", "provenance_review"):
            if row.get(flag) != "NOT VERIFIED":
                raise IntakeError("Unproven clearance flag: " + flag)
        if row.get("admission") != "BLOCKED":
            raise IntakeError("Unauthorized source admission")
        if row.get("byte_exact_recovery") is not False:
            raise IntakeError("Unsupported byte-exact recovery claim")
        if row.get("source_bytes_included") is not False:
            raise IntakeError("PRIVATE source bytes must not be embedded")
        groups[group] += 1
        bytes_by_group[group] += size
    for group, (count, total) in _ALLOWED_GROUPS.items():
        if groups[group] != count or bytes_by_group[group] != total:
            raise IntakeError("Source-set closure count/size mismatch: " + group)
    return {
        "result": "PASS_METADATA_ONLY",
        "candidate_count": len(rows),
        "blocked_count": len(rows),
        "historical_tree_bytes": sum(bytes_by_group.values()),
        "source_sets": {g: {"count": groups[g], "historical_tree_bytes": bytes_by_group[g]} for g in _ALLOWED_GROUPS},
        "product_gradle_build": "NOT RUN",
        "rights_license_privacy_security": "NOT VERIFIED",
        "public_migration": "BLOCKED",
        "production_final": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
        print(json.dumps(check_intake(data), ensure_ascii=False, indent=2))
        return 0
    except (IntakeError, OSError, ValueError, TypeError) as exc:
        print(json.dumps({"result": "FAIL", "reason": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
