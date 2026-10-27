# Embasic PDF Editor — Public Repository Status

Date: 2026-10-27 (Europe/Istanbul)

## Authority

- **Canonical destination:** `ftmstr/Embasic-PDF-Editor-Build` (PUBLIC), default branch `main`.
- The previous development repository is an **inactive, read-only historical reference**. Do not make commits to it or delete it automatically.
- This repository was empty before the public transition. This status is not a continuation of the former repository's checkpoint or test certification.

## Current qualification status

- Public repository bootstrap: complete (documentation only).
- Source migration with secret/license/provenance checks: **NOT RUN**.
- Byte-exact recovery verification against authoritative manifests: **NOT RUN** in this public repository.
- Reconstructed/new implementation source verification: **NOT RUN** in this public repository.
- Trusted complete Git checkout: **NOT RUN** in this public repository.
- V477-to-latest regression suite: **NOT RUN** in this public repository.
- Gradle strict dependency verification / resolved graph: **NOT RUN**.
- License / SBOM / THIRD_PARTY_NOTICES completeness: **NOT RUN**.
- Build / unit / integration / Android / Windows / Ubuntu: **NOT RUN**.
- Security / installers / signing / rollback: **NOT RUN**.

**PRODUCTION NOT FINAL.** No release binaries, package or runtime validation are claimed.

## Safe public migration sequence

1. Determine an exact, reviewed source inventory (binary and secret exclusions; licensing and provenance).
2. Establish a trusted checkout of this PUBLIC repository and verify HEAD, index, and clean tree.
3. Import only approved sources, preserving byte-exact recovery and reconstructed/new provenance separately.
4. Recompute file hashes from a trusted checkout; reconcile the reconstruction manifest, never falsely declare stale evidence converged.
5. Run regression tests, strict Gradle dependency verification, license/SBOM/NOTICE checks and actual platform build/runtime tests.
6. Address ADR-005 workspace immutable state and PDF source-identity security findings with RED → FIX → GREEN evidence before release.

## Architectural and licensing constraints

ADR-005: shared `commonMain` domain types, immutable editor state, bounded history, no Android URI, PDFBox, Swing, Compose, Path, or bitmap handles leaking into domain.
Do not copy PDF Arranger GPL-3.0 code. Keep Apache PDFBox for desktop structural operations and Android PdfRenderer as Android viewing baseline; no unapproved Poppler/pikepdf. Android structural engine requires separate ADR/PoC/license/security/performance proof.

Commit policy: `[skip ci]`, no force push. The historical Actions blackout ended 2026-10-05 00:00 TRT, but no Actions runs should be triggered merely to initialize this repository.

## Latest verified PUBLIC state

This document reflects the transition/bootstrap only. It must be amended upon new verified public development work. The former private repository's V519 and later independent test reports do not become public-repository PASS results by reference.

## V1056 — 2026-10-27 PUBLIC migration preflight

- Read-only historical PRIVATE inventory: product 399 blobs, recovered-source 39 blobs; these are **not** migrated files or verified PUBLIC recovery.
- Independently authored PUBLIC `tools/public_migration_preflight.py` and `tests/test_public_migration_preflight.py`; no PRIVATE/PDF Arranger implementation copied.
- **13/13 synthetic Python unit tests PASS**, `py_compile` PASS on isolated locally authored bytes; GitHub blob identities and content read-back match the tested files. These are *scoped tooling tests*, **not** product Unit/Security gate PASS.
- `docs/PUBLIC-MIGRATION-INTAKE.md` documents the inventory, mechanical preflight limitations, rights/privacy/license review requirement, and clean-room boundary.
- Trusted executable PUBLIC checkout attempt **FAIL (DNS: github.com, git exit 128)**. Actual full checkout, source migration, reconstruction checksum convergence, Gradle, platform build/runtime, resolved license/SBOM/NOTICE, packaging/signing/rollback remain **NOT RUN**.
- Historical PRIVATE starter 142/142 and policy 17/17 were **NOT RUN** on PUBLIC. No PRIVATE writes. No Actions triggered. PUBLIC commits include `[skip ci]`; no force-push.
- **PRODUCTION NOT FINAL.** No public production binaries or migration authorization.

## V1057 — 2026-10-27 hardlink admission regression

- PUBLIC main was `0744ae21d8e8b5a1cebbd8a6dff351f5b5a54c49` at the beginning of this turn; this is a **PUBLIC** change, with PRIVATE read-only.
- Verified PUBLIC tooling/test bytes against the earlier evidence ZIP using `git hash-object`: `ccabdbd221dad8e266c5a0e57c3426bd84672a35` / `98fe48d609fe1d7e763b870af0261455664599af`. Re-ran existing 13 tests: 13/13 PASS.
- A real local hardlink pointing outside the candidate directory passed the prior preflight despite being a multi-link inode. New regression reproduced this gap: 1 expected FAIL (14 tests, exit 1).
- Small fail-closed fix rejects `st_nlink != 1` and detects changed source identity/size/mtime around read. New isolated regression: **14/14 PASS** (exit 0), `py_compile` PASS; updated local Git blob IDs: tool `cb30b28fa4debeeb8f21a86e0e1ba758d113c90a`, test `824bff3a3e6e51c82af7b3bfc9eaf16164120c9f`. GitHub updated blobs were checked against these local identities.
- **Limitations:** This is a best-effort offline mechanical preflight, not an atomic file-descriptor walk, race-proof intake, trusted checkout, legal/privacy clearance, or release gate. Multi-link rejection may conservatively reject safe candidates; human review still required. No PRIVATE files migrated.
- `git clone` PUBLIC still **FAIL (DNS / exit 128)** in the executable environment. Trusted full checkout, V477–latest regressions, reconstruction convergence, strict Gradle dependency verification, resolved license/SBOM/NOTICE, product build/unit/integration, Android/Windows/Ubuntu, security, packaging and signing/rollback all **NOT RUN** in PUBLIC. Historical PRIVATE security/reconstruction failures remain unresolved; do not promote historical PASS.
- PDF Arranger GPL-3.0 implementation was not copied; ADR-005 is a historical architecture reference, not a completed PUBLIC implementation. Desktop PDFBox and Android PdfRenderer remain planned baselines.
- GitHub Actions not triggered; PUBLIC commits use `[skip ci]`; no force push; **PRODUCTION NOT FINAL**.

## V1058 — 2026-10-27 18:00 TRT — isolated clean-room workspace PoC

- Starting canonical PUBLIC HEAD: `01e0e32866be9d0e31bd032818d8132fba93a5d7`; PRIVATE remains strictly READ-ONLY.
- Added **independently authored** `prototypes/common-editor-workspace/` Kotlin domain PoC, its isolated smoke harness, and README. This is **not integrated** into Gradle or production commonMain and imports no PRIVATE implementation or PDF Arranger GPL-3.0 code.
- Scope: `SourceDocumentRef`, `EditorPageRef`, `SelectionState`, `EditorDocumentState`, `EditorAction`, `EditorExportPlan`, `EditorHistory`; reducer supports import/move/rotate/duplicate/delete/select. Opaque source IDs, declarative export plan, defensive collection copies, snapshot-count-bounded undo/redo. No PDFBox, Android URI, Swing, Compose, renderer or filesystem handles in domain.
- Actual isolated execution: `kotlinc-jvm 1.9.0` with JRE 21 compiled the locally authored Kotlin sources (exit 0); `java -jar editor-workspace-smoke.jar` **26/26 PASS** (exit 0). This is **JVM-only PoC smoke**, not product Unit/Integration/KMP/Android/Windows/Ubuntu acceptance.
- GitHub PUBLIC source/test blobs match the exact locally compiled and executed source: Kotlin source `4af9c9005b6297dbc37785789922f1a0f6c1912c`, smoke test `171b5a900e0b7a299207e971802005ad5c870021`. Static platform import pattern screen: 9/9 PASS (text only).
- V1057 PUBLIC preflight tooling independently re-executed from the V1057 evidence ZIP: **14/14 PASS**, exit 0; not product Security gate.
- Trusted PUBLIC `git ls-remote` still **FAIL**, DNS `github.com` exit 128; full checkout, V477–latest regressions, source migration, authoritative starter/policy rechecks, reconstruction convergence, strict dependency verification, resolved License/SBOM/NOTICE, Gradle and platform gates remain **NOT RUN**.
- History bounded by number of snapshots, not byte memory; source IDs need verified platform bindings; no PDF byte export implemented. This prototype must not be promoted until P0 checkout/migration/license/build gates and real KMP integration tests.
- PDF Arranger clean-room boundary unchanged; desktop PDFBox structural backend and Android PdfRenderer viewer remain intended; no Poppler/pikepdf or Android structural engine choice.
- GitHub Actions not triggered; all new PUBLIC commits `[skip ci]`, no force push; **PRODUCTION NOT FINAL**.

## V1059 — 2026-10-27 19:00 TRT — export-plan source minimization (isolated PoC)

- PUBLIC `main` was `a19562e1cefa61a31a38cca7c932e155759a7a00` at start. PRIVATE remained **strictly READ-ONLY**.
- Reused V1058 evidence ZIP source/test after verifying exact Git blob identities `4af9c9005b6297dbc37785789922f1a0f6c1912c` and `171b5a900e0b7a299207e971802005ad5c870021` against PUBLIC GitHub.
- **Bug:** `EditorExportPlan.from` included source documents even after all their pages were deleted. This would force adapters to handle unreferenced inputs unnecessarily, and could increase file-access and privacy exposure if naïvely implemented.
- Added two independent regression scenarios: (1) completely deleted source is omitted, (2) each referenced source appears exactly once in original import order while export page order remains unchanged.
- Actual **RED**: Kotlin/JVM compilation exit 0; old implementation with new regression harness exited **1** on the deleted-source test (expected failure).
- Small clean-room fix: compute source IDs referenced by the current page list, filter source refs while preserving original source import order; no engine, platform adapter, or other behavior changed.
- Actual **GREEN**: `kotlinc-jvm 1.9.0` / JRE 21 compilation exit 0; `java -jar` exit 0; **28/28 isolated JVM smoke PASS**. This is not a Gradle/KMP/product Unit or Integration PASS.
- Exact updated Git blob IDs matched locally compiled/tested bytes: source `7a6c144d9e0ff479dbf29170eb7f09721ec818aa`, smoke `6d74664697b8be5a01ec46d1671b8a0ce272493b`. PUBLIC commits include `[skip ci]`; no force push or Actions trigger.
- PUBLIC `git ls-remote` in the executable container **FAIL** (DNS, exit 128); trusted complete checkout **NOT RUN**. No PRIVATE files migrated; authoritative starter/policy and recovery/reconstruction checks **NOT RUN in PUBLIC**.
- PUBLIC production gates: Build/Unit/Integration/Android/Windows/Ubuntu/Security/Dependency Verification/License-SBOM-NOTICE/Packaging/Signing-Rollback all **NOT RUN**; reconstruction **NOT RUN**. **0/11 PASS.**
- PDF Arranger GPL-3.0 code not used; ADR-005 only an isolated domain PoC, not production commonMain. Desktop Apache PDFBox / Android PdfRenderer architectural baselines retained; no Poppler/pikepdf or Android structural engine chosen.
- Next P0: trusted full PUBLIC checkout, secret/license/provenance-gated product migration, V477–latest real regressions, checksum convergence, strict resolved dependency/license/SBOM/NOTICE, and platform acceptance. **PRODUCTION NOT FINAL.**

## V1060 — 2026-10-27 19:56 TRT — clean-room multi-page reorder PoC

- Canonical PUBLIC `main` was `ceabfc20d7c262f599404796677a52b485f25579` at start. PRIVATE repository strictly READ-ONLY. Historical PRIVATE tests do not qualify PUBLIC.
- PUBLIC V1059 Kotlin source/test bytes were checked against prior evidence ZIP and GitHub blob IDs `7a6c144d9e0ff479dbf29170eb7f09721ec818aa` / `6d74664697b8be5a01ec46d1671b8a0ce272493b` before modifications.
- New independently authored `EditorAction.MovePages(pageIds, targetIndex)` moves a nonempty selected subset as a stable ordered block. `targetIndex` is measured in the **remaining** page list after removing selected pages. Invalid IDs, empty selection, and invalid insertion indexes are fail-closed. No-op reorder preserves state/history; selection, origin, undo/redo preserved.
- Actual RED: Kotlin/JVM compile exit 0; newly added scenario against stub implementation exited 1 (expected regression failure). Actual GREEN: `kotlinc-jvm 1.9.0` / JRE 21 compile exit 0; `java -jar` exit 0; **35/35 isolated Kotlin/JVM scenarios PASS**, including exhaustive five-page nonempty subsets and insertion points (**106 distinct cases**) with order and undo/redo assertions. This is **not** Gradle/KMP/product Unit or Integration PASS.
- Local compiled source/test Git blob identities: `368c635ca5c7d46f55017da394278634d8462eff` / `cfe38603978c16a61cb6d159df21a3fde6fd5d9f`; GitHub PUBLIC write responses matched both. Public source and test commits have `[skip ci]`.
- Independently re-executed unchanged PUBLIC migration-preflight evidence sources (blobs `cb30b28fa4debeeb8f21a86e0e1ba758d113c90a` / `824bff3a3e6e51c82af7b3bfc9eaf16164120c9f`): **14/14 synthetic unittest PASS**; Python py_compile exit 0. This is not product Security PASS.
- Trusted PUBLIC `git ls-remote` **FAIL** (DNS `github.com`, exit 128); full authenticated checkout **NOT RUN**. No PRIVATE source migrated. PUBLIC authoritative starter/policy rechecks and recovery/reconstruction convergence **NOT RUN**. Historical 142/142 starter and 17/17 policy values are not new PASS results.
- Build / Unit / Integration / Android / Windows / Ubuntu / Security / Dependency Verification / License-SBOM-NOTICE / Packaging / Signing-Rollback: **NOT RUN** as product gates; Reconstruction **NOT RUN**. **0/11 production gates PASS**.
- ADR-005 remains an isolated clean-room domain PoC; no real `commonMain` product adapter/Gradle integration. PDF Arranger GPL-3.0 code not copied, desktop Apache PDFBox structural and Android PdfRenderer viewer baselines unchanged, no Poppler/pikepdf or Android structural engine selection.
- GitHub Actions not triggered, no force push. Next P0 remains trusted PUBLIC checkout → safe product migration → V477–latest regression chain → reconstruction convergence → strict dependency verification/resolved license/SBOM/NOTICE → actual build/platform release gates. **PRODUCTION NOT FINAL.**
