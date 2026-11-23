# V1130 — Trusted PUBLIC checkout live-remote-main parity, fail closed

**Date:** 2026-11-23 (Europe/Istanbul) | **PRODUCTION NOT FINAL**

## Canonical scope

- Only PUBLIC `ftmstr/Embasic-PDF-Editor-Build` main is writable. Started from `f0230f31035d32d56f85235b4980e2d184cddb89` (V1129); no later turn at entry. PRIVATE historical template STRICT READ-ONLY.
- Preserved V1126 production/test APK physical-and-byte identity, V1128 evidence JSON/SHA failure fail-closed and V1129 inherited Git TLS/config environment sanitizer without changing those implementations.
- Real `git ls-remote` and independent complete `git clone --no-tags --no-single-branch --branch main` both FAIL `exit 128`, DNS `github.com` not resolved. Clone did not create `.git`; local complete PUBLIC fsck/remote/event SHA parity and V477-latest NOT RUN.
- Only available PUBLIC `.github/workflows/p0-trusted-public-checkout.yml` is already `workflow_dispatch` manual-only, `contents: read`; connected GitHub actions do not expose manual dispatch. No new hosted workflow created, and no Actions triggered. Commit-specific PR-run and commit-status reads returned empty; a global Actions history check was not possible.

## Reproduced P0 defect

`tools/p0_public_checkout.py:verify_checkout()` checked `git rev-parse HEAD` against the **cached** `refs/remotes/origin/main`, but did not query remote main. A real bare-Git fixture was cloned; after advancing the actual origin's main independently, the previous Python implementation still returned `status: PASS`. When the origin directory was renamed and the remote became unreachable, the previous implementation again returned `PASS`. Treating a stale or unreachable origin as a trusted current checkout breaks source provenance verification.

## Minimal correction and verification

- Read the canonical Python module through the GitHub connector and reconstructed it byte-for-byte in an isolated local test directory. Pre-change Git blob `f5732b1a8ab9d6e918c5a7f4b8a345032fb9a7b8` verified against local `git hash-object`.
- RED: three new real local-bare-Git fixture tests: 2 FAIL, 1 ERROR, exit 1. The baseline falsely accepted advanced and unavailable remote; the success-path test lacked a live SHA evidence field.
- In `verify_checkout()`, after local integrity and gitlink checks, call `git ls-remote --exit-code origin refs/heads/main` through the existing sanitized, timeout-bounded `run_git()`. Require its exact single remote-ref line to equal `<local HEAD>\trefs/heads/main`. Fail closed on ref mismatch, missing remote, DNS, timeout, malformed output. Add `live_remote_main` field to scoped evidence.
- GREEN: new three tests **3/3 PASS, exit 0**; existing directly impacted `tests/test_p0_public_checkout.py` **10/10 PASS**; combined isolated source-bound tests **13/13 PASS, exit 0**. Python compile PASS. Existing test file pre-change Git blob `23d38f1e60cfee376977d9d93c0a0bbab43c6342` matched the local copy. These are real **local fixture tests**, NOT full trusted PUBLIC checkout or production Unit/Integration.
- Published Python fix Git blob `64e1171a003a171e9a2dd2f02dd646a85640d679`; new test `tests/test_v1130_remote_main.py` Git blob `a5418e49657bfacbde0e65a0a1afbe4016a66a87`; both matched local source by exact git hash-object and GitHub fetch readback. All PUBLIC commit messages `[skip ci]`; no force push, no workflow dispatch.
- A live parity check cannot prevent future remote movement after the final read (TOCTOU); the result describes a single observed remote main at verification. CI event-SHA binding and immutable commits must be separately verified in a real hosted run.

## Platform/third-party gate

- The PUBLIC checkout still cannot supply a trusted full Gradle source tree, wrapper/AGP/KGP/Compose versions, task variants, resolved graphs or strict dependency verification. Actual production APK and instrumentation APK distinct bytes/signers, independently pinned `aapt2` and `apksigner`, SPDX/SBOM/THIRD_PARTY_NOTICES, real Android PdfRenderer nonempty/pixel/negative device tests: NOT RUN.
- Official Maven Central versioned POM of `junit:junit:4.13.2` lists **Eclipse Public License 1.0**: https://central.sonatype.com/artifact/junit/junit/4.13.2 . This confirms the ADR-007 policy conflict; no exception, waiver, actual resolved test-only scope, license notice approval or replacement migration was granted. ADR-007 remains BLOCKED_TEST_ONLY_EXCEPTION_REVIEW; ADR-006 remains PROPOSED.
- Historical 51 Kotlin candidates remain rights/ownership/privacy/secrets/fonts/assets/third-party license BLOCKED. No PRIVATE-to-PUBLIC migration. V477-latest and Windows/Ubuntu install, runtime, upgrade/uninstall and signing: NOT RUN.

## Conclusion

Build, Unit, Integration, Android, Windows, Ubuntu, Security, Dependency Verification, License/SBOM/NOTICE, Packaging, Signing/Rollback all **NOT RUN: 0/11 PASS**. Security product gate NOT RUN despite scoped checkout regression passing. PowerShell dashboard is an inspectable snapshot; real Windows PowerShell 5.1/7 execution NOT RUN. Conditional 12–24-week estimate applies only after verified complete PUBLIC checkout, source rights and all Android/Windows/Ubuntu labs exist. **PRODUCTION NOT FINAL.**
