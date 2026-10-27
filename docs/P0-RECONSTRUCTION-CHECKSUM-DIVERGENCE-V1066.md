# V1066 — P0 reconstruction checksum divergence (READ-ONLY historical sample)

Date: 2026-10-28 02:00 TRT. **PRODUCTION NOT FINAL.**

## Authority and scope

Only `ftmstr/Embasic-PDF-Editor-Build` PUBLIC `main` is writable. The historical PRIVATE repository `ftmstr/uygulama-baslangic-sablonu` was inspected **READ-ONLY** at `e4e4b4f6ccd9d838b5ac5434b45fb8202d4ba786`. No PRIVATE implementation, assets, keys, case data, or third-party code were copied into PUBLIC. This document is independently authored audit metadata, **not** a license/privacy authorization or migrated source.

The historical PRIVATE `projects/embasic-pdf-editor/product/RECONSTRUCTION_SHA256SUMS.txt` (Git blob `e6b9daf909207c35a33a3201438a60aa67a4310b`) lists 41 paths. V1065 checked 41/41 *path existence only*. V1066 performed an actual SHA-256 content comparison on **three** selected UTF-8 text entries, pinned to the same PRIVATE commit. The remaining **38 entries were NOT RUN**, including the binary Gradle wrapper JAR.

## Actual sampled results

| Historical path suffix | Expected SHA-256 in manifest | Recomputed SHA-256 | Result |
|---|---|---|---|
| `product/shared/build.gradle.kts` | `8ed45b4e29e9d7683b6495196bbcda45d3691339bd41bdc993be6861cc26051d` | same | **MATCH** |
| `product/androidApp/build.gradle.kts` | `e8530e76e90ab5760a581bec28a6ecc96461c3b93130b778e153d5f8215ca506` | `549a79bd5edcebf07c85a6095c543037a3a1b7b69e7e8d23f79b45b1664c6396` | **MISMATCH** |
| `product/shared/src/commonMain/kotlin/com/embasic/pdfeditor/reconstructed/MonetizationPolicy.kt` | `91c751bfe32e35c038899b62a20002e8e71852ef6afebeeeef6808082ba66096` | same | **MATCH** |

SHA-256 was calculated from GitHub connector-returned UTF-8 file bytes using an independent SHA-256 implementation checked against standard `abc` and empty-input vectors; two positive manifest matches provide an additional control. This is a scoped API content audit, **not** trusted full Git checkout or product build evidence. Recheck from a trusted full checkout before any manifest repair.

## Interpretation and safe next action

**Historical reconstruction checksum convergence is demonstrably NOT achieved for this sampled PRIVATE snapshot.** The Android Gradle file is already known to participate in the incomplete Android source-set/manifest integration. The mismatch does not, by itself, establish which revision is correct or whether a change was unauthorized. **Do not rewrite the authoritative manifest to match current bytes blindly.**

1. Obtain trusted full PUBLIC checkout on a Git-capable host; current execution container still fails DNS resolution for `github.com`.
2. Inventory and independently review rights, privacy, secrets, SPDX/license, assets, dependency graph and provenance before moving any historical sources.
3. For any approved migration, verify *all* authoritative SHA-256 entries on trusted checked-out bytes, classify each as `byte_exact_recovery`, `reconstructed`, or `new_implementation`, and investigate each mismatch against history/ADR/recovery evidence. Preserve expected and observed hashes, Git blob IDs, and review disposition; never silently rebaseline.
4. Resolve shared and Android source-set closure and Android merged-manifest service policy only with real Gradle and runtime evidence. Run V477–latest verifier regressions, strict dependency verification, resolved License/SBOM/NOTICE and all platform release gates.

PUBLIC product Build/Unit/Integration/Android/Windows/Ubuntu/Security/Dependency Verification/License-SBOM-NOTICE/Packaging/Signing-Rollback: **all NOT RUN**. Reconstruction **FAIL for this historical three-entry sample; PUBLIC convergence NOT RUN**. No PRIVATE historical PASS is inherited.

PDF Arranger GPL-3.0 source/modules/implementation are prohibited. Desktop Apache PDFBox structural backend and Android PdfRenderer viewer remain baselines; no Poppler/pikepdf or Android structural engine selected. ADR-005 is an isolated clean-room Kotlin PoC, not product `commonMain` integration. All PUBLIC commits `[skip ci]`, no force push; no Actions dispatch. **PRODUCTION NOT FINAL.**
