#!/usr/bin/env python3
"""Read-only, fail-closed file/graph preflight for independently evidenced APKs.

NEVER a substitute for Gradle resolution, aapt package inspection, real Android
execution, signing verification, SBOM or third-party license acceptance.
"""
import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

ALLOW = frozenset({'Apache-2.0', 'MIT', 'BSD-2-Clause', 'BSD-3-Clause', 'ISC', 'Zlib'})
EXCLUDED_PROD_PREFIXES = ('junit:', 'org.hamcrest:', 'androidx.test:', 'androidx.test.ext:')
HEAD_RE = re.compile(r'^[0-9a-f]{40}$')
SHA_RE = re.compile(r'^[0-9a-f]{64}$')
GAV_RE = re.compile(r'^[A-Za-z0-9_.-]+:[A-Za-z0-9_.-]+:[A-Za-z0-9][A-Za-z0-9_.+\-]*$')
PACKAGE_RE = re.compile(r'^[a-zA-Z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+$')
MAX_JSON_BYTES = 2_000_000
MAX_FILE_BYTES = 512 * 1024 * 1024


def duplicate_reject(pairs):
    value = {}
    for k, v in pairs:
        if k in value:
            raise ValueError(f'duplicate JSON key {k!r}')
        value[k] = v
    return value


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for part in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(part)
    return h.hexdigest()


def safe_path(root, item):
    if not isinstance(item, str) or not item or '\\' in item or '\x00' in item:
        raise ValueError('invalid relative file path')
    path = Path(item)
    if path.is_absolute() or any(x in ('..', '.') for x in path.parts):
        raise ValueError('traversal/absolute file path')
    candidate = root / path
    for ancestor in (candidate, *candidate.parents):
        if ancestor == root.parent:
            break
        if ancestor.is_symlink():
            raise ValueError('symlink in file path')
    real = candidate.resolve(strict=True)
    if not real.is_relative_to(root.resolve(strict=True)) or not real.is_file() or real.is_symlink():
        raise ValueError('file escapes evidence root or is not regular')
    if real.stat().st_size > MAX_FILE_BYTES:
        raise ValueError('evidence file is oversized')
    return real


def apk_structure(path):
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        if len(infos) > 5_000 or sum(i.file_size for i in infos) > 256 * 1024 * 1024:
            raise ValueError('ZIP too large for bounded preflight')
        paths = [i.filename for i in infos]
        if len(paths) != len(set(paths)) or any(n.startswith('/') or '..' in Path(n).parts or '\\' in n for n in paths):
            raise ValueError('APK ZIP unsafe/duplicate entries')
        if 'AndroidManifest.xml' not in paths or 'classes.dex' not in paths:
            raise ValueError('APK ZIP lacks manifest/dex (does not verify binary format)')
        if archive.testzip() is not None:
            raise ValueError('APK ZIP CRC failed')


def validate(data, evidence_root, expected_head):
    issues = []
    def fail(msg):
        issues.append(msg)
    if not isinstance(data, dict) or set(data) != {'schema_version', 'repository', 'head', 'status', 'graphs', 'gradle_evidence'}:
        return ['unexpected or missing top-level fields']
    if type(data['schema_version']) is not int or data['schema_version'] != 1:
        fail('unknown manifest schema')
    if data['repository'] != 'ftmstr/Embasic-PDF-Editor-Build' or data['head'] != expected_head or not HEAD_RE.fullmatch(str(data['head'])):
        fail('noncanonical/stale PUBLIC head')
    if data['status'] != 'PRODUCTION NOT FINAL':
        fail('unsupported release claim')
    graphs = data['graphs']
    if not isinstance(graphs, dict) or set(graphs) != {'production', 'instrumentation'}:
        fail('must provide distinct production and instrumentation graphs')
        return issues
    package_names = {}
    for name in ('production', 'instrumentation'):
        g = graphs[name]
        if not isinstance(g, dict) or set(g) != {'package', 'target_package', 'apk', 'roots', 'components'}:
            fail(f'{name}: incomplete graph structure')
            continue
        package_names[name] = g['package']
        if not isinstance(g['package'], str) or not PACKAGE_RE.fullmatch(g['package']):
            fail(f'{name}: invalid package identifier')
        if (name == 'production' and g['target_package'] is not None) or (name == 'instrumentation' and g['target_package'] != package_names.get('production')):
            fail(f'{name}: mismatched target/production package')
        apk = g['apk']
        if not isinstance(apk, dict) or set(apk) != {'file', 'sha256'}:
            fail(f'{name}: absent real APK digest/path')
        else:
            try:
                path = safe_path(evidence_root, apk['file'])
                if not SHA_RE.fullmatch(str(apk['sha256'])) or digest(path) != apk['sha256']:
                    fail(f'{name}: APK SHA256 mismatch')
                apk_structure(path)
            except (OSError, ValueError, zipfile.BadZipFile, RuntimeError) as exc:
                fail(f'{name}: APK evidence invalid ({type(exc).__name__})')
        roots = g['roots']
        comps = g['components']
        if not isinstance(roots, list) or not roots or any(not isinstance(x, str) for x in roots) or len(roots) != len(set(roots)):
            fail(f'{name}: invalid/empty resolved dependency roots')
            continue
        if not isinstance(comps, list) or not comps or len(comps) > 20_000:
            fail(f'{name}: missing/oversize resolved component closure')
            continue
        by_id = {}
        for c in comps:
            if not isinstance(c, dict) or set(c) != {'id', 'file', 'sha256', 'spdx', 'notice', 'dependencies'}:
                fail(f'{name}: invalid component contract')
                continue
            ident = c['id']
            if not isinstance(ident, str) or not GAV_RE.fullmatch(ident) or ident in by_id:
                fail(f'{name}: malformed/duplicate component id')
                continue
            by_id[ident] = c
            if not isinstance(c['spdx'], str) or c['spdx'] not in ALLOW:
                fail(f'{name}: unapproved or composite/unknown SPDX for {ident}: {c["spdx"]}')
            if name == 'production' and ident.startswith(EXCLUDED_PROD_PREFIXES):
                fail(f'production: test-library leakage detected {ident}')
            if ident.startswith('junit:junit:'):
                fail(f'{name}: JUnit EPL test-only exception not approved {ident}')
            if not isinstance(c['dependencies'], list) or any(not isinstance(x, str) for x in c['dependencies']) or len(set(c['dependencies'])) != len(c['dependencies']):
                fail(f'{name}: invalid graph edges {ident}')
            for key in ('file', 'notice'):
                try:
                    path = safe_path(evidence_root, c[key])
                    if key == 'file' and (not SHA_RE.fullmatch(str(c['sha256'])) or digest(path) != c['sha256']):
                        fail(f'{name}: component SHA256 mismatch {ident}')
                    if key == 'notice' and (path.stat().st_size == 0 or path.stat().st_size > 1_000_000):
                        fail(f'{name}: blank/oversized notice {ident}')
                except (OSError, ValueError) as exc:
                    fail(f'{name}: missing/untrusted {key} {ident} ({type(exc).__name__})')
        visited = set()
        todo = list(roots)
        while todo:
            x = todo.pop()
            if x in visited:
                continue
            if x not in by_id:
                fail(f'{name}: missing root/transitive component {x}')
                continue
            visited.add(x)
            deps = by_id[x]['dependencies']
            if isinstance(deps, list):
                todo.extend(y for y in deps if isinstance(y, str))
        if set(by_id) != visited:
            fail(f'{name}: orphan/nonresolved component in graph')
    if package_names.get('production') == package_names.get('instrumentation'):
        fail('production and test APK must be distinct packages')
    gradle = data['gradle_evidence']
    if not isinstance(gradle, dict) or set(gradle) != {'report_file', 'sha256', 'head', 'source', 'variants'}:
        fail('no separate captured Gradle resolution evidence')
    else:
        if gradle['head'] != expected_head or gradle['source'] != 'ACTUAL_GRADLE_RESOLUTION' or set(gradle.get('variants', [])) != {'production', 'instrumentation'}:
            fail('Gradle resolution record is missing/stale/synthetic')
        try:
            path = safe_path(evidence_root, gradle['report_file'])
            if not SHA_RE.fullmatch(str(gradle['sha256'])) or digest(path) != gradle['sha256'] or path.stat().st_size == 0:
                fail('Gradle report missing/mismatched SHA')
        except (OSError, ValueError) as exc:
            fail(f'Gradle report missing/unsafe ({type(exc).__name__})')
    return issues


def main(argv=None):
    cli = argparse.ArgumentParser()
    cli.add_argument('--manifest', type=Path, required=True)
    cli.add_argument('--evidence-root', type=Path, required=True)
    cli.add_argument('--expected-head', required=True)
    args = cli.parse_args(argv)
    try:
        raw = args.manifest.read_bytes()
        if len(raw) > MAX_JSON_BYTES:
            raise ValueError('oversize JSON')
        record = json.loads(raw.decode('utf-8'), object_pairs_hook=duplicate_reject)
        issues = validate(record, args.evidence_root, args.expected_head)
    except (ValueError, UnicodeError, OSError, TypeError) as exc:
        issues = ['unreadable/invalid evidence: ' + type(exc).__name__]
    print(json.dumps({
        'result': 'BLOCKED' if issues else 'LOCAL_FILE_GRAPH_PREFLIGHT_ONLY',
        'issues': issues[:80], 'production_gate': 'NOT RUN',
        'gradle_runtime': 'NOT_VERIFIED', 'android_apk_identity': 'NOT_VERIFIED',
        'signatures_and_sbom': 'NOT_VERIFIED', 'production_final': False,
    }, sort_keys=True))
    return 65 if issues else 0


if __name__ == '__main__':
    sys.exit(main())
