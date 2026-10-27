#!/usr/bin/env python3
"""Offline, read-only mechanical preflight for an explicitly reviewed PUBLIC source batch.

This does NOT establish legal ownership, privacy clearance, historical provenance,
secret-free content, trusted Git checkout, or production release readiness.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath

ALLOWED_LICENSES = frozenset({"Apache-2.0", "MIT", "BSD-2-Clause", "BSD-3-Clause", "ISC"})
ALLOWED_SUFFIXES = frozenset({".kt", ".kts", ".java", ".xml", ".md", ".json", ".toml", ".py", ".sh", ".ps1", ".yml", ".yaml", ".txt"})
SOURCE_KINDS = frozenset({"byte_exact_recovery", "reconstructed", "new_implementation"})
FORBIDDEN_NAMES = frozenset({"local.properties", "gradle.properties", "google-services.json", "credentials.json", "secrets.json", "id_rsa", "id_ed25519"})
FORBIDDEN_SUFFIXES = frozenset({".keystore", ".jks", ".p12", ".pfx", ".pem", ".key", ".env", ".zip", ".jar", ".apk", ".aab", ".pdf"})
SECRET_PATTERNS = (
    re.compile(rb"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----"),
    re.compile(rb"(?:gh[pousr]_|github_pat_)[A-Za-z0-9_]{20,}"),
    re.compile(rb"AKIA[0-9A-Z]{16}"),
    re.compile(rb"(?im)^\s*(?:password|api[_-]?key|client[_-]?secret|access[_-]?token)\s*[:=]\s*['\"]?[^'\"#\s]{8,}"),
)
MAX_FILE_BYTES = 1024 * 1024
MAX_TOTAL_BYTES = 10 * MAX_FILE_BYTES
SHA256 = re.compile(r"[0-9a-f]{64}\Z")


class AdmissionError(ValueError):
    pass


def unique_keys(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise AdmissionError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def canonical_path(raw):
    if not isinstance(raw, str) or not raw or "\\" in raw or ":" in raw or "\x00" in raw:
        raise AdmissionError("invalid POSIX path")
    p = PurePosixPath(raw)
    if p.is_absolute() or str(p) != raw or any(x in (".", "..") or x.startswith(".") for x in raw.split("/")):
        raise AdmissionError("noncanonical or hidden path")
    if p.name.lower() in FORBIDDEN_NAMES or p.suffix.lower() in FORBIDDEN_SUFFIXES:
        raise AdmissionError("sensitive or binary file name")
    if p.suffix.lower() not in ALLOWED_SUFFIXES:
        raise AdmissionError("extension not allowlisted")
    return p


def preflight(root: Path, manifest: Path):
    if not root.is_dir() or root.is_symlink():
        raise AdmissionError("candidate root must be a real directory")
    raw_manifest = manifest.read_bytes()
    if len(raw_manifest) > MAX_FILE_BYTES:
        raise AdmissionError("manifest too large")
    doc = json.loads(raw_manifest.decode("utf-8"), object_pairs_hook=unique_keys)
    if not isinstance(doc, dict) or set(doc) != {"schema_version", "files"} or type(doc["schema_version"]) is not int or doc["schema_version"] != 1:
        raise AdmissionError("manifest schema mismatch")
    entries = doc["files"]
    if not isinstance(entries, list) or not entries:
        raise AdmissionError("manifest requires nonempty files list")
    seen = set()
    total = 0
    counts = {kind: 0 for kind in sorted(SOURCE_KINDS)}
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"path", "sha256", "source_kind", "license_spdx", "rights_reviewed", "privacy_reviewed"}:
            raise AdmissionError("file entry schema mismatch")
        p = canonical_path(entry["path"])
        if str(p) in seen:
            raise AdmissionError("duplicate manifest path")
        seen.add(str(p))
        if entry["source_kind"] not in SOURCE_KINDS:
            raise AdmissionError("invalid source kind")
        if entry["license_spdx"] not in ALLOWED_LICENSES:
            raise AdmissionError("license not preliminarily allowlisted")
        if entry["rights_reviewed"] is not True or entry["privacy_reviewed"] is not True:
            raise AdmissionError("explicit rights and privacy reviews required")
        if not isinstance(entry["sha256"], str) or not SHA256.fullmatch(entry["sha256"]):
            raise AdmissionError("invalid lowercase SHA-256")
        current = root
        for component in p.parts:
            current = current / component
            if current.is_symlink():
                raise AdmissionError("symlink in source path")
        if not current.is_file() or not current.resolve().is_relative_to(root.resolve()):
            raise AdmissionError("missing or escaping source file")
        if current.stat().st_size > MAX_FILE_BYTES:
            raise AdmissionError("source file exceeds limit")
        data = current.read_bytes()
        total += len(data)
        if total > MAX_TOTAL_BYTES:
            raise AdmissionError("candidate batch exceeds limit")
        try:
            data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise AdmissionError("non-UTF-8 candidate") from exc
        if any(pattern.search(data) for pattern in SECRET_PATTERNS):
            raise AdmissionError("potential secret marker")
        if hashlib.sha256(data).hexdigest() != entry["sha256"]:
            raise AdmissionError("SHA-256 mismatch")
        counts[entry["source_kind"]] += 1
    actual = set()
    for item in root.rglob("*"):
        if item.is_symlink():
            raise AdmissionError("symlink in candidate tree")
        if item.is_file():
            actual.add(item.relative_to(root).as_posix())
    if actual != seen:
        raise AdmissionError("candidate tree differs from manifest")
    return {"result": "MECHANICAL_PREFLIGHT_PASS_ONLY", "files": len(entries), "bytes": total, "provenance_counts": counts, "production_gate": "NOT RUN", "human_approval_required": True}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        print(json.dumps(preflight(args.root, args.manifest), sort_keys=True))
        return 0
    except (AdmissionError, OSError, ValueError, TypeError) as exc:
        print(json.dumps({"result": "FAIL_CLOSED", "error": str(exc)}, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
