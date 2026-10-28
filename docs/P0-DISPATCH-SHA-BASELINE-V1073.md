# V1073 — Manual PUBLIC checkout evidence bound to dispatch commit

Date: 2026-10-28 09:03 TRT. **PRODUCTION NOT FINAL.**

## Authority and scope
Sole writable canonical repository: `ftmstr/Embasic-PDF-Editor-Build` PUBLIC `main`. Starting HEAD `c6eff6428bb8b735904a04b9051cdd3b90d018ef` (V1072). PRIVATE `ftmstr/uygulama-baslangic-sablonu` remained READ-ONLY. Historical 41/41 SHA-256 provenance does not qualify PUBLIC reconstruction.

## Reproduced correctness gap
The V1072 manual-only workflow compared cloned `HEAD` to `origin/main` and live remote `main`, but did **not** compare it to the `workflow_dispatch` event commit. A concurrent change to `main` could therefore let the workflow certify a different tree than the dispatch event. This is a baseline attribution gap, not a proven production runtime defect.

## Minimal fix and regression
- Add fail-closed `test -n "${GITHUB_SHA:-}"` and `test "$HEAD_SHA" = "$GITHUB_SHA"` after remote equality.
- Add `test_trigger_sha_bound_to_checked_out_head` to the existing scoped policy suite.
- RED before fix: **6 pass / 1 fail**, unittest exit 1, new test fails for absent `GITHUB_SHA` binding (expected).
- GREEN after fix: **7/7 PASS**, unittest exit 0; YAML parsed and manual-only trigger checked PASS; `bash -n` PASS.
- Synthetic real local Git clone and `git fsck` with event SHA matching: **PASS**, shell exit 0. With deliberately mismatched event SHA: **expected FAIL**, shell exit 1. The two other Python suites in the synthetic fixture are **placeholder tests**; they are **not** PUBLIC product regressions.
- Exact tested PUBLIC workflow blob `d43a2aaab36a9082b090b65adfccb6997576d7b5`; policy test blob `7134a747f8c9b9275983408b213aa84f4c273e78`. GitHub read-back matched.
- Local direct `git ls-remote` remains **FAIL**: DNS `github.com`, exit 128. Actual hosted workflow **NOT RUN** (no dispatch); trusted full PUBLIC checkout **NOT RUN**.

## P0 execution gate
Dispatch `.github/workflows/p0-trusted-public-checkout.yml` on PUBLIC `main` once using an authorized GitHub Actions/Codex surface. Record workflow run ID, event SHA, actual checkout HEAD, `origin/main`, remote SHA, `git fsck`, test counts, full logs and exit codes. If `main` changes between dispatch and checkout, a FAIL is correct; re-dispatch against the new HEAD rather than removing the check.

After trusted checkout, perform reviewed migration with rights/privacy/license/secret/provenance screening. Run V477–latest verifier regressions, PUBLIC reconstruction checksum convergence, strict dependency verification and resolved transitive License/SBOM/NOTICE, followed by real Gradle/build/unit/integration/platform/security/packaging/signing-rollback gates.

## Boundaries
No PRIVATE files migrated or written. No PDF Arranger GPL-3.0 implementation copied. Desktop Apache PDFBox and Android PdfRenderer baselines unchanged; Poppler/pikepdf excluded; Android structural engine unselected. ADR-005 remains isolated Kotlin PoC, not production commonMain.

All PUBLIC writes `[skip ci]`; no force push, no Actions dispatch. Build, Unit, Integration, Android, Windows, Ubuntu, Security, Dependency Verification, License/SBOM/NOTICE, Packaging, Signing/Rollback and PUBLIC Reconstruction **NOT RUN**. **PRODUCTION NOT FINAL.**
