import copy
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from v1122_dual_apk_preflight import validate, duplicate_reject

HEAD = 'ebd19257e798103498e58aceb3c6ea031a3b475f'


class DualApkClosurePreflight(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'artifacts').mkdir()
        (self.root / 'notices').mkdir()
        (self.root / 'reports').mkdir()
        for name in ('app.apk', 'test.apk'):
            with zipfile.ZipFile(self.root / 'artifacts' / name, 'w') as z:
                z.writestr('AndroidManifest.xml', b'FAKE_NOT_REAL_BINARY_XML')
                z.writestr('classes.dex', b'FAKE_NOT_REAL_DEX')
        (self.root / 'artifacts/lib.aar').write_bytes(b'synthetic test component; no actual AAR')
        (self.root / 'notices/lib.txt').write_text('Fake sample MIT notice for structural checks only', encoding='utf-8')
        (self.root / 'reports/gradle.json').write_text('SYNTHETIC; NOT AN ACTUAL GRADLE REPORT', encoding='utf-8')
        sha = lambda p: hashlib.sha256((self.root / p).read_bytes()).hexdigest()
        lib = {'id': 'org.example:original:1.0', 'file':'artifacts/lib.aar',
               'sha256':sha('artifacts/lib.aar'), 'spdx':'MIT','notice':'notices/lib.txt', 'dependencies':[]}
        graph = lambda name, apk: {
            'package': 'org.embasic.pdfeditor' + ('.test' if name == 'instrumentation' else ''),
            'target_package': 'org.embasic.pdfeditor' if name == 'instrumentation' else None,
            'apk': {'file':'artifacts/' + apk, 'sha256':sha('artifacts/' + apk)},
            'roots':[lib['id']], 'components':[copy.deepcopy(lib)]
        }
        self.record = {'schema_version':1, 'repository':'ftmstr/Embasic-PDF-Editor-Build', 'head':HEAD,
            'status':'PRODUCTION NOT FINAL',
            'graphs': {'production': graph('production', 'app.apk'), 'instrumentation': graph('instrumentation', 'test.apk')},
            'gradle_evidence':{'report_file':'reports/gradle.json', 'sha256':sha('reports/gradle.json'),
                               'head':HEAD,'source':'ACTUAL_GRADLE_RESOLUTION','variants':['production','instrumentation']}}

    def check(self, mutation, phrase=None):
        item = copy.deepcopy(self.record)
        mutation(item)
        errors = validate(item, self.root, HEAD)
        self.assertTrue(errors, 'untrusted manifest unexpectedly passed preflight')
        if phrase:
            self.assertIn(phrase, ' '.join(errors))

    def test_synthetic_good_is_still_only_local_format(self):
        self.assertEqual(validate(self.record,self.root,HEAD),[])

    def test_old_head(self): self.check(lambda x:x.update(head='0'*40),'stale')
    def test_wrong_repo(self): self.check(lambda x:x.update(repository='ftmstr/private'), 'noncanonical')
    def test_production_final_claim(self): self.check(lambda x:x.update(status='FINAL'), 'release claim')
    def test_missing_graph(self): self.check(lambda x:x['graphs'].pop('instrumentation'), 'distinct')
    def test_same_apk_package(self): self.check(lambda x:x['graphs']['instrumentation'].update(package='org.embasic.pdfeditor'), 'distinct')
    def test_mismatched_instrumentation_target(self): self.check(lambda x:x['graphs']['instrumentation'].update(target_package='org.other'), 'mismatched')
    def test_missing_apk_path(self): self.check(lambda x:x['graphs']['production']['apk'].update(file='artifacts/no.apk'), 'APK evidence invalid')
    def test_apk_digest_mismatch(self): self.check(lambda x:x['graphs']['production']['apk'].update(sha256='0'*64), 'APK SHA256 mismatch')
    def test_apk_path_traversal(self): self.check(lambda x:x['graphs']['production']['apk'].update(file='../outside.apk'), 'APK evidence invalid')
    def test_apk_absolute_path(self): self.check(lambda x:x['graphs']['production']['apk'].update(file='/etc/passwd'), 'APK evidence invalid')
    def test_unsupported_spdx(self): self.check(lambda x:x['graphs']['production']['components'][0].update(spdx='GPL-3.0-only'), 'unapproved')
    def test_epl_instrumentation_blocked(self): self.check(lambda x:x['graphs']['instrumentation']['components'][0].update(spdx='EPL-1.0'), 'unapproved')
    def test_forged_junit_mit_still_blocked(self): self.check(lambda x:x['graphs']['instrumentation']['components'][0].update(id='junit:junit:4.13.2') or x['graphs']['instrumentation'].update(roots=['junit:junit:4.13.2']), 'JUnit EPL test-only exception')
    def test_nonstring_spdx_fails_closed(self): self.check(lambda x:x['graphs']['production']['components'][0].update(spdx={'bad':'spdx'}), 'unapproved')
    def test_composite_spdx_requires_review(self): self.check(lambda x:x['graphs']['production']['components'][0].update(spdx='MIT OR EPL-1.0'), 'unapproved')
    def test_unknown_license(self): self.check(lambda x:x['graphs']['production']['components'][0].update(spdx='NOASSERTION'), 'unapproved')
    def test_junit_production_leak(self): self.check(lambda x:x['graphs']['production']['components'][0].update(id='junit:junit:4.13.2') or x['graphs']['production'].update(roots=['junit:junit:4.13.2']), 'test-library leakage')
    def test_androidx_test_production_leak(self): self.check(lambda x:x['graphs']['production']['components'][0].update(id='androidx.test:runner:1.7.0') or x['graphs']['production'].update(roots=['androidx.test:runner:1.7.0']), 'test-library leakage')
    def test_root_missing(self): self.check(lambda x:x['graphs']['production'].update(roots=['not:present:1.0']), 'missing root')
    def test_orphan(self): self.check(lambda x:x['graphs']['production'].update(components=x['graphs']['production']['components'] + [{**x['graphs']['production']['components'][0], 'id':'org.other:orphan:1'}]), 'orphan')
    def test_transitive_missing(self): self.check(lambda x:x['graphs']['production']['components'][0].update(dependencies=['missing:lib:2.0']), 'missing root')
    def test_duplicate_component(self): self.check(lambda x:x['graphs']['production']['components'].append(copy.deepcopy(x['graphs']['production']['components'][0])), 'duplicate')
    def test_missing_notice(self): self.check(lambda x:x['graphs']['production']['components'][0].update(notice='notices/not-present.txt'), 'missing/untrusted notice')
    def test_wrong_artifact_sha(self): self.check(lambda x:x['graphs']['instrumentation']['components'][0].update(sha256='f'*64), 'component SHA256 mismatch')
    def test_empty_roots(self): self.check(lambda x:x['graphs']['production'].update(roots=[]), 'empty')
    def test_missing_gradle_resolution(self): self.check(lambda x:x.update(gradle_evidence={}), 'no separate')
    def test_synthetic_gradle_source_not_admissible(self): self.check(lambda x:x['gradle_evidence'].update(source='SYNTHETIC'), 'missing/stale/synthetic')
    def test_gradle_report_hash(self): self.check(lambda x:x['gradle_evidence'].update(sha256='1'*64), 'Gradle report')
    def test_gradle_wrong_variants(self): self.check(lambda x:x['gradle_evidence'].update(variants=['production']), 'missing/stale/synthetic')
    def test_symlink_in_evidence_path_rejected(self):
        (self.root/"artifacts"/"link.apk").symlink_to("app.apk")
        self.check(lambda x:x["graphs"]["production"]["apk"].update(file="artifacts/link.apk"), "APK evidence invalid")
    def test_duplicate_json_property_rejected(self):
        with self.assertRaises(ValueError):
            json.loads('{"head":"a","head":"b"}',object_pairs_hook=duplicate_reject)
    def test_cli_never_claims_release(self):
        path=self.root/'manifest.json'
        path.write_text(json.dumps(self.record))
        cmd=[sys.executable,str(Path(__file__).resolve().parents[1]/'tools/v1122_dual_apk_preflight.py'), '--manifest',str(path),'--evidence-root',str(self.root),'--expected-head',HEAD]
        out=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=6)
        self.assertEqual(out.returncode,0)
        obj=json.loads(out.stdout)
        self.assertEqual(obj['result'],'LOCAL_FILE_GRAPH_PREFLIGHT_ONLY')
        self.assertEqual(obj['production_gate'],'NOT RUN')
        self.assertFalse(obj['production_final'])
        self.assertEqual(obj['android_apk_identity'],'NOT_VERIFIED')
    def test_cli_bad_input_fails_closed(self):
        path=self.root/'manifest.json'; path.write_text('{"head":"dup","head":"more"}')
        cmd=[sys.executable,str(Path(__file__).resolve().parents[1]/'tools/v1122_dual_apk_preflight.py'), '--manifest',str(path),'--evidence-root',str(self.root),'--expected-head',HEAD]
        out=subprocess.run(cmd,stdout=subprocess.PIPE,timeout=6)
        self.assertEqual(out.returncode,65)
        self.assertEqual(json.loads(out.stdout)['result'],'BLOCKED')

if __name__ == '__main__': unittest.main()
