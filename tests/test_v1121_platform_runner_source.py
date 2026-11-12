import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'prototypes' / 'android-platform-instrumentation'
SOURCE = ROOT / 'src/androidDeviceTest/kotlin/org/embasic/pdfeditor/platformtest/PlatformOnlyPdfInstrumentation.kt'
MANIFEST = ROOT / 'manifest/AndroidManifest.xml.template'
README = ROOT / 'README.md'

class PlatformOnlySourceAdmission(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE.read_text('utf-8')
        cls.manifest = MANIFEST.read_text('utf-8')
        cls.readme = README.read_text('utf-8')

    def test_runner_is_platform_instrumentation(self):
        self.assertIn('class PlatformOnlyPdfInstrumentation : Instrumentation()', self.source)
        self.assertIn('override fun onStart()', self.source)
        self.assertIn('finish(status, result)', self.source)

    def test_no_third_party_test_framework_import(self):
        imports = [x for x in self.source.splitlines() if x.startswith('import ')]
        for line in imports:
            self.assertTrue(line.startswith(('import android.', 'import java.')), line)
        self.assertNotIn('@Test', self.source)

    def test_test_counts_and_nonzero_failure(self):
        self.assertIn('passed++', self.source)
        self.assertIn('failed++', self.source)
        self.assertIn('Activity.RESULT_CANCELED', self.source)
        self.assertIn('Activity.RESULT_OK', self.source)
        for f in ('v1121_protocol', 'v1121_run', 'v1121_passed', 'v1121_failed', 'v1121_outcome'):
            self.assertIn(f, self.source)

    def test_real_pdf_platform_render_not_mock(self):
        for fragment in ('PdfDocument()', 'document.finishPage(page)', 'document.writeTo(it)',
                         'PdfRenderer(descriptor)', 'page.render(bitmap', 'bitmap.getPixel(48, 72)',
                         'bitmap.getPixel(8, 8)', 'bitmap.eraseColor(Color.MAGENTA)'):
            self.assertIn(fragment, self.source)

    def test_malformed_input_and_real_parser_negative(self):
        self.assertIn('"not-a-pdf"', self.source)
        self.assertIn('catch (_: IOException)', self.source)
        self.assertIn('check(rejected)', self.source)

    def test_resource_release_visible(self):
        for fragment in ('bitmap.recycle()', 'page.close()', 'renderer.close()',
                         'descriptor.close()', 'document.close()', 'check(file.delete() || !file.exists())'):
            self.assertIn(fragment, self.source)

    def test_cache_only_no_sensitive_pdf(self):
        self.assertIn('targetContext.cacheDir', self.source)
        self.assertIn('File.createTempFile(', self.source)
        self.assertNotIn('getExternalStorageDirectory', self.source)
        self.assertNotIn('READ_EXTERNAL_STORAGE', self.source)

    def test_manifest_templates_unresolved(self):
        manifest = ET.fromstring(self.manifest)
        android = '{http://schemas.android.com/apk/res/android}'
        self.assertEqual(manifest.attrib['package'], '@TEST_PACKAGE@')
        self.assertEqual(len(manifest), 1)
        self.assertEqual(manifest[0].attrib[android + 'targetPackage'], '@TARGET_PACKAGE@')
        self.assertEqual(manifest[0].attrib[android + 'name'],
                         'org.embasic.pdfeditor.platformtest.PlatformOnlyPdfInstrumentation')

    def test_readme_requires_two_apk_licensing(self):
        for phrase in ('STAGING / NOT APPROVED', 'production', 'test APK', 'resolved', 'Gradle'):
            self.assertIn(phrase, self.readme)
        self.assertIn('NOT RUN', self.readme)

    def test_no_fabricated_sdk_compilation(self):
        self.assertIn('NOT compiled against Android SDK', self.source)
        self.assertIn('NOT executed on an Android device', self.source)

if __name__ == '__main__': unittest.main()
