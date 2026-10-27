# V1056 — PUBLIC source migration intake (mechanical preflight only)

**Date:** 2026-10-27 Europe/Istanbul. **PRODUCTION NOT FINAL.**

## Source of authority

The only writable canonical repository is `ftmstr/Embasic-PDF-Editor-Build` (PUBLIC). The former `ftmstr/uygulama-baslangic-sablonu` is **read-only historical evidence**; no writes, releases, or Actions are permitted there.

The PUBLIC repository was a documentation-only bootstrap at HEAD `b686fbea547bedf48850cebdc43dfecc6c082e1f`. The exact current PUBLIC HEAD and `docs/STATUS.md` must be checked again before every write. Historical PRIVATE V519 status and later independent regression PASS reports do not transfer to PUBLIC.

## Read-only inventory (not imported)

At the historical PRIVATE reference HEAD `e4e4b4f6ccd9d838b5ac5434b45fb8202d4ba786`, the GitHub Git-tree API returned a complete, non-truncated tree. **399 blobs** were under the reconstructed `product/` surface, and **39 blobs** under the separate `recovered-source/` surface. The reconstructed product includes Android, desktop, shared, test, tooling, Gradle, dependency metadata, and partial NOTICE materials. These counts are **not** an ownership/license clearance, checksum convergence, complete checkout, or a public-source migration.

Read-only inspection of historical ADR-001, ADR-004, ADR-005, dependency declarations, settings, `gradle.properties`, and partial third-party notices found the expected provenance split and platform constraints. No file was admitted for public transfer based on this limited inspection.

Historical starter input: SHA-256 `ff50a26027b1d3d8e34d846d1bfcb0ffe96929875a70ce72c1eb97b1177fb4f1`; historical archive verification 142/142 and policy 17/17 are **NOT RUN in PUBLIC**. Do not upload these inputs or assume public redistribution rights.

## New, independently authored PUBLIC preflight

`tools/public_migration_preflight.py` and `tests/test_public_migration_preflight.py` were authored without copying PRIVATE implementation or PDF Arranger code. They do **not** import any PRIVATE files. They are a preliminary, offline, read-only mechanical candidate-batch screen.

Example after **separate trusted checkout and human review**:

```sh
python3 -m unittest discover -s tests -p 'test_public_migration_preflight.py' -v
python3 tools/public_migration_preflight.py --root /path/to/reviewed-candidate --manifest /path/to/reviewed-manifest.json
```

Manifest schema: `{"schema_version":1,"files":[{"path":"src/Example.kt","sha256":"<64 lowercase hex>","source_kind":"new_implementation","license_spdx":"Apache-2.0","rights_reviewed":true,"privacy_reviewed":true}]}`. Use `byte_exact_recovery`, `reconstructed`, and `new_implementation` distinctly. Boolean review declarations are **not** proof of ownership or authorization; independently signed provenance and licensing evidence remains mandatory.

Mechanical checks include canonical relative paths, symlinks, UTF-8 text-only scope, file/batch limits, exact inventory and SHA-256, preliminary SPDX allowlist, and a few known secret markers. **These checks are incomplete and can miss credentials, personal data, licenses, and time-of-check/time-of-use races. A mechanical PASS is never public release approval.** Binary files, build wrappers, keystores, real PDFs, user data, and Gradle properties are excluded pending separate review.

On 2026-10-27, 13 isolated synthetic Python unit tests ran successfully (13/13 PASS) with Python 3; `py_compile` PASS. The committed files were read back from PUBLIC and their Git blob IDs matched the locally tested bytes. No PRIVATE files were included. Full PUBLIC checkout and real Gradle/Android/Windows/Ubuntu tests were **NOT RUN**.

## Blockers and next P0 steps

The execution container cannot resolve `github.com` for `git ls-remote` (exit 128), so a trusted complete PUBLIC Git checkout remains blocked in this environment. A GitHub API tree is not a trusted executable checkout. Use a suitable Codex/local runtime to obtain a full clean PUBLIC checkout, then conduct human source ownership/privacy/license review and a deterministic allowlist-based migration; do not bulk-copy the PRIVATE repository.

After migration, run V477–latest regressions on actual checked-out source, recover/reconstructed checksum convergence, strict Gradle dependency verification and resolved transitive License/SBOM/NOTICE, then Build/Unit/Integration/Android/Windows/Ubuntu/Security/Packaging/Signing/Rollback acceptance.

## Clean-room and architecture

No PDF Arranger GPL-3.0 source/module/implementation is copied or used as a runtime dependency. Apache PDFBox remains the desktop structural backend, Android PdfRenderer the Android viewer baseline. Poppler/pikepdf stay excluded. Android structural engine requires a separate PoC and ADR with licensing, transitive, ABI, malformed/stress/performance evidence.

Historical ADR-005 is an accepted *design reference* but is **not implemented or imported** in PUBLIC. Implement immutable `EditorDocumentState`, `SourceDocumentRef`, `EditorPageRef`, `SelectionState`, `EditorAction`, `EditorExportPlan`, bounded `EditorHistory` in `commonMain` only after the P0 migration/build baseline; keep Android URI/PDFBox/Swing/Compose/Path/bitmap handles out of domain.

All PUBLIC commits require `[skip ci]`; never force-push. Historical Actions blackout ended 2026-10-05 00:00 TRT; no Actions were triggered in this turn.
