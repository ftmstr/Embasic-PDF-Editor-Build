# V1119 — PdfRenderer pixel-oracle RED/GREEN and test-only dependency license gate

**11 Nov 2026, Türkiye. PRODUCTION NOT FINAL.**

## Canonical scope and real checkout truth
Only PUBLIC `ftmstr/Embasic-PDF-Editor-Build` main is writable. Starting HEAD `a47cd7548b581723ae1df2229857e902e62ae2aa`, STATUS V1118. Verified current PUBLIC tree, GitHub Actions **0 runs**, and last V1118 native Drive Rapor/Codex. Historical PRIVATE `ftmstr/uygulama-baslangic-sablonu` remains **STRICT READ-ONLY**.

Actually executed PUBLIC `git ls-remote` and `git clone --no-tags --no-single-branch --branch main`: both **FAIL DNS exit 128**, no checkout directory. Actual clone log SHA-256 `cd7287dabdb3d5f80ef78e3b67d837ecbb2fd1fea1b15989887f2ef9ae167439`. Current GitHub connector cannot initiate `workflow_dispatch`; no hosted run. Therefore genuine full non-shallow clone, `git fsck`, event/origin/main equality, pre/post clean tree, complete V477–latest regressions **NOT RUN**. API/Drive ZIP does not replace Git.

## New concrete test flaw and minimum staged-only fix
Exact uploaded V1118 `PdfRendererAndroidDeviceSmokeTest.kt`, SHA-256 `13f0d89afb47177de9c3fd5495a062a83b1b3327581f01ef1e37cf961510a3b4`, rendered a generated white page but asserted **only page count and dimensions**. Blank/wrong raster output could pass this test. This is a **false-positive test oracle risk**, not evidence that actual Android `PdfRenderer` is faulty.

Built **new** Python source/license tests before editing: original V1118 candidate **3 expected RED failures, 8/11 PASS, process exit 1**. Edited ONLY an isolated, UNAPPROVED staged test candidate to draw a black interior rectangle on a white synthetic PDF background, initialize the bitmap magenta and assert interior/exterior pixel brightness contrast after render; preserved malformed PDF rejection and resource cleanup. New candidate SHA-256 `f4d8a9545cb5b897f98de0522408108a7da081501488d497403daaf9ac3f9217`; unified patch SHA-256 `dce785247305b9789ab0e5f2a8ca161b4ed3a1021452c0d9b5dae2854f4fb481`. **11/11 executed local stdlib source/license checks PASS, exit 0**. Actual pixel behavior, Android compilation, instrumented execution and color-tolerance calibration: **NOT RUN**. No source/third-party binaries migrated to PUBLIC product.

## Newly researched license gate — **NOT approved**
Project's user-uploaded `11-ACIK-KAYNAK-LISANS-POLITIKASI(2).md` defaults to Apache-2.0, MIT, BSD-2/3, ISC, Zlib; non-allowlisted licenses require separate review. Official AndroidX Test release listing identifies stable `androidx.test:runner:1.7.0`, `androidx.test:core:1.7.0`, `androidx.test.ext:junit:1.3.0` (source code Apache-2.0 indicators). These are **candidate coordinates only**; exact resolved artifact SHA-256, transitive SPDX/NOTICE and distribution scope **NOT RUN**. https://developer.android.com/jetpack/androidx/releases/test

Official JUnit/Maven Central metadata for **`junit:junit:4.13.2` specifies EPL-1.0**, not the project's default permissive allowlist; JUnit's Hamcrest 1.3 transitive is reported New BSD. Test-only use is a distinct policy question; **BLOCKED_TEST_ONLY_EXCEPTION_REVIEW**, not automatic acceptance or shipped runtime addition. https://central.sonatype.com/artifact/junit/junit/4.13.2 and https://junit.org/junit4/dependencies.html . No JAR/AAR was downloaded or added. A Drive-only `UNAPPROVED_PRE_RESOLUTION` candidate manifest records all missing hashes, license decisions and NOTICE requirements.

## Actually executed V1119 checks
- Legacy **RED** 3 failed new pixel assertions (expected, exit 1), 8/11 others pass.
- Corrected staged test plus test-license policy: **11/11 PASS**, exit 0.
- New PowerShell/data safety checks (including fake release PASS and fake EPL approval): **10/10 PASS**, exit 0.
- Total new local checks **21/21 PASS** on corrected staged artifacts. These are **NOT product Unit/Security/Android PASS**.
- Real Git clone **FAIL exit 128**. Gradle, Android SDK/adb/emulator, PowerShell runtime, rights-cleared source-set/accepted ADR-006: unavailable; platform/build tasks **NOT RUN**.
- V1118 prior Python/JVM and V1115 Python70/Kotlin48 results **NOT rerun** this turn.

## P0 follow-up and release gates
First trusted full PUBLIC checkout or one justified authorized manual GitHub-hosted run with run/event SHA, HEAD/origin/main parity, strict `git fsck`, clean before/after, exit codes/log hashes. Then accept a single rights-cleared Gradle/KGP/AGP lineage and source-set/Android isolated-service graph, manually review JUnit EPL test-only scope or choose cleared alternative, resolve full strict dependencies/transitive SPDX/SBOM/NOTICE. Only then run **nonempty actual** host/device tasks on emulator/device and verify the contrasting pixels/malformed PDF. Complete V477–latest applicable PUBLIC regressions, product Build/Unit/Integration, Android/Windows/Ubuntu runtime/security/packaging/signing/rollback. Historical **51 Kotlin candidates BLOCKED** pending source ownership/PII/secrets/asset/provenance/license review; separate byte-exact recovery/reconstructed/new manifests.

All **11 production gates (Build, Unit, Integration, Android, Windows, Ubuntu, Security, Dependency Verification, License/SBOM/NOTICE, Packaging, Signing/Rollback) NOT RUN; 0/11 PASS**; PUBLIC reconstruction NOT RUN. PowerShell **0%** refers only to proven production gate PASS coverage, not overall product progress. Conditional scenario **12–24 weeks after** real checkout/rights/platform labs; hypothetical readiness 2026-11-11 → **2027-02-03 through 2027-04-28**, **not a committed FINAL date**.

ADR-005 isolated PoC; ADR-006 PROPOSED, not accepted. GPL-3.0 PDF Arranger code/fork/module/runtime prohibited, desktop Apache PDFBox structural and Android PdfRenderer viewer baseline retained, no Poppler/pikepdf or selected Android structural engine. PUBLIC commits `[skip ci]`, no force push/Actions, PRIVATE STRICT READ-ONLY. **PRODUCTION NOT FINAL**.
