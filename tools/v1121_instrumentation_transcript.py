#!/usr/bin/env python3
"""Fail-closed LOCAL transcript check for staged Android platform-only instrumentation.

This never certifies real Android execution, Gradle, source provenance, APK
identity, signed test package, resolved license graph, or a product release.
"""
import argparse
import json
import re
import sys
from pathlib import Path

PROTOCOL = "1"
KNOWN = {"v1121_protocol", "v1121_run", "v1121_passed", "v1121_failed", "v1121_outcome", "v1121_error_type"}
RESULT = re.compile(r"^INSTRUMENTATION_RESULT: (v1121_[a-z_]+)=(.*)$")
CODE = re.compile(r"^INSTRUMENTATION_CODE: (-?\d+)$")
MAX_BYTES = 1_048_576


def check_transcript(content: bytes, adb_exit_code: int) -> tuple[bool, str]:
    if not content or len(content) > MAX_BYTES:
        return False, "missing or oversized transcript"
    try:
        text = content.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        return False, "non-UTF8 transcript"
    if any(ord(ch) < 32 and ch not in "\n\r\t" for ch in text):
        return False, "disallowed control characters"
    fields: dict[str, str] = {}
    codes: list[int] = []
    for line in text.splitlines():
        if line.startswith("INSTRUMENTATION_FAILED:") or line.startswith("INSTRUMENTATION_ABORTED:"):
            return False, "instrumentation abort/failure"
        result = RESULT.fullmatch(line)
        if result:
            key, value = result.groups()
            if key not in KNOWN or key in fields:
                return False, "unknown or duplicate v1121 result key"
            fields[key] = value
        elif line.startswith("INSTRUMENTATION_RESULT: v1121_"):
            return False, "malformed protocol result"
        code = CODE.fullmatch(line)
        if code:
            codes.append(int(code.group(1)))
        elif line.startswith("INSTRUMENTATION_CODE:"):
            return False, "malformed instrumentation exit code"
    required = {
        "v1121_protocol": PROTOCOL,
        "v1121_run": "2",
        "v1121_passed": "2",
        "v1121_failed": "0",
        "v1121_outcome": "PASS",
    }
    if adb_exit_code != 0:
        return False, "adb shell exited nonzero"
    if len(codes) != 1 or codes[0] != -1:
        return False, "missing, duplicate or failing instrumentation code"
    if fields.get("v1121_error_type") is not None:
        return False, "error type supplied despite claimed success"
    if any(fields.get(k) != v for k, v in required.items()):
        return False, "incomplete, skipped or contradictory test counts"
    return True, "LOCAL_TRANSCRIPT_FORMAT_PASS_NOT_ANDROID_PROVENANCE"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True, help="unmodified adb shell am instrument output")
    p.add_argument("--adb-exit-code", type=int, required=True, help="actual captured adb exit status")
    args = p.parse_args(argv)
    try:
        raw = args.input.read_bytes()
        result, detail = check_transcript(raw, args.adb_exit_code)
    except (OSError, ValueError) as exc:
        result, detail = False, "cannot read transcript: " + type(exc).__name__
    print(json.dumps({"result": "LOCAL_CHECK_PASS" if result else "FAIL", "detail": detail,
                      "android_runtime": "NOT_VERIFIED", "production_gate": "NOT_RUN"}, sort_keys=True))
    return 0 if result else 65


if __name__ == "__main__":
    sys.exit(main())
