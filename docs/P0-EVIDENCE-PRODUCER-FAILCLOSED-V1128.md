# V1128 — Checkout evidence writers must fail closed

Date: 2026-11-22 (Europe/Istanbul). Scope: **PUBLIC** `main` only. PRIVATE history STRICT READ-ONLY.

## Source of truth
Starting checkpoint: V1127 `6611d35ec5f1ed9a8b734410fd8c4daa95541e9c`; `docs/STATUS.md` V1127. The V1127 `git status` producer fail-closed fix and V1126 distinct dual APK physical/byte identity hardening are retained unchanged.

## Verified checkout outcome
Real local `GIT_TERMINAL_PROMPT=0 git ls-remote --exit-code` and independent `git clone --no-tags --no-single-branch --branch main` fail with DNS resolution for github.com, each exit 128. No `.git` checkout. No hosted workflow dispatched. The connector does not expose workflow_dispatch. Thus trusted nonshallow clone, `origin/main`/remote/event parity, `git fsck --full --strict`, V477–latest full regressions: **NOT RUN**.

## Root cause and scope
In `tools/p0_public_checkout_once.sh`, EXIT-trap `complete()` previously used `set +e` to preserve the original command status, but did not check failure of either evidence writer. If `python3` failed to write `checkout-evidence.json`, or `sha256sum` failed to produce `SHA256SUMS.txt`, an otherwise successful run still printed `Exit: 0` and exited 0, leaving an absent or misleading evidence record. This is a **local synthetic evidence-producer issue**, not proof of a real hosted runner compromise.

Test-first reproduction: 4 source-bound `unittest` methods, **RED 2/4 failures** (Python writer failure, checksum writer failure), exit 1. Baseline normal success and original runner exit-17 handling already pass. Minimum patch tracks `evidence_failed` in EXIT trap; failed JSON or digest producer removes invalid/partial evidence and forces exit **70**. **GREEN 4/4**, exit 0; `bash -n` PASS. These are **scoped LOCAL** tests, not a product Unit/Android/security or hosted checkout PASS.

PUBLIC files:
- `tools/p0_public_checkout_once.sh`: exact revised Git blob `0266f09a0168c1100d8473f8689c7750b3313541` (remote readback).
- `tests/test_v1128_trap_evidence.py`: exact Git blob `11a8e3e3a106ede88eee69a33a4d659325e37f4b`, matching local source-bound test Git blob.
No dependency, signing key, user PDF, PRIVATE code or APK included. All PUBLIC commits include `[skip ci]`; no force-push and no Actions run triggered.

## Remaining release blockers
Trusted nonshallow PUBLIC checkout absent; no real Gradle/AGP/KMP tasks or strict resolved graph. Separate signed production/test APKs, exact SHA/SPDX/SBOM/NOTICE, independent `aapt2`/`apksigner` tool and signer pins, Android PdfRenderer nonempty actual device run, Windows/Ubuntu install/runtime tests **NOT RUN**. ADR-006 toolchain **PROPOSED**; ADR-007 `junit:junit:4.13.2` test-only EPL-1.0 review **BLOCKED**, not waived. 51 historical Kotlin candidate ownership/rights/PII/secret/asset provenance **BLOCKED**, no migration. Official source confirms JUnit 4.13.2 EPL 1.0: https://central.sonatype.com/artifact/junit/junit/4.13.2/1000 ; Gradle dependency checks: https://docs.gradle.org/current/userguide/dependency_verification.html .

All **11** production Build, Unit, Integration, Android, Windows, Ubuntu, Security, Dependency Verification, License/SBOM/NOTICE, Packaging, Signing/Rollback gates **NOT RUN**, **0/11 PASS**. Reconstruction NOT RUN. No product completion percentage claimed. Conditional ETA 12–24 weeks applies ONLY after verified complete PUBLIC checkout, rights-cleared source and all three target labs are ready; those conditions are not met, no unconditional ETA.

**PRODUCTION NOT FINAL.**
