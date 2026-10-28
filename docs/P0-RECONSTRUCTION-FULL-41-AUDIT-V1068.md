# V1068 — Full 41-entry historical reconstruction SHA-256 audit (READ-ONLY)

Date: 2026-10-28 ~04:00 TRT. **PRODUCTION NOT FINAL.**

## Scope and authority

Canonical writable repository: `ftmstr/Embasic-PDF-Editor-Build` PUBLIC main, starting HEAD `236817f230bf79d03902211464cb5eb8105de7e4`. Historical PRIVATE repository `ftmstr/uygulama-baslangic-sablonu` is **READ-ONLY**; no private code, assets, binaries, secrets, case data or third-party implementation copied here. This report publishes only low-risk file-path and status metadata. No source migration or license/secret clearance is claimed.

Historical manifest: `projects/embasic-pdf-editor/product/RECONSTRUCTION_SHA256SUMS.txt`, Git blob `e6b9daf909207c35a33a3201438a60aa67a4310b` (41 entries). Manifest-writing commit: `5ec86225eb9047324772ad2b2a1ae7b55a493e14` (2026-09-09). Pinned later PRIVATE snapshot: `e4e4b4f6ccd9d838b5ac5434b45fb8202d4ba786`.

## Executed audit — two distinct historical checkpoints

- **Pinned PRIVATE snapshot:** all **41/41** manifest paths fetched as base64-decoded bytes and SHA-256 computed: **22 MATCH, 19 MISMATCH, 0 NOT RUN**. This is a **historical integrity comparison**, not a successful reconstruction gate.
- **Manifest-writing commit:** 19 pinned-mismatching paths fetched again and SHA-256 computed: **10 MATCH, 9 MISMATCH**. The remaining 22 pinned-matching paths had identical Git blob IDs at both commits, establishing **32 MATCH, 9 MISMATCH, 0 NOT RUN** at manifest origin. Git tree comparison: 25 unchanged blob IDs, 16 changed.
- SHA-256 implementation was checked against standard empty-string and `abc` test vectors (**2/2 PASS**). Connector data was decoded as bytes, including the binary Gradle wrapper JAR; no text normalization was applied.
- **New P0 root cause:** Nine entries were already divergent **at the manifest-writing commit**. Later source changes explain some additional mismatches, but **cannot explain all historical divergence**. Do not call the full manifest merely “stale due to later edits”; the initial baseline itself requires provenance reconciliation. Do not rewrite the authoritative manifest blindly.

| # | Relative product path | Pinned snapshot | Manifest origin | Git blob changed since origin |
|---:|---|---|---|---|
| 1 | `ADR-001-RECONSTRUCTION-PROVENANCE.md` | MATCH | MATCH | NO |
| 2 | `ADR-002-DESKTOP-PDFBOX-BACKEND.md` | MATCH | MATCH | NO |
| 3 | `ADR-003-MONETIZATION-BOUNDARY.md` | MATCH | MATCH | NO |
| 4 | `DEPENDENCY_DECLARATIONS.md` | MISMATCH | MISMATCH | NO |
| 5 | `androidApp/README_RECONSTRUCTION.md` | MISMATCH | MATCH | YES |
| 6 | `androidApp/build.gradle.kts` | MISMATCH | MATCH | YES |
| 7 | `androidApp/src/main/kotlin/com/embasic/pdfeditor/AndroidPdfViewerActivity.kt` | MISMATCH | MATCH | YES |
| 8 | `androidApp/src/main/kotlin/com/embasic/pdfeditor/MainActivity.kt` | MISMATCH | MATCH | YES |
| 9 | `build.gradle.kts` | MISMATCH | MATCH | YES |
| 10 | `desktopApp/build.gradle.kts` | MISMATCH | MATCH | YES |
| 11 | `desktopApp/src/main/kotlin/com/embasic/pdfeditor/desktop/DesktopMain.kt` | MISMATCH | MATCH | YES |
| 12 | `desktopApp/src/main/kotlin/com/embasic/pdfeditor/desktop/DesktopPdfBackend.kt` | MATCH | MATCH | NO |
| 13 | `desktopApp/src/main/kotlin/com/embasic/pdfeditor/desktop/RenderGenerationGate.kt` | MATCH | MATCH | NO |
| 14 | `desktopApp/src/test/kotlin/com/embasic/pdfeditor/desktop/DesktopPdfBackendTest.kt` | MATCH | MATCH | NO |
| 15 | `gradle.properties` | MISMATCH | MATCH | YES |
| 16 | `gradle/wrapper/gradle-wrapper.jar` | MATCH | MATCH | NO |
| 17 | `gradle/wrapper/gradle-wrapper.properties` | MATCH | MATCH | NO |
| 18 | `gradlew` | MATCH | MATCH | NO |
| 19 | `gradlew.bat` | MATCH | MATCH | NO |
| 20 | `settings.gradle.kts` | MATCH | MATCH | NO |
| 21 | `shared/build.gradle.kts` | MATCH | MATCH | NO |
| 22 | `shared/src/androidInstrumentedTest/kotlin/com/embasic/pdfeditor/reconstructed/AndroidFileTokenLedgerStoreInstrumentedTest.kt` | MISMATCH | MISMATCH | YES |
| 23 | `shared/src/androidMain/kotlin/com/embasic/pdfeditor/androidpdf/AndroidPdfRecentRepository.kt` | MATCH | MATCH | NO |
| 24 | `shared/src/androidMain/kotlin/com/embasic/pdfeditor/androidpdf/AndroidPdfUriValidator.kt` | MATCH | MATCH | NO |
| 25 | `shared/src/androidMain/kotlin/com/embasic/pdfeditor/androidpdf/AndroidRecentPdfResolver.kt` | MATCH | MATCH | NO |
| 26 | `shared/src/androidMain/kotlin/com/embasic/pdfeditor/reconstructed/AndroidFileTokenLedgerStore.kt` | MISMATCH | MISMATCH | YES |
| 27 | `shared/src/commonMain/kotlin/com/embasic/pdfeditor/reconstructed/MonetizationPolicy.kt` | MATCH | MATCH | NO |
| 28 | `shared/src/commonMain/kotlin/com/embasic/pdfeditor/reconstructed/PdfRenderSizePolicy.kt` | MISMATCH | MATCH | YES |
| 29 | `shared/src/commonMain/kotlin/com/embasic/pdfeditor/reconstructed/TokenLedger.kt` | MISMATCH | MISMATCH | YES |
| 30 | `shared/src/commonMain/kotlin/com/embasic/pdfeditor/reconstructed/TokenLedgerStateCodec.kt` | MISMATCH | MISMATCH | YES |
| 31 | `shared/src/commonTest/kotlin/com/embasic/pdfeditor/integration/PdfViewerControllerIntegrationTest.kt` | MATCH | MATCH | NO |
| 32 | `shared/src/commonTest/kotlin/com/embasic/pdfeditor/pdf/PdfNavigationPolicyTest.kt` | MATCH | MATCH | NO |
| 33 | `shared/src/commonTest/kotlin/com/embasic/pdfeditor/reconstructed/MonetizationPolicyTest.kt` | MATCH | MATCH | NO |
| 34 | `shared/src/commonTest/kotlin/com/embasic/pdfeditor/reconstructed/PdfRenderSizePolicyTest.kt` | MISMATCH | MATCH | YES |
| 35 | `shared/src/commonTest/kotlin/com/embasic/pdfeditor/reconstructed/TokenLedgerStateCodecTest.kt` | MISMATCH | MISMATCH | YES |
| 36 | `shared/src/commonTest/kotlin/com/embasic/pdfeditor/reconstructed/TokenLedgerTest.kt` | MISMATCH | MISMATCH | NO |
| 37 | `shared/src/desktopMain/kotlin/com/embasic/pdfeditor/reconstructed/DesktopFileTokenLedgerStore.kt` | MISMATCH | MISMATCH | YES |
| 38 | `shared/src/desktopMain/kotlin/com/embasic/pdfeditor/time/EpochClock.jvm.kt` | MATCH | MATCH | NO |
| 39 | `shared/src/desktopTest/kotlin/com/embasic/pdfeditor/reconstructed/DesktopFileTokenLedgerStoreTest.kt` | MISMATCH | MISMATCH | NO |
| 40 | `tools/check_ad_privacy_consent_policy.py` | MATCH | MATCH | NO |
| 41 | `tools/check_monetization_ui_boundary.py` | MATCH | MATCH | NO |

## Fresh isolated PUBLIC tooling/PoC regression re-run

Exact tested bytes from the V1066 evidence ZIP match the six corresponding PUBLIC Git blob IDs at starting HEAD. Executed in the available Linux container: Python checkout tool **10/10 PASS**; Python migration preflight **14/14 PASS**; Python `py_compile` **PASS**; Kotlin/JVM `kotlinc` compile **PASS**; isolated editor smoke **45/45 PASS**. These are **NOT** product Build/Unit/Integration/Security or platform release gates.

Executable `git ls-remote` against PUBLIC GitHub still **FAIL (DNS: github.com)**. Trusted full checkout **NOT RUN**; source migration, V477–latest product regressions, PUBLIC reconstruction checksum convergence, strict dependency verification, resolved license/SBOM/NOTICE, real Gradle build and platform runtime **NOT RUN**. Historical starter 142/142 and policy 17/17 evidence reviewed (V555) but **NOT RUN** against PUBLIC. Historical PRIVATE PASS must not be transferred.

## Required P0 path

1. Obtain trusted complete PUBLIC checkout and verify clean HEAD/origin/main, non-shallow history, `git fsck --full --strict` and tool checks.
2. Preserve both historical snapshots and reconcile **nine origin mismatches** before addressing **ten additional later mismatches**. Determine source revision, authorizing evidence, privacy/secret/license/provenance disposition for each; preserve byte-exact vs reconstructed/new labels.
3. Complete safe two-surface source graph closure (product + recovered-source), Android source sets/merged manifest, and reviewed PUBLIC migration. Do not copy uncertain files.
4. Execute V477–latest regressions, reconstruction convergence, strict Gradle dependency verification, resolved licenses/SBOM/NOTICE, build/unit/integration, Android/Windows/Ubuntu runtime, security, packaging, signing and rollback gates.

## ADR-005 / PDF Arranger clean-room

ADR-005 immutable commonMain workspace remains **isolated Kotlin PoC**, not production Gradle/KMP integration. No PDF Arranger GPL-3.0 code, fork, modules or runtime dependency copied. No Poppler/pikepdf. Desktop Apache PDFBox structural backend and Android PdfRenderer viewer baseline unchanged. Android structural engine requires separate PoC/ADR with transitive license, ABI, package, performance, malformed and stress evidence. No premature Compose rewrite.

All PUBLIC commits use `[skip ci]`, no force push, no unnecessary Actions (blackout ended 2026-10-05 00:00 TRT). PRIVATE strictly READ-ONLY. **PRODUCTION NOT FINAL.**
