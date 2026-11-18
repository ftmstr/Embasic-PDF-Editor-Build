"""V1126 original independent product vs test APK identity admission checks.

Fixtures are synthetic ZIPs, not real Android APKs or Gradle resolutions.
"""
import copy
import hashlib
import os
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from v1122_dual_apk_preflight import validate

HEAD = "601a57426524b5243c5ed3d0d4e8405197e83b6e"
REPO = "ftmstr/Embasic-PDF-Editor-Build"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class DualApkPhysicalIdentity(unittest.TestCase):
    def setUp(self):
        ctx = tempfile.TemporaryDirectory()
        self.addCleanup(ctx.cleanup)
        self.root = Path(ctx.name)
        for name in ('artifacts', 'notices', 'reports'):
            (self.root / name).mkdir()
        self.app = self.root / 'artifacts/app.apk'
        self.test = self.root / 'artifacts/test.apk'
        for p, mark in ((self.app, b'APP_SYNTHETIC'), (self.test, b'TEST_SYNTHETIC')):
            with zipfile.ZipFile(p, 'w') as z:
                z.writestr('AndroidManifest.xml', b'FAKE_XML_NOT_ANDROID')
                z.writestr('classes.dex', mark)
        lib = self.root / 'artifacts/fictional.aar'
        lib.write_bytes(b'SYNTHETIC_COMPONENT_NOT_AN_AAR')
        (self.root / 'notices/lib.txt').write_text('Synthetic test notice, no real license evidence')
        report = self.root / 'reports/gradle.txt'
        report.write_text('SYNTHETIC_GRADLE_NOT_REAL')
        c = dict(id='org.example:mock:1', file='artifacts/fictional.aar',
                 sha256=digest(lib), spdx='MIT', notice='notices/lib.txt', dependencies=[])
        def graph(name, path):
            return dict(package='org.embasic.pdfeditor' + ('.test' if name=='instrumentation' else ''),
                        target_package='org.embasic.pdfeditor' if name=='instrumentation' else None,
                        apk={'file':str(path.relative_to(self.root)), 'sha256':digest(path)},
                        roots=[c['id']], components=[copy.deepcopy(c)])
        self.data={'schema_version':1,'repository':REPO,'head':HEAD,
                   'status':'PRODUCTION NOT FINAL',
                   'graphs':{'production':graph('production',self.app),
                             'instrumentation':graph('instrumentation',self.test)},
                   'gradle_evidence':{'report_file':'reports/gradle.txt', 'sha256':digest(report),
                                      'head':HEAD,'source':'ACTUAL_GRADLE_RESOLUTION',
                                      'variants':['production','instrumentation']}}

    def issues(self):
        return validate(self.data, self.root, HEAD)

    def use_test(self, path):
        self.data['graphs']['instrumentation']['apk'] = {'file':str(path.relative_to(self.root)), 'sha256':digest(path)}

    def test_distinct_mock_apks_format_only(self):
        self.assertEqual(self.issues(), [])

    def test_same_exact_path_rejected(self):
        self.use_test(self.app)
        self.assertTrue(any('distinct' in x.lower() or 'same' in x.lower() for x in self.issues()), self.issues())

    def test_hardlinked_apks_rejected(self):
        self.test.unlink()
        os.link(self.app, self.test)
        self.use_test(self.test)
        self.assertTrue(self.issues(), 'hardlinked APKs must not pass separate product/test evidence')

    def test_byte_identical_distinct_files_rejected(self):
        self.test.write_bytes(self.app.read_bytes())
        self.use_test(self.test)
        self.assertFalse(os.path.samefile(self.test, self.app))
        self.assertTrue(self.issues(), 'byte-identical production/test APKs must not pass')

    def test_independent_distinct_files_after_identity_reset_accepted_local_only(self):
        self.test.write_bytes(self.test.read_bytes() + b'different synthetic test package')
        self.use_test(self.test)
        self.assertEqual(self.issues(), [])

    def test_shared_dependency_artifact_is_allowed(self):
        self.assertEqual(self.data['graphs']['production']['components'][0]['file'],
                         self.data['graphs']['instrumentation']['components'][0]['file'])
        self.assertEqual(self.issues(), [])

    def test_missing_test_apk_remains_rejected(self):
        self.test.unlink()
        self.assertTrue(self.issues())

    def test_distinct_bytes_cannot_bypass_declared_sha(self):
        self.test.write_bytes(self.test.read_bytes()+b'changed_without_sha_update')
        self.assertTrue(any('SHA256' in x or 'sha' in x.lower() for x in self.issues()), self.issues())

if __name__=='__main__':
    unittest.main()
