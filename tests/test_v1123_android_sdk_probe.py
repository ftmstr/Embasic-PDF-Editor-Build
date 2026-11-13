import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

TOOL = Path(__file__).resolve().parents[1] / 'tools' / 'v1123_android_sdk_probe.py'
PIN_APP = 'a' * 64
PIN_TEST = 'b' * 64

MOCK = '''#!/usr/bin/env python3
import os,sys,time
args=sys.argv[1:]
kind='app' if 'app.apk' in args[-1] else 'test'
mode=os.getenv('MOCK_MODE','')
if mode=='timeout': time.sleep(2)
if mode=='exit': sys.exit(3)
if mode=='empty': sys.exit(0)
if mode=='badutf8': sys.stdout.buffer.write(b'\\xff'); sys.exit(0)
if mode=='oversize': print('x'*530000); sys.exit(0)
if args[0]=='dump':
    pkg='org.example.pdf' if kind=='app' else 'org.example.pdf.test'
    if mode=='badpkg' and kind=='test': pkg='org.other.test'
    print("package: name='"+pkg+"' versionCode='1'")
    if mode=='duplicatepkg': print("package: name='"+pkg+"' versionCode='1'")
    if kind=='test' and mode!='noneinstrument':
        target='org.other' if mode=='wrongtarget' else 'org.example.pdf'
        runner='org.other.Runner' if mode=='wrongrunner' else 'org.example.platform.PlatformOnlyPdfInstrumentation'
        print("instrumentation: name='"+runner+"' targetPackage='"+target+"'")
    if kind=='app' and mode=='instrumentApp':
        print("instrumentation: name='org.example.platform.PlatformOnlyPdfInstrumentation' targetPackage='org.example.pdf'")
elif args[0]=='verify':
    digest='a'*64 if kind=='app' else 'b'*64
    if mode=='wrongsigner': digest='f'*64
    if mode=='zerosigner': sys.exit(0)
    print('Signer #1 certificate SHA-256 digest: '+digest)
    if mode=='multisigner': print('Signer #2 certificate SHA-256 digest: '+digest)
else: sys.exit(4)
'''

class APKToolchainGate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.mock = self.root / 'fake-android-sdk'
        self.mock.write_text(MOCK, encoding='utf-8')
        self.mock.chmod(0o700)
        self.app = self.root / 'app.apk'
        self.test = self.root / 'test.apk'
        self.app.write_bytes(b'FAKE_APK_APP_NOT_REAL_BINARY')
        self.test.write_bytes(b'FAKE_APK_TEST_NOT_REAL_BINARY')
        sha = hashlib.sha256(self.mock.read_bytes()).hexdigest()
        self.flags = ['--aapt2',str(self.mock),'--apksigner',str(self.mock),
            '--app-apk',str(self.app),'--test-apk',str(self.test),
            '--expected-package','org.example.pdf',
            '--expected-test-package','org.example.pdf.test',
            '--expected-runner','org.example.platform.PlatformOnlyPdfInstrumentation',
            '--app-signer-sha256',PIN_APP,'--test-signer-sha256',PIN_TEST,
            '--aapt2-sha256',sha,'--apksigner-sha256',sha, '--timeout-seconds','1']

    def runprobe(self, mode='', extra=None):
        args=self.flags.copy()
        if extra: extra(args)
        proc=subprocess.run([sys.executable,str(TOOL),*args],
            env={**os.environ,'MOCK_MODE':mode},capture_output=True,text=True,timeout=10)
        return proc.returncode,json.loads(proc.stdout)

    def bad(self,mode='',extra=None):
        rc,v=self.runprobe(mode,extra)
        self.assertEqual(rc,65,v)
        self.assertEqual(v['result'],'BLOCKED')
        self.assertEqual(v['production_gate'],'NOT RUN')
        self.assertFalse(v['production_final'])

    def test_synthetic_success_only_local_preflight(self):
        rc,v=self.runprobe()
        self.assertEqual(rc,0,v)
        self.assertEqual(v['result'],'LOCAL_SDK_OUTPUT_PREFLIGHT_ONLY')
        self.assertEqual(v['production_gate'],'NOT RUN')
        self.assertEqual(v['android_test_execution'],'NOT RUN')
        self.assertEqual(v['gradle_resolved_graph'],'NOT_VERIFIED')
        self.assertEqual(v['license_sbom_notice'],'NOT_VERIFIED')
        self.assertEqual(v['app_signer_fingerprint'],PIN_APP)

    def test_missing_aapt2(self): self.bad(extra=lambda a:a.__setitem__(a.index(str(self.mock)),str(self.root/'none')))
    def test_bad_aapt_pin(self): self.bad(extra=lambda a:a.__setitem__(a.index('--aapt2-sha256')+1,'f'*64))
    def test_bad_apksigner_pin(self): self.bad(extra=lambda a:a.__setitem__(a.index('--apksigner-sha256')+1,'f'*64))
    def test_bad_expected_app_signer(self): self.bad(extra=lambda a:a.__setitem__(a.index('--app-signer-sha256')+1,'f'*64))
    def test_missing_app(self): self.bad(extra=lambda a:a.__setitem__(a.index(str(self.app)),str(self.root/'none.apk')))
    def test_test_apk_symlink(self):
        p=self.root/'link.apk';p.symlink_to(self.test)
        self.bad(extra=lambda a:a.__setitem__(a.index(str(self.test)),str(p)))
    def test_app_and_test_same(self): self.bad(extra=lambda a:a.__setitem__(a.index(str(self.test)),str(self.app)))
    def test_invalid_expected_package(self): self.bad(extra=lambda a:a.__setitem__(a.index('org.example.pdf'),'not package'))
    def test_same_expected_package(self): self.bad(extra=lambda a:a.__setitem__(a.index('org.example.pdf.test'),'org.example.pdf'))
    def test_wrong_package(self): self.bad('badpkg')
    def test_wrong_instrumentation_target(self): self.bad('wrongtarget')
    def test_wrong_instrumentation_runner(self): self.bad('wrongrunner')
    def test_no_instrumentation(self): self.bad('noneinstrument')
    def test_product_contains_instrumentation(self): self.bad('instrumentApp')
    def test_bad_signer_pin(self): self.bad('wrongsigner')
    def test_missing_signer(self): self.bad('zerosigner')
    def test_multiple_signers(self): self.bad('multisigner')
    def test_duplicate_package(self): self.bad('duplicatepkg')
    def test_nonzero_sdk_exit(self): self.bad('exit')
    def test_blank_sdk_output(self): self.bad('empty')
    def test_invalid_utf8(self): self.bad('badutf8')
    def test_bounded_output(self): self.bad('oversize')
    def test_timeout(self): self.bad('timeout')
    def test_zero_timeout(self): self.bad(extra=lambda a:a.__setitem__(a.index('--timeout-seconds')+1,'0'))
    def test_unknown_approved_signer(self): self.bad(extra=lambda a:a.__setitem__(a.index('--test-signer-sha256')+1,'not-sha'))
    def test_tools_read_only_no_shell(self):
        source=TOOL.read_text('utf-8')
        self.assertIn('subprocess.run([str(tool), *args]',source)
        self.assertNotIn('shell=True',source)
        self.assertNotIn('apksigner sign',source)
    def test_mutated_apk_during_sdk_call(self):
        # Fake platform executable changes input: the hash must not match after calls.
        other=self.root/'mutating-sdk'
        other.write_text(MOCK.replace("args=sys.argv[1:]", "args=sys.argv[1:]\nif args[0]=='verify' and 'app.apk' in args[-1]: open(args[-1],'ab').write(b'mutated')"),encoding='utf-8')
        other.chmod(0o700)
        sha=hashlib.sha256(other.read_bytes()).hexdigest()
        def mutate(a):
            a[a.index('--aapt2')+1]=str(other)
            a[a.index('--apksigner')+1]=str(other)
            a[a.index('--aapt2-sha256')+1]=sha
            a[a.index('--apksigner-sha256')+1]=sha
        self.bad(extra=mutate)

if __name__=='__main__': unittest.main()
