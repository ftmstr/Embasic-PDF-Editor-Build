"""Synthetic, independently authored regression fixtures. No PRIVATE source is used."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from android_manifest_component_gate import GateError, check, resolve_name

NS = 'com.example.editor'
PKG = 'com.example.editor.android.isolated'
FQCN = PKG + '.RendererService'

class AndroidComponentAdmissionTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.sources = self.root / 'src'
        self.sources.mkdir()
        self.manifest = self.root / 'AndroidManifest.xml'
        self.add_source()

    def add_source(self):
        path = self.sources / Path(*PKG.split('.')) / 'RendererService.kt'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('package ' + PKG + '\nclass RendererService\n', encoding='utf-8')
        return path

    def write_manifest(self, name=FQCN, exported='false', isolated='true', process=':renderer'):
        self.manifest.write_text(
            '<?xml version="1.0" encoding="utf-8"?>\n'
            '<manifest xmlns:android="http://schemas.android.com/apk/res/android">'
            '<application><service android:name="' + name + '" '
            'android:exported="' + exported + '" '
            'android:isolatedProcess="' + isolated + '" '
            'android:process="' + process + '"/></application></manifest>',
            encoding='utf-8',
        )

    def test_fully_qualified_service_passes(self):
        self.write_manifest()
        self.assertEqual(check(self.manifest, NS, [self.sources])['isolated_services'], 1)

    def test_relative_name_wrong_package_fails(self):
        self.write_manifest(name='.isolated.RendererService')
        with self.assertRaisesRegex(GateError, 'package mismatch'):
            check(self.manifest, NS, [self.sources])

    def test_relative_name_under_actual_namespace_passes(self):
        self.write_manifest(name='.android.isolated.RendererService')
        self.assertEqual(check(self.manifest, NS, [self.sources])['isolated_services'], 1)

    def test_exported_isolated_service_fails(self):
        self.write_manifest(exported='true')
        with self.assertRaisesRegex(GateError, 'must not be exported'):
            check(self.manifest, NS, [self.sources])

    def test_nonprivate_process_fails(self):
        self.write_manifest(process='com.example.external')
        with self.assertRaisesRegex(GateError, 'private process'):
            check(self.manifest, NS, [self.sources])

    def test_missing_isolated_service_fails(self):
        self.write_manifest(isolated='false')
        with self.assertRaisesRegex(GateError, 'isolated service missing'):
            check(self.manifest, NS, [self.sources])

    def test_source_class_missing_fails(self):
        self.write_manifest()
        (self.sources / Path(*PKG.split('.')) / 'RendererService.kt').unlink()
        with self.assertRaisesRegex(GateError, 'class missing'):
            check(self.manifest, NS, [self.sources])

    def test_symlink_source_fails(self):
        self.write_manifest()
        path = self.sources / Path(*PKG.split('.')) / 'RendererService.kt'
        path.unlink()
        path.symlink_to(self.manifest)
        with self.assertRaisesRegex(GateError, 'symlinked'):
            check(self.manifest, NS, [self.sources])

    def test_bad_namespace_fails(self):
        with self.assertRaises(GateError):
            resolve_name('com.example../bad', '.RendererService')

    def test_doctype_fails(self):
        self.write_manifest()
        content = self.manifest.read_text(encoding='utf-8')
        self.manifest.write_text('<!DOCTYPE manifest [<!ENTITY x "y">]>' + content, encoding='utf-8')
        with self.assertRaisesRegex(GateError, 'DTD'):
            check(self.manifest, NS, [self.sources])

if __name__ == '__main__':
    unittest.main()
