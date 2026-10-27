# P0 — PUBLIC source migration dependency and release-gate map

**Date:** 2026-10-27  
**Status:** Planning evidence only — **PRODUCTION NOT FINAL**  
**Authority:** Only `ftmstr/Embasic-PDF-Editor-Build` (PUBLIC) `main` and `docs/STATUS.md` govern future work.

## Verified read-only discovery

The former development repository is **inactive and READ-ONLY**. Its tree at historical HEAD `e4e4b4f6ccd9d838b5ac5434b45fb8202d4ba786` exposed **399 product blobs** (1,563,857 total bytes according to the Git tree metadata), not an authorized migration or complete local checkout. This count is historical metadata, not a PUBLIC reconstruction PASS.

**Critical cutover dependency:** The historical `shared` Gradle configuration references Kotlin sources outside the product directory, under the separate `recovered-source/shared` area. Copying only the historical `product` subtree would therefore create an **incomplete source graph**. This must be handled by a reviewed, explicit two-provenance intake plan, not by blindly copying all files or silently rewriting imports.

Historical direct declarations observed read-only: Kotlin 2.3.20, Android Gradle Plugin 8.13.2, Gradle 8.13, JDK 17, Android compile/target SDK 36, coroutines 1.11.0, desktop PDFBox 3.0.8. These are **declared historical coordinates**, not a resolved graph, license clearance, or successful PUBLIC build.

The historical `RECONSTRUCTION_SHA256SUMS.txt` is stale; the historical `THIRD_PARTY_NOTICES.partial.md` explicitly is not distribution-complete. Neither can be promoted to PUBLIC PASS by copying them.

## Required safe migration sequence

1. Obtain a **trusted full, non-shallow, clean checkout** of the PUBLIC repository. Record `HEAD`, index, branch, worktree state, and exact toolchain versions. A GitHub API tree or reconstructed collection of individual blobs is **not** an equivalent checkout.
2. Inspect candidate historical product and recovered-source inventories **read-only**, with an explicit allowlist. Before any PUBLIC write, review every admitted file for credentials, signing keys, private URLs, real case data, personal information, binary/asset rights, SPDX/license obligations, and source provenance. Exclude unresolved candidates.
3. Record separate manifests for **byte-exact recovered** and **reconstructed/new** sources. A recovered-source path alone is not evidence of byte-exact recovery; compare bytes against authoritative recovery checksums and origin records. Preserve distinctions and reject any unsupported recovery credit.
4. Review the historical Gradle source-set path relationships. Choose a **reviewed** PUBLIC layout that does not depend on PRIVATE checkout paths, and update source-set references in one atomic, reviewable migration. Verify no missing or ambiguous sources. Do not invent or silently vendor dependencies.
5. Re-run V477 through latest applicable verifier regressions in the trusted PUBLIC checkout. Regenerate and verify reconstruction checksums on the exact accepted PUBLIC source tree; do not copy the stale historical manifest as an authoritative PASS.
6. Run strict dependency verification and export actual resolved build/runtime dependency graphs. Generate complete license inventory, SBOM, and THIRD_PARTY_NOTICES from resolved artifacts; review transitive licenses, notices, and hashes. Partial direct-dependency lists are insufficient.
7. Run real Gradle build, unit/integration, Android instrumentation/device, Windows and Ubuntu runtime/install/upgrade/uninstall, security/malformed/stress, packaging, signing, and rollback gates. Report **PASS / FAIL / NOT RUN** individually, with commands, exit codes, artifacts, and SHA-256 evidence.

## Clean-room and architecture boundary

The PUBLIC `prototypes/common-editor-workspace` is independently authored, isolated Kotlin/JVM proof-of-concept code. It is **not** a production `commonMain` integration. ADR-005 calls for immutable, platform-neutral editor state, stable source/page references, bounded history, and declarative export; platform URI, PDFBox, Swing, Compose, Path, or renderer handles must not leak into the domain.

Do **not** copy/fork/use GPL-3.0 PDF Arranger implementation or its modules. Do not add Poppler/pikepdf as runtime dependencies under current policy. Keep desktop Apache PDFBox structural backend and Android PdfRenderer viewer baseline; choose no Android structural engine without a separate ADR and PoC covering license, transitives, ABI, package size, performance, malformed inputs, and stress.

## Execution and publication policy

- GitHub writes **only** to PUBLIC `ftmstr/Embasic-PDF-Editor-Build`; PRIVATE remains READ-ONLY, never deleted or modified by this workflow.
- Every commit includes `[skip ci]`; never force-push. Historical Actions blackout ended 2026-10-05 00:00 TRT, but do not trigger Actions merely to generate planning evidence.
- Tests only PASS when executed on the explicitly identified bytes. Prior PRIVATE results do not certify PUBLIC. The current isolated PoC smoke tests do not certify production Build/Unit/Integration/Security.
- Drive backups and API tree metadata are supporting evidence, **not** a trusted Git checkout or production release certification.
- **PRODUCTION NOT FINAL** until all required release gates are proven.
