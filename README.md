# Embasic PDF Editor

Cross-platform PDF viewing and page/file operations for Android, Windows and Ubuntu/Linux.

> **Status: PRE-IMPLEMENTATION / NOT FINAL.** This public repository has been selected as the canonical development destination, but the previously developed implementation has **not** yet passed a public-source migration and verification gate. Do not treat this repository as a downloadable production release.

## Intended scope

- View PDFs and navigate pages.
- Merge, split, reorder, rotate and remove pages; export results.
- Do **not** add annotations, signatures, drawing, or edits to the content of individual PDF pages. Those features belong to a separate Studio application.

## Planned architecture

Kotlin Multiplatform with shared platform-neutral domain/state, and platform-specific adapters. Desktop PDF structural operations retain Apache PDFBox; Android PDF viewing retains the Android PdfRenderer baseline. The shared editor workspace follows immutable, unidirectional state and bounded undo/redo history.

## Contribution and release gates

Prior implementation must be migrated with provenance, source/license/secret scanning, recovery checksums, and verified tests before it is accepted here. Do not copy GPL-3.0 PDF Arranger code or include Poppler/pikepdf as runtime dependencies without a separate policy decision. A completed release requires clean builds, unit/integration, real Android/Windows/Ubuntu tests, supply-chain checks, package installation, signing and rollback evidence.

Every repository commit must include `[skip ci]` until the project explicitly changes that policy. Never force-push. Only actually executed and verified tests may be marked PASS.

See [project status](docs/STATUS.md).

## License

No repository-wide license has been approved or published yet. **Do not assume permission to redistribute third-party sources, assets, or binaries**; validate their licenses before public migration.
