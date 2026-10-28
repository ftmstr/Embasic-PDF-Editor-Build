# V1080 — Historical Android app + shared source-set closure (metadata-only)

**2026-10-28 ~15:03 TRT — PRODUCTION NOT FINAL**

## Canonical and provenance

- Sole writable target: `ftmstr/Embasic-PDF-Editor-Build` (PUBLIC). Starting main `aca9763ca6cd282f89c2ffa4516fe6ba5799e3c4` / `docs/STATUS.md` V1079. Historical PRIVATE `ftmstr/uygulama-baslangic-sablonu` at `e4e4b4f6ccd9d838b5ac5434b45fb8202d4ba786` inspected **READ-ONLY** through GitHub GET; no PRIVATE write, Actions dispatch or source-byte publication.
- The GitHub historical tree query was **not truncated**. This document and new code publish only historical path/size/Git blob metadata, never PRIVATE Kotlin implementation bytes, assets, secrets, keys, documents or unreviewed binaries.
- Historical recovered-source bytes are **NOT** admitted to PUBLIC. Their source-byte SHA-256, rights, licensing, PII/secret and provenance clearance remain **NOT VERIFIED**. Historical PRIVATE V519 tests, 41/41 historical SHA, starter 142/142 and policy 17/17 are **not PUBLIC product PASS**.

## Concrete source-set closure finding

The historical `product/shared/build.gradle.kts` declares `kotlin.srcDir("../../recovered-source/shared/src/commonMain/kotlin")` and `kotlin.srcDir("../../recovered-source/shared/src/androidMain/kotlin")`. Consequently, the recovered Android app's seven Kotlin files **cannot** be treated as a complete independently buildable migration; the Gradle-configured shared source-set roots include **28 additional Kotlin files**.

| Historical recovered Kotlin root | Files | Git-tree-reported bytes | Admission |
| --- | ---: | ---: | --- |
| `recovered-source/androidApp/src/main/kotlin/` | 7 | 57,915 | BLOCKED |
| `recovered-source/shared/src/androidMain/kotlin/` | 6 | 7,107 | BLOCKED |
| `recovered-source/shared/src/commonMain/kotlin/` | 22 | 69,750 | BLOCKED |
| **Total** | **35** | **134,772** | **35/35 BLOCKED** |

The historical product also contains `shared/src/commonMain` 12 Kotlin files and `shared/src/androidMain` 4 Kotlin files; these are additional product dependencies, not included in the 35 recovered candidates. Kotlin symbol imports were inspected **READ-ONLY**: the recovered app references `AndroidPdfSourcePicker`, `AndroidPdfViewerPolicy`, `PdfPlatformServices`, `PdfViewerController`, `AppResult`, `PdfSelectionValidator`, and search/render policy types from the shared roots. A source-file inventory and import inspection are **not** a compiler-resolved symbol graph, and do not prove that all historical code builds.

The historical product and recovered Android manifests collide by destination path. Never overwrite the product manifest. After per-file clearance, review an additive service declaration with fully qualified `com.embasic.pdfeditor.android.isolated.IsolatedPdfRendererService` and verify actual manifest merge/runtime.

## New PUBLIC executable gate and actual tests

- `tools/public_source_set_closure.py`: fail-closed **metadata-only** intake check for the pinned historical tree, 35 unique safe paths, exact source-set counts and tree-reported byte totals, valid Git blob SHA-1 metadata, all five clearance flags `NOT VERIFIED`, all admissions `BLOCKED`, no unsupported byte-exact recovery claims and no source-byte inclusion.
- `tests/test_public_source_set_closure.py`: **16/16 PASS** local execution, including missing/duplicate/unsafe paths, wrong totals, unauthorized admission, bogus SHA, unsupported provenance and noncanonical target negative tests.
- On the 35-row historical **metadata-only** manifest: `python3 tools/public_source_set_closure.py historical_recovered_35_blocked.json` -> **PASS_METADATA_ONLY, 35 candidates, 35 blocked, 134,772 historical tree bytes**. This is **not** migration PASS, product Build PASS, Security PASS or License PASS.
- Re-executed prior PUBLIC-Git-blob-scoped Python regressions from V1079 ZIP: **42/42 PASS**, exit 0; isolated Kotlin/JVM `kotlinc` compilation exit 0 and smoke **45/45 PASS**, exit 0. New PUBLIC tool and test exact `git hash-object` values matched GitHub read-back (2/2). Python `py_compile` PASS.
- Direct executable `git ls-remote` to PUBLIC: **FAIL** DNS (exit 128); trusted complete Git checkout and GitHub-hosted manual workflow **NOT RUN**. GitHub Actions read-only API returned **0 runs**. No Actions triggered.

## P0 next — stop extending verifiers

1. **Obtain a real trusted full PUBLIC checkout** in an authorized Codex/runner environment; execute existing manual-only workflow once if authorized. Capture event SHA, HEAD, origin/main, clean index, non-shallow, `git fsck`, command exit/log SHA-256.
2. Perform rights/license/secret/PII/provenance review for **all 35 recovered candidates** and the historical product dependency graph. Do not copy 7 Android app files alone; do not publish any blocked source. Separate byte-exact recovery (source-byte SHA-256 and authoritative manifest required) from reconstructed/new implementation.
3. After source approval, integrate a complete reviewed Gradle source-set layout and additive Android manifest, run V477–latest regressions, PUBLIC reconstruction convergence, strict resolved dependency verification, transitive License/SBOM/NOTICE, then actual Gradle/KMP and Android/Windows/Ubuntu/runtime/security/packaging/signing/rollback gates. Do not use this metadata validator as a substitute for those tests.

**Release gates:** Build, Unit, Integration, Android, Windows, Ubuntu, Security, Dependency Verification, License/SBOM/NOTICE, Packaging, Signing/Rollback: **all NOT RUN; 0/11 PASS**. PUBLIC Reconstruction **NOT RUN**. The 0% figure is verified release-gate coverage, not overall project completion. The earlier 12–24 week range remains conditional on trusted checkout, rights and platform test infrastructure; no committed FINAL date.

**Architecture:** ADR-005 immutable editor domain remains an isolated Kotlin prototype, not production `commonMain`. No PDF Arranger GPL-3.0 source copied/forked or runtime dependency; no Poppler/pikepdf. Desktop PDFBox structural and Android PdfRenderer viewer baselines unchanged. No Android structural engine without independent PoC + ADR + licensing/transitives/ABI/package/performance/malformed/stress evidence.

All PUBLIC writes use `[skip ci]`, never force push. PRIVATE remains READ-ONLY. Actions blackout ended 2026-10-05 00:00 TRT; avoid unnecessary dispatch. **PRODUCTION NOT FINAL.**
