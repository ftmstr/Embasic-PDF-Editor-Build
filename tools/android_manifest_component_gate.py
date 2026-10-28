#!/usr/bin/env python3
"""Independent, read-only Android isolated-service admission preflight.

This checks a narrow migration invariant, NOT Android compilation, package merging,
security clearance, runtime correctness, or release readiness.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ANDROID = '{http://schemas.android.com/apk/res/android}'
SEGMENT = r'[A-Za-z_][A-Za-z0-9_]*'
QUALIFIED = re.compile(rf'{SEGMENT}(?:\.{SEGMENT})+\Z')
COMPONENT = re.compile(rf'\.?{SEGMENT}(?:\.{SEGMENT})*\Z')
MAX_BYTES = 1024 * 1024

class GateError(ValueError):
    pass


def resolve_name(namespace: str, raw: str) -> str:
    if not isinstance(namespace, str) or not QUALIFIED.fullmatch(namespace):
        raise GateError('invalid namespace')
    if not isinstance(raw, str) or not COMPONENT.fullmatch(raw):
        raise GateError('invalid component name')
    if raw.startswith('.'):
        return namespace + raw
    if '.' not in raw:
        return namespace + '.' + raw
    return raw


def read_file(path: Path) -> str:
    if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_BYTES:
        raise GateError('missing, symlinked or oversized input')
    return path.read_text(encoding='utf-8')


def source_class_exists(fqcn: str, source_roots: list[Path]) -> bool:
    package, _, name = fqcn.rpartition('.')
    if not package or not name:
        return False
    rel = Path(*package.split('.'))
    for root in source_roots:
        if root.is_symlink() or not root.is_dir():
            raise GateError('invalid source root')
        for suffix in ('.kt', '.java'):
            candidate = root / rel / (name + suffix)
            if candidate.is_symlink():
                raise GateError('symlinked service source')
            if not candidate.is_file():
                continue
            body = read_file(candidate)
            if re.search(r'^\s*package\s+' + re.escape(package) + r'\s*[;\r\n]', body, re.M) and re.search(
                r'\b(?:class|object)\s+' + re.escape(name) + r'\b', body
            ):
                return True
    return False


def check(manifest: Path, namespace: str, source_roots: list[Path], require_isolated: bool = True) -> dict:
    if not source_roots:
        raise GateError('at least one source root is required')
    resolve_name(namespace, 'Example')
    content = read_file(manifest)
    if '<!DOCTYPE' in content.upper() or '<!ENTITY' in content.upper():
        raise GateError('DTD/entity declaration forbidden')
    try:
        doc = ET.fromstring(content)
    except ET.ParseError as exc:
        raise GateError('invalid XML') from exc
    if doc.tag != 'manifest':
        raise GateError('not an Android manifest')
    services = doc.findall('./application/service')
    isolated = [x for x in services if x.attrib.get(ANDROID + 'isolatedProcess') == 'true']
    if require_isolated and not isolated:
        raise GateError('isolated service missing')
    for item in isolated:
        if item.attrib.get(ANDROID + 'exported') != 'false':
            raise GateError('isolated service must not be exported')
        process = item.attrib.get(ANDROID + 'process', '')
        if not re.fullmatch(r':[A-Za-z_][A-Za-z0-9_]*', process):
            raise GateError('isolated service must have private process name')
        fqcn = resolve_name(namespace, item.attrib.get(ANDROID + 'name'))
        if not source_class_exists(fqcn, source_roots):
            raise GateError('isolated service class missing or package mismatch')
    return {
        'result': 'MECHANICAL_ANDROID_COMPONENT_PASS_ONLY',
        'isolated_services': len(isolated),
        'production_gate': 'NOT RUN',
        'runtime_verified': False,
        'license_and_privacy_review_required': True,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', required=True, type=Path)
    parser.add_argument('--namespace', required=True)
    parser.add_argument('--source-root', required=True, type=Path, action='append')
    args = parser.parse_args(argv)
    try:
        print(json.dumps(check(args.manifest, args.namespace, args.source_root), sort_keys=True))
        return 0
    except (GateError, OSError, UnicodeError) as exc:
        print(json.dumps({'result': 'FAIL_CLOSED', 'reason': str(exc)}, sort_keys=True))
        return 1

if __name__ == '__main__':
    sys.exit(main())
