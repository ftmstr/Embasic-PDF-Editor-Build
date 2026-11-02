# V1113 — P0 checkout Gitlink fail-open under `pipefail`: RED → GREEN

**2 November 2026, 06:38 TRT | PRODUCTION NOT FINAL**

## Canonical boundary

- Starting canonical PUBLIC `ftmstr/Embasic-PDF-Editor-Build` main HEAD `556568157fa7a2c1b3862e520d616259beaa9774` (V1112). Only PUBLIC can be written; historical PRIVATE `ftmstr/uygulama-baslangic-sablonu` remains READ-ONLY, never deleted.
- GitHub Actions GET: **0 runs**, no manual `workflow_dispatch` action exposed in this connector, no workflows dispatched. Real `git ls-remote` or clone to PUBLIC still **FAIL DNS exit 128**. Trusted full non-shallow PUBLIC checkout, `git fsck`, product migration, Gradle and platform tests **NOT RUN**.
- Read current PUBLIC `docs/STATUS.md`, 37+ blob tree, historical reconstruction provenance and source-set blockers, last V1112 native Rapor/Codex docs. Source-checks before edits: runner blob `f74b68f341a66ad67d6dd172b8339e55ad54cac0`, test blob `481430aa5db5e648febe6358559ee9498348e799`. No PRIVATE source imported.

## Bug reproduction and root cause — verified real local Git index (not PUBLIC clone)

The published one-shot runner contained:

```bash
set -o pipefail
if git ls-files --stage | grep -q '^160000 '; then
    echo 'Unexpected gitlink: blocked' >&2
    exit 65
fi
```

`grep -q` returns immediately upon the first match. On a large Git index, this closes the pipe early, and `git ls-files` may exit **141 / SIGPIPE**; with `pipefail`, the pipeline is then nonzero, so the `if` condition becomes false and **an existing gitlink is allowed past this security admission check**.

Observed in a temporary local Git repository with one mode-160000 gitlink lexicographically before **25,000** other index entries:
- baseline Bash pipeline exit **141**, despite the gitlink being present — **FAIL / reproducible fail-open**.
- The original eight offline regression tests: **8/8 PASS**, which did not detect this class.
- Added three tests before changing source; regression run **FAIL (3 errors; 8 prior PASS)** because the safe separated-index guard did not yet exist.

## Minimal fix — no changes to product engines or user data

Changed only `tools/p0_public_checkout_once.sh` gitlink check:
1. Execute `git ls-files --stage > "$OUT/tracked-index.txt"` to completion; command failure stops under `set -e`.
2. Run `grep '^160000 ' "$OUT/tracked-index.txt" > "$OUT/gitlinks.txt"` on the complete file (no `-q`, no producer pipeline).
3. Exit **65** on a found gitlink; treat exit **1** as no gitlink; any other grep exit as **blocked**. All output files are outside checkout under the requested `umask 077` evidence directory.

Actual local regression after fix: **11/11 PASS** (eight prior + three new: huge index with gitlink rejected, huge index without gitlink accepted, `git ls-files` error rejected). `bash -n` PASS. Corrected source `git hash-object` and GitHub read-back **MATCH**, Git blob `a08e32fe899d978e8b57ee5c3804dd6d4104486c`, SHA-256 `451a323fae219f540e9930af829b20ba8a0ed4139527c5609acdcdcc3d02c128`. Test byte-exact Git blob `b3594de5901a0e80b5624eee09ba0d90f3bac62f`, SHA-256 `ee1db2349a336388158a21c9375d6269d9e2a8af369a73933ef36b12063471d1`.

PUBLIC commits, all `[skip ci]`:
- `dfbb75a70ff33f594004324ac482132cec2bb94b` — minimal source fix.
- `e2711f9743c052f57c1e5fb76bb89cf964372a7c` and `0e60beee7fa125e7586c4ff5dadcf732d691a838` — new regression plus exact alignment with tested source bytes. No force push.

Re-ran fixed exact PUBLIC source runner against PUBLIC HTTPS:
- **FAIL exit 128 at CLONE** due to `github.com` DNS; `head=null`, `remote_main=null`, no Python/Kotlin suite executed.
- New real `runner.log` SHA-256 `f41b2d50ffedf4b50eb90b984e50d0c9efb38e1c14ac6d58084c5f06b59844be`.
- No actual trusted PUBLIC checkout success is claimed. Regression is in a temporary local synthetic Git index, not a production application or platform.

## P0 remaining work and gate truth

**0/11 production PASS:** Build, Unit, Integration, Android, Windows, Ubuntu, Security, Dependency Verification, License/SBOM/NOTICE, Packaging, Signing/Rollback all **NOT RUN**. PUBLIC reconstruction **NOT RUN**. Historical PRIVATE 41/41 snapshot, uploaded starter 142/142 and policies 17/17, standalone Kotlin prototype 48/48, and prior scoped Python 59/59 are **not** V1113 production test PASS.

51 historical Kotlin candidates stay **BLOCKED** for ownership/secret/PII/license/transitive/asset/provenance. Source intake requires a reviewed dual-root Gradle migration with Android isolated-service and manifest reconciliation; preserve byte-exact versus reconstructed/new separation, including divergent historical security fixes. Do not copy PRIVATE assets or use GPL-3.0 PDF Arranger code. Desktop Apache PDFBox structural and Android PdfRenderer viewer baselines remain. No Poppler/pikepdf or approved Android structural engine. ADR-005 immutable `commonMain` remains an isolated Kotlin PoC.

Next real P0: authorized networked Codex host or one justified manual-only hosted checkout, capture event and commit SHA, branch/origin/non-shallow/fsck/clean pre/post plus exit/log checksum; then V477–latest regressions and rights-cleared product migration, strict resolved Gradle licenses/SBOM/NOTICE, actual Android/Windows/Ubuntu and installer/rollback acceptance.

Progress dashboard must show **0% verified release gate coverage (not overall project completion)**, PowerShell 5.1/7 execution **NOT RUN**. Conditional planning scenario of **12–24 weeks after** trusted checkout, source rights and testing labs are available, not a promise: if hypothetically all ready 2026-11-02, 2027-01-25 through 2027-04-19. No defensible committed FINAL date.

GitHub Actions blackout ended 2026-10-05 00:00 TRT; do not trigger unnecessarily. All PUBLIC writes `[skip ci]`, no force push. **PRODUCTION NOT FINAL.**
