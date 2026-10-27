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
