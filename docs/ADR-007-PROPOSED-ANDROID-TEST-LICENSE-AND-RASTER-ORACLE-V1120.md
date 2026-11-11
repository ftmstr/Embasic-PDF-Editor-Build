# V1120 — Clean-room raster oracle prototype and test-runner license decision ADR-007 (PROPOSED)

**2026-11-11 TRT • PRODUCTION NOT FINAL**  
**Canonical PUBLIC** `ftmstr/Embasic-PDF-Editor-Build` main, starting HEAD `3d64bb6fd826d17730ffcac3f4583a4146faa8b4`.

## P0 network checkout / hosted workflow: still blocked

- Read PUBLIC `main`, `docs/STATUS.md`, tree, GitHub Actions and latest native Drive V1119 Rapor/Codex. There were **0 Actions runs**. Connected GitHub tools can fetch and write PUBLIC files but **cannot dispatch** the existing manual-only workflow; no hosted workflow was started. Historical PRIVATE `ftmstr/uygulama-baslangic-sablonu` remains **STRICT READ-ONLY**.
- Actually ran canonical PUBLIC `git ls-remote`: **FAIL exit 128**, unable to resolve github.com. Then a separate real `git clone --no-tags --no-single-branch --branch main`: **FAIL exit 128**, no checkout. Clone stderr SHA-256 `f1a0ef891b3c90bb379e759e3b2929daf6e9506236b126029cc89ea3411887a5`.
- Thus trusted full non-shallow PUBLIC checkout, object `git fsck`, remote/HEAD/event SHA comparison, clean before/after, complete V477–latest verified regressions **NOT RUN**. A standalone file fetched over GitHub API is not a full trusted checkout.

## Substantive new PUBLIC-source engineering — original license-free raster sample oracle

Two **new, independently authored** source files were added only under the repository's already-public **isolated** `prototypes/common-editor-workspace` tree, **not** a rights-gated production Gradle module, not historical PRIVATE source and not GPL PDF Arranger:
- `src/commonMain/kotlin/org/embasic/pdfeditor/workspace/RasterContrastOracle.kt`: platform-neutral ARGB model and fail-closed two-point contrast evaluation, no Android/JVM/PDFBox handle, no external dependencies. Explicit bounds, 16,777,216-pixel image cap using 64-bit multiplication, distinct sample positions, almost-opaque alpha, dark/bright thresholds and minimum 130 luma difference. Source SHA-256 `8ee4e848bd25fec0ab1545fb059ca0cd03a8ce33ff7284b9defa81d12e64e8ce`, PUBLIC Git blob `51300c5d7e2bdf437d0a8f5a613e6994b4edbc07`.
- `src/commonTest/kotlin/org/embasic/pdfeditor/workspace/RasterContrastOracleSmoke.kt`: dependency-free standalone JVM smoke tests, including normal black/white, blank, inverted, unreplaced magenta sentinel, transparent, coordinate overflow, incorrect contrast, anti-alias and **4,000 deterministic equal-gray negative variants**. SHA-256 `7b447bda043f0036c585c2b0fa7b5ae4d35db1c085c818007554d40c9f64af05`, PUBLIC Git blob `faa5c3baca0892f0b97767ce48ff1550b971fd10`.

**Test-first execution:** before adding implementation, `kotlinc` on the new smoke failed as expected for missing oracle symbols (**RED exit 1**). After adding implementation, `kotlinc -J-Xmx768m ... -include-runtime` **PASS exit 0** and `java -Xmx256m -jar ...` **15/15 PASS exit 0** (4,000 inner negative samples), using local OpenJDK 21 and Kotlin/JVM compiler 1.9.0. Exact local Git blobs were compared against GitHub `fetch_file` after publication: **2/2 MATCH**. Compiled jar used solely for local testing, **not redistributed** because runtime notice/license verification for that JAR is not a production release task.

**Important limitations:** This oracle takes caller-supplied ARGB samples; it **cannot authenticate their provenance**. Android platform adapter must actually read post-`PdfRenderer.Page.render` bitmap pixels at meaningful interior/exterior locations and bind samples to the correct source/page/render frame; no fake samples, no release gate from two-point inspection. This is a *limited secondary acceptance oracle*, not pixel-perfect regression nor structural PDF correctness. Kotlin 1.9/JVM smoke is not the product Kotlin 2.4/KMP/Android build.

## ADR-007 PROPOSED: Android instrumentation test dependencies and EPL scope

**Decision state:** `PROPOSED / FAIL-CLOSED / NO JUNIT OR ANDROIDX APPROVAL`.

The user's uploaded `11-ACIK-KAYNAK-LISANS-POLITIKASI(2).md` §2 defaults runtime/source licenses to Apache-2.0, MIT, BSD-2/3, ISC, Zlib. §7 separates **build tools not embedded in the application** from runtime, but does not auto-approve unknown licenses or eliminate third-party redistribution obligations. This distinction is crucial: a test runner may be absent from the *production APK* but packaged in a separately distributed **instrumentation test APK**. Both the product runtime closure and test APK closure must be measured independently.

- Upstream official JUnit 4 project license and Maven Central `junit:junit:4.13.2`: **EPL-1.0**. This SPDX is **outside the default allowlist**, so `BLOCKED_TEST_ONLY_EXCEPTION_REVIEW`; do **not** silently approve on the basis of test-only scope. Official JUnit upstream lists `org.hamcrest:hamcrest-core:1.3` (New BSD) as a compile dependency; actual resolved coordinates/artifact checksums/NOTICE **NOT RUN**.
  - https://junit.org/junit4/license.html
  - https://central.sonatype.com/artifact/junit/junit/4.13.2
  - https://junit.org/junit4/dependencies.html
- AndroidX Test official release page shows stable `androidx.test:runner:1.7.0`, `androidx.test:core:1.7.0`, `androidx.test.ext:junit:1.3.0`. This confirms *published candidate versions*, **not their full resolved Gradle graph, exact binary hashes, individual SPDX labels, or redistribution rights**. All remain `PENDING_RESOLVED_LICENSE_SHA_SBOM_NOTICE`; no artifact was downloaded or linked.
  - https://developer.android.com/jetpack/androidx/releases/test

**Candidate paths, neither accepted yet:**
1. Review a **narrowly documented test-only EPL exception**, proving `junit:junit` and its transitives are absent from *production* compile/runtime/package, and separately accounting for test APK lab distribution, license notices, modifications and CI cache. Require explicit project policy approval before adding any artifact.
2. Prototype an **Android platform `Instrumentation`-only smoke runner** with no additional JUnit/AndroidX dependency. It still requires an exact Android test-APK manifest/runner, Android SDK/Gradle task wiring, actual emulator/device execution, and review of any platform/test APK licenses. No source or claim of success for this alternative was added. It must **not** be treated as an Android PASS without real device/runtime evidence.

**Do not choose a test framework solely from a POM snippet.** On an authorized networked Gradle host, pin exact accepted toolchain ADR-006, then `./gradlew --dependency-verification strict :shared:dependencies` (only if actual task exists) and relevant `dependencyInsight` for Android host/device **and** production variants; generate separate *resolved* manifest, SHA256, SPDX, dependency/NOTICE graph, license admission decision and SBOM for each variant. Unknown/forbidden dependency fails closed, no automatic waiver. Product and test APK must be checked separately for transitive test libraries.

## Remaining work and the actual release status

**11/11 production release gates are NOT RUN (0 PASS):** Build, Unit, Integration, Android, Windows, Ubuntu, Security, Dependency Verification, License/SBOM/NOTICE, Packaging and Signing/Rollback. PUBLIC reconstruction NOT RUN. No actual Gradle, Android SDK/adb/emulator, PowerShell, full product source/wrapper or Windows host was available. Historical 51 Kotlin candidates remain BLOCKED pending ownership/PII/secret/asset/SPDX/transitive/provenance; ADR-006 is PROPOSED; ADR-005's immutable workspace remains a prototype.

Next P0: genuine authorized full PUBLIC checkout or a justified manual-only Actions run; decide test-runner/license scope in an accepted follow-up ADR, rights-clear source intake, strict resolved artifacts, real nonempty Android host/device tests with verified post-render pixels, full V477–latest regression chain and Windows/Ubuntu/Android package/security/install/sign/rollback tests.

PowerShell **0/11 = 0% verified production gate coverage**, not overall project completion. Conditional **12–24 weeks only after** trusted full checkout, rights and all platform labs are ready. Hypothetical readiness on 2026-11-11 would imply **2027-02-03 to 2027-04-28**, not a delivery promise. Desktop Apache PDFBox structural and Android PdfRenderer viewer baseline unchanged; GPL-3.0 PDF Arranger source/runtime and Poppler/pikepdf prohibited.

**PUBLIC only, every commit `[skip ci]`; no force push, no unnecessary Actions, PRIVATE STRICT READ-ONLY. PRODUCTION NOT FINAL.**
