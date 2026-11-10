# V1118 — Android-KMP AGP 9.1 test-compilation API and staged nonempty test evidence

**2026-11-10 ~22:23 TRT. PRODUCTION NOT FINAL.**

## PUBLIC authority and actual checkout result
- Canonical writable repository: **PUBLIC** `ftmstr/Embasic-PDF-Editor-Build`, starting `main` `054d03c877d178917934fb3935751cf403c0ba32` (V1117), `docs/STATUS.md` V1117. Verified current PUBLIC tree, Actions (GET: **0 runs**), latest V1117 native Drive Rapor/Codex and uploaded authoritative starter/policy references. Historical PRIVATE `ftmstr/uygulama-baslangic-sablonu` **STRICT READ-ONLY**; no PRIVATE writes or copying.
- Actually tried `git ls-remote` and `git clone --no-tags --no-single-branch --branch main` against the exact PUBLIC HTTPS URL. Both **FAIL DNS exit 128** (cannot resolve `github.com`); the fresh clone error log SHA-256 is `c2a0eec1de24810fab5e5113fa503c94724865c1c37b04e2de0d70df25d41c1c`. The clone did **not** produce a checkout directory. Current GitHub connector has no manual workflow dispatch action; there are no hosted workflow runs.
- Therefore trusted non-shallow full PUBLIC checkout, remote SHA/event parity, `git fsck`, clean before/after, complete V477–latest regressions and product Gradle build **NOT RUN**. An API blob or ZIP is **not** a full Git checkout.

## New, version-scoped **official API resolution** (not a Gradle runtime test)
The **Android Gradle Plugin 9.1** `KotlinMultiplatformAndroidLibraryExtension` API reference explicitly declares **all four** members:
- `withHostTest(action)` and `withHostTestBuilder(action)`: both supported in AGP 9.1. Default host compilation `hostTest`, source set `androidHostTest`, and source-set tree `test`; the builder permits changing defaults.
- `withDeviceTest(action)` and `withDeviceTestBuilder(action)`: both supported in AGP 9.1. Default device compilation `deviceTest`, source set `androidDeviceTest`, and source-set tree **`null`** (does **not** inherit `commonTest`). A builder can explicitly set `sourceSetTreeName = "test"`. It must be decided whether device tests should deliberately inherit `commonTest`.
- API explicitly supports **one compilation of each test type**; blindly combining both opt-ins for the same type is a configuration error risk.

Official source: https://developer.android.com/reference/tools/gradle-api/9.1/com/android/build/api/dsl/KotlinMultiplatformAndroidLibraryExtension
General setup: https://developer.android.com/kotlin/multiplatform/plugin

This resolves the **documentation-level method-name ambiguity** recorded in V1117. It does **not** establish a compiled plugin binary, actual `:shared:tasks --all` result, KGP/AGP resolution, Android test execution or release acceptance. The V1117 `androidLibrary {}` → `android {}` pilot remains **UNAPPROVED/DRIVE ONLY**. No source migration or Gradle/dependency change was made to PUBLIC.

## New original nonempty test sources, quarantined in Drive evidence only
To give the authorized Gradle host actionable, independent source-set fixtures, created the following **original, staging-only** Kotlin files. These do not copy code from GPL PDF Arranger, PRIVATE or actual PDF documents:
1. `staged/src/androidHostTest/kotlin/org/embasic/pdfeditor/acceptance/EditorWorkspaceAndroidHostTest.kt`: **2 distinct annotated tests** using `kotlin.test`: exact Unicode source/page ID preservation and rejection above the domain's 10,000-page bound. SHA-256 `62d05bf3c396b20741faa00ec8ba832fef000d548518137a76f5e352f6a937e8`.
2. `staged/src/androidDeviceTest/kotlin/org/embasic/pdfeditor/acceptance/PdfRendererAndroidDeviceSmokeTest.kt`: **2 distinct annotated tests**: generate a synthetic one-page PDF with platform `PdfDocument`, render it with `PdfRenderer`; reject a locally generated malformed PDF. Explicit bitmap, file descriptor and cache-file cleanup. SHA-256 `13f0d89afb47177de9c3fd5495a062a83b1b3327581f01ef1e37cf961510a3b4`.
3. `staged/jvm-preflight/HostPreflight.kt`: separate **main-based JVM-only** execution of five Unicode/upper-bound/selection behaviors, *not* the JUnit/Kotlin-test host source set. SHA-256 `30da2d2c40a2b89dd6d02e234c62dca3afdd970d6b27ee49ac0c797e0f922b62`.

Preflight used exact current PUBLIC independent domain prototype source: Git blob `cc20f008a4a1efe48688b69ca5293585ab9acbd5` **MATCH** (source SHA-256 `8a92995439cd82bca52ca842c970a4d5585eaf51b6a030422451a3e8b32a24a6`). This model is **not** a rights-cleared PDF Editor product sourceSet or working structural PDF backend.

### Actually executed local checks
- `kotlinc -J-Xmx768m EditorWorkspace.kt staged/jvm-preflight/HostPreflight.kt -include-runtime -d <isolated>/host-preflight.jar`: **PASS exit 0**; `java -Xmx512m -jar ...`: **5/5 PASS exit 0**. These are isolated **JVM preflight scenarios**, not Gradle `androidHostTest`.
- New stdlib Python staged-source admission tests `python -m unittest discover -s tests -p 'test_*.py' -v`: **8/8 PASS exit 0**, checking the current source Git blob, nonempty distinct host/device annotated tests, synthetic PDF-only fixtures, resource cleanup, staged/not-approved status and no shipped secrets.
- Real Android host/device Gradle compilation and test runner: **NOT RUN**. `gradle`, `pwsh`, `adb`, `sdkmanager`, actual approved wrapper and Android SDK/emulator are unavailable in this runtime. No JUnit/AndroidX dependencies were downloaded or approved. Device test might need changes after real Android compile/run; it is not called passing.
- Historical V1117 **12/12 candidate** and **8/8 dashboard** checks, V1115 Python **70/70** and Kotlin PoC **48/48** are **NOT re-executed** this turn and are not promoted to release gates.

## Enforceable acceptance path on a real authorized Gradle/Android host
1. **Trusted full PUBLIC checkout** with strict `git fsck`, branch/origin/main/remote/event SHA, clean before/after, logs and hashes. STOP on DNS/error, don't use ZIP as checkout.
2. Rights/secret/PII/SPDX and transitive asset/dependency clearance for any imported source. Historical 51 Kotlin candidates **BLOCKED**. ADR-006 still **PROPOSED**, choose one resolved Gradle/KGP/AGP matrix and reviewed test-sourceSet approach before applying any draft.
3. Download and authenticate Gradle distribution/wrapper JAR using publisher hashes/signatures; discover **real** `./gradlew --dependency-verification strict :shared:tasks --all`. Confirm actual source-set compilations for **both** host/device and explicitly verify intended `commonTest` inheritance. Generated NO-SOURCE or SKIPPED tasks are **NOT PASS**.
4. Review/license exact AndroidX instrumentation registry and JUnit/Kotlin test dependencies, update strict verification metadata from real resolved graphs, SBOM/NOTICE and negative security checks. Then compile and execute **nonempty** host tests and Android device tests on a real emulator/physical device, retaining test counts/exit/log/artifact hashes and any required revisions.
5. Complete V477–latest PUBLIC regressions, byte-exact versus reconstructed/new provenance reconciliation, build, unit/integration, desktop PDFBox and Android PdfRenderer runtime tests, Windows/Ubuntu installer/runtime, stress/malformed, packaging/signing/rollback.

## Release gates and time claims
Build, Unit, Integration, Android, Windows, Ubuntu, Security, Dependency Verification, License/SBOM/NOTICE, Packaging and Signing/Rollback: **ALL NOT RUN (0/11 PASS)**. PUBLIC reconstruction **NOT RUN**. The PowerShell dashboard must show **0% verified release gate coverage, NOT overall completion**; true Windows PowerShell runtime **NOT RUN**.

Conditional, nonbinding planning window: **12–24 weeks only after** real checkout, source rights and Android/Windows/Ubuntu laboratories are ready. Hypothetically ready on 2026-11-10 → 2027-02-02 through 2027-04-27, but prerequisites are not met; **no committed FINAL date**.

ADR-005 immutable domain remains isolated PoC, not product commonMain. GPL-3.0 PDF Arranger implementation/fork/module/runtime forbidden. Desktop Apache PDFBox structural and Android PdfRenderer viewer baselines preserved; no Poppler/pikepdf or preapproved Android structural engine. Only PUBLIC docs commits `[skip ci]`; no force push or Actions dispatch. PRIVATE **STRICT READ-ONLY**. **PRODUCTION NOT FINAL**.
