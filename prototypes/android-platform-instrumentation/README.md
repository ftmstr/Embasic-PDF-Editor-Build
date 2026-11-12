# Android platform-only instrumentation proof-of-concept — V1121

**STAGING / NOT APPROVED / NOT BUILDABLE AS-IS / NO ANDROID RUN.** This is original
source, not historical/private PDF Editor material, and does not add JUnit or
AndroidX. It uses Android platform APIs (`android.app.Instrumentation`,
`PdfDocument`, `PdfRenderer`, `Bitmap`, `ParcelFileDescriptor`).

The template contains unresolved `@TEST_PACKAGE@` and `@TARGET_PACKAGE@` tokens
on purpose; NEVER replace them with guessed product identities. Android-KMP
instrumentation runner wiring and source-set placement must first be tested
against a trusted full PUBLIC checkout, a rights-cleared application module,
an approved ADR-006 toolchain and actual `:shared:tasks --all` discovery.

On an authorized Android host, after build and package/runner alignment:

```
adb shell am instrument -w -r TEST_PACKAGE/org.embasic.pdfeditor.platformtest.PlatformOnlyPdfInstrumentation
```

The host must retain exit status AND raw `INSTRUMENTATION_RESULT` fields,
`INSTRUMENTATION_CODE`, device/API/OS, exact APK hashes and resolved
prod/test dependency graphs. Shell exit 0 alone **never** proves PASS. The
package has to be instrumenting the correct target. The provided exact-protocol
parser is designed to reject partial/contradictory transcripts. The platform
runtime test is NOT RUN here (no Android SDK/device/Gradle installed).

The proposed runner executes two original tests: generated black-marker/white-
background PDF raster contrast and malformed synthetic PDF rejection. Both are
bounded to the test app cache, with mandatory file/descriptor/page/bitmap cleanup.
Runtime behavior, color management, platform IOException behavior and test
APK creation need **real** device acceptance before a passing claim.

A self-reported manifest is not trusted provenance. Separate actual production
APK and test APK dependency closure + checksum/SPDX/NOTICE and ADR-007 license
approval are required. A platform-only test alternative can reduce reliance on
`junit:junit` but never automatically approves a release.
