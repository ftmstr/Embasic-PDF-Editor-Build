#!/usr/bin/env python3
"""Bounded, read-only AAPT2/apksigner cross-check for two APK files.

An SDK CLI preflight only, NEVER approval of APK provenance, test execution,
Gradle resolution, signing-key custody, SBOM, or product release.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

MAX_APK_BYTES = 512 * 1024 * 1024
MAX_OUTPUT_BYTES = 512 * 1024
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
PKG = re.compile(r"[A-Za-z_][A-Za-z_0-9]*(?:\.[A-Za-z_][A-Za-z_0-9]*)+\Z")
PACKAGE_LINE = re.compile(r"(?m)^package:\s+name='([^'\r\n]+)'[^\r\n]*$")
INSTR_LINE = re.compile(r"(?m)^instrumentation:\s+([^\r\n]*)$")
SIGNED = re.compile(r"(?m)^Signer #([0-9]+) certificate SHA-256 digest:\s*([0-9a-fA-F:]+)\s*$")
ATTR = re.compile(r"\b(name|targetPackage)='([^']*)'")

class ProbeBlocked(Exception):
    pass


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def checked_file(value: str, label: str, maxsize: int) -> Path:
    p = Path(value)
    if not p.is_absolute() or not p.is_file():
        raise ProbeBlocked(f'{label}: missing or non-regular absolute file path')
    if any(part.is_symlink() for part in (p, *p.parents)):
        raise ProbeBlocked(f'{label}: symlink in path/ancestor')
    size = p.stat().st_size
    if size == 0 or size > maxsize:
        raise ProbeBlocked(f'{label}: empty or oversized')
    return p


def file_identity(path: Path) -> tuple[int, int, int, int, int]:
    # An identity snapshot reduces obvious replacement races; it is NOT an atomic attestation.
    st = path.stat()
    return (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)

def checked_sha(value: str, label: str) -> str:
    v = value.lower()
    if not HEX64.fullmatch(v):
        raise ProbeBlocked(f'{label}: invalid SHA-256 pin')
    return v


def sdk_call(tool: Path, args: list[str], label: str, timeout: int) -> str:
    # Executable and arguments are passed as argv; no shell, no script parsing.
    with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
        try:
            p = subprocess.run([str(tool), *args], stdout=stdout, stderr=stderr, timeout=timeout, check=False,
                               env={**os.environ, 'LC_ALL': 'C'})
        except (subprocess.TimeoutExpired, OSError) as e:
            raise ProbeBlocked(f'{label}: SDK command timeout/launch failure ({type(e).__name__})') from e
        if p.returncode != 0:
            raise ProbeBlocked(f'{label}: SDK command failed, exit {p.returncode}')
        if stdout.tell() > MAX_OUTPUT_BYTES or stderr.tell() > MAX_OUTPUT_BYTES:
            raise ProbeBlocked(f'{label}: oversized SDK output')
        stdout.seek(0)
        data = stdout.read(MAX_OUTPUT_BYTES + 1)
        try:
            text = data.decode('utf-8', 'strict')
        except UnicodeDecodeError as e:
            raise ProbeBlocked(f'{label}: invalid UTF-8 output') from e
        if '\x00' in text or not text.strip():
            raise ProbeBlocked(f'{label}: missing/unsafe SDK output')
        return text


def badging(output: str, label: str) -> tuple[str, list[tuple[str, str]]]:
    packages = PACKAGE_LINE.findall(output)
    if len(packages) != 1 or not PKG.fullmatch(packages[0]):
        raise ProbeBlocked(f'{label}: missing/duplicate package from AAPT2')
    pairs = []
    for entry in INSTR_LINE.findall(output):
        attrs = ATTR.findall(entry)
        names = [v for k,v in attrs if k=='name']
        targets = [v for k,v in attrs if k=='targetPackage']
        if len(names) != 1 or len(targets) != 1:
            raise ProbeBlocked(f'{label}: malformed instrumentation tag')
        pairs.append((names[0], targets[0]))
    return packages[0], pairs


def signer(output: str, label: str) -> str:
    sigs = SIGNED.findall(output)
    if len(sigs) != 1 or sigs[0][0] != '1':
        raise ProbeBlocked(f'{label}: missing/multiple signer fingerprints')
    fingerprint = sigs[0][1].replace(':', '').lower()
    if not HEX64.fullmatch(fingerprint):
        raise ProbeBlocked(f'{label}: malformed signing certificate digest')
    return fingerprint


def main(argv: list[str] | None = None) -> int:
    cli = argparse.ArgumentParser()
    for flag in ('aapt2', 'apksigner', 'app-apk', 'test-apk', 'expected-package',
                 'expected-test-package', 'expected-runner', 'app-signer-sha256',
                 'test-signer-sha256', 'aapt2-sha256', 'apksigner-sha256'):
        cli.add_argument('--'+flag, required=True)
    cli.add_argument('--timeout-seconds', type=int, default=15)
    args = cli.parse_args(argv)
    report = {'result': 'BLOCKED', 'production_gate': 'NOT RUN', 'production_final': False,
              'android_test_execution': 'NOT RUN', 'gradle_resolved_graph': 'NOT_VERIFIED',
              'license_sbom_notice': 'NOT_VERIFIED', 'sdk_tool_origin': 'PIN_MATCH_ONLY'}
    try:
        if args.timeout_seconds < 1 or args.timeout_seconds > 30:
            raise ProbeBlocked('unbounded/invalid SDK timeout')
        aapt = checked_file(args.aapt2, 'aapt2', 100 * 1024 * 1024)
        signer_tool = checked_file(args.apksigner, 'apksigner', 100 * 1024 * 1024)
        app = checked_file(args.app_apk, 'app', MAX_APK_BYTES)
        test = checked_file(args.test_apk, 'test', MAX_APK_BYTES)
        if app == test or os.path.samefile(app, test):
            raise ProbeBlocked('product and test APK must be distinct physical files')
        observed_identity = [(p, file_identity(p)) for p in (aapt, signer_tool, app, test)]
        for name in ('expected_package','expected_test_package','expected_runner'):
            if not PKG.fullmatch(getattr(args,name)):
                raise ProbeBlocked('invalid expected package/runner')
        if args.expected_package == args.expected_test_package:
            raise ProbeBlocked('production and test package must differ')
        pins = {k: checked_sha(getattr(args,k),k) for k in (
            'app_signer_sha256','test_signer_sha256','aapt2_sha256','apksigner_sha256')}
        if sha256(aapt) != pins['aapt2_sha256'] or sha256(signer_tool) != pins['apksigner_sha256']:
            raise ProbeBlocked('SDK executable hash differs from independently pinned digest')
        before = [sha256(app),sha256(test)]
        if before[0] == before[1]:
            raise ProbeBlocked('product and test APK must have distinct bytes')
        app_pkg, app_instrumentation = badging(sdk_call(aapt,['dump','badging',str(app)], 'app aapt2',args.timeout_seconds),'app')
        test_pkg, instr = badging(sdk_call(aapt,['dump','badging',str(test)], 'test aapt2',args.timeout_seconds),'test')
        if app_pkg != args.expected_package or test_pkg != args.expected_test_package:
            raise ProbeBlocked('APK package does not match independent approved expectation')
        if app_instrumentation:
            raise ProbeBlocked('unexpected instrumentation in product APK')
        if instr != [(args.expected_runner,args.expected_package)]:
            raise ProbeBlocked('instrumentation runner/targetPackage mismatch')
        app_signer = signer(sdk_call(signer_tool,['verify','-Werr','--print-certs',str(app)],'app apksigner',args.timeout_seconds),'app')
        test_signer = signer(sdk_call(signer_tool,['verify','-Werr','--print-certs',str(test)],'test apksigner',args.timeout_seconds),'test')
        if app_signer != pins['app_signer_sha256'] or test_signer != pins['test_signer_sha256']:
            raise ProbeBlocked('APK signer certificate fingerprint differs from approved pin')
        if before != [sha256(app),sha256(test)]:
            raise ProbeBlocked('APK changed during SDK verification')
        if sha256(aapt) != pins['aapt2_sha256'] or sha256(signer_tool) != pins['apksigner_sha256']:
            raise ProbeBlocked('SDK executable changed during verification')
        if any(file_identity(path) != initial for path, initial in observed_identity):
            raise ProbeBlocked('SDK tool or APK identity changed during verification')
        report['result'] = 'LOCAL_SDK_OUTPUT_PREFLIGHT_ONLY'
        report['app_apk_sha256'],report['test_apk_sha256'] = before
        report['app_signer_fingerprint'],report['test_signer_fingerprint'] = app_signer,test_signer
        report['android_apk_package_fields'] = 'SDK_OUTPUTS_MATCH_EXPECTATIONS_NOT_INDEPENDENT_PROVENANCE'
        print(json.dumps(report,sort_keys=True))
        return 0
    except (ProbeBlocked, OSError, ValueError, TypeError) as exc:
        report['reason'] = (str(exc) if isinstance(exc, ProbeBlocked) else type(exc).__name__)[:180]
        print(json.dumps(report,sort_keys=True))
        return 65

if __name__ == '__main__':
    sys.exit(main())
