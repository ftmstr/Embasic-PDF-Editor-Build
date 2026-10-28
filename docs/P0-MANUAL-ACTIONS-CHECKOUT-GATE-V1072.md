# V1072 — Manual-only PUBLIC checkout execution gate

Date: 2026-10-28 08:04–08:xx TRT. **PRODUCTION NOT FINAL.**

## Canonical authority
- Sole writable repository: `ftmstr/Embasic-PDF-Editor-Build` (PUBLIC `main`).
- Starting PUBLIC HEAD: `1aa487f37a7aba7ee974037d9ba9cb70201c9839` (`docs/STATUS.md` V1071).
- PRIVATE `ftmstr/uygulama-baslangic-sablonu` is strictly READ-ONLY. No writes, PRs, Actions dispatch, or deletion.
- Historical V1071 PRIVATE snapshot 41/41 SHA-256 is **historical provenance**, not PUBLIC reconstruction or release certification.
- Authoritative starter input historical SHA-256 `ff50a26027b1d3d8e34d846d1bfcb0ffe96929875a70ce72c1eb97b1177fb4f1`; historical 142/142 starter and 17/17 policy results are **NOT RUN on PUBLIC**.

## New concrete P0 implementation
A narrowly scoped, **manual-only** workflow is present at `.github/workflows/p0-trusted-public-checkout.yml`. It has only `workflow_dispatch`, `permissions: contents: read`, and an `ubuntu-24.04` job restricted to `main`. It uses no third-party Actions, no secrets, no PRIVATE repository, no submodule checkout, no GitHub remote writes, and no push/PR/schedule trigger.

When explicitly dispatched, the job attempts a fresh PUBLIC `git clone --no-tags --no-single-branch --branch main`, checks canonical origin URL, branch, non-shallow status, clean index/worktree, `HEAD == origin/main == remote main`, rejects gitlinks, and executes `git fsck --full --strict --no-reflogs`. It then executes the two existing scoped Python suites, the new manual-workflow policy suite, and `py_compile`. Its GitHub job log and step summary must be retained as evidence; no automatic release gate promotion.

The workflow is **not dispatched in this turn**. A complete trusted PUBLIC GitHub checkout on a hosted runner is therefore **NOT RUN**. The executable container's real `git ls-remote` still **FAILS**, DNS for `github.com`, Git exit 128.

## Actually executed locally in V1072
- YAML parsed with PyYAML BaseLoader; verified sole manual trigger and read-only token: **PASS**.
- Extracted shell script `bash -n`: **PASS**.
- Independently authored stdlib regression `tests/test_p0_manual_workflow.py`: **6/6 PASS** on exact source bytes later committed to PUBLIC.
- Complete workflow shell executed against a **synthetic local file:// Git origin** with a non-shallow clone, `git fsck`, clean tree, remote equality, two synthetic placeholder Python tests, and the six workflow-policy tests: **PASS** (synthetic only). A first synthetic attempt without the new test file failed with exit 5; fixture corrected and successful rerun recorded.
- PUBLIC GitHub blob read-back matches local tested workflow and test file identities. These are *not* PUBLIC hosted-runner checkout results.
- Historical Kotlin 45/45, Python checkout 10/10 and preflight 14/14 were **not re-executed in this turn**. Do not promote prior scoped results to current product gates.

## P0 next action — delegated execution, not a completed run
On a trusted GitHub Actions execution surface, explicitly dispatch the `P0 Manual Trusted PUBLIC Checkout` workflow on `main` once, after checking current PUBLIC HEAD and `docs/STATUS.md`. Capture run ID, job ID, commit SHA, all step logs, stdout/stderr, exit codes, SHA-256 and actual test counts. Confirm no workflow was auto-triggered and no PRIVATE write. If runner or GitHub permission is unavailable, mark **NOT RUN** and use a trusted local/Codex host to run `python3 tools/p0_public_checkout.py --destination <new-empty-path>` after reading `--help`.

Then perform reviewed two-surface product/recovered-source migration with secret, privacy, license, rights and provenance gates; run V477–latest verifiers on a real complete checkout; reconcile PUBLIC checksums without silently rebaselining the stale manifest; resolve strict Gradle dependency verification and transitive license/SBOM/NOTICE; execute real build, unit, integration, Android, Windows, Ubuntu, security, packaging, signing and rollback gates.

## Release status
Build **NOT RUN**; Unit **NOT RUN**; Integration **NOT RUN**; Android **NOT RUN**; Windows **NOT RUN**; Ubuntu **NOT RUN**; Security **NOT RUN**; Dependency Verification **NOT RUN**; License/SBOM/NOTICE **NOT RUN**; Packaging **NOT RUN**; Signing/Rollback **NOT RUN**. PUBLIC Reconstruction **NOT RUN**. **Production 0/11 PASS.**

ADR-005 remains an isolated Kotlin PoC, not production `commonMain`. PDF Arranger GPL-3.0 source/modules/implementation are excluded; desktop Apache PDFBox structural and Android PdfRenderer viewer baselines unchanged. No Poppler/pikepdf runtime or premature Android structural engine selection.

All PUBLIC commits `[skip ci]`, no force push. Historical Actions blackout ended 2026-10-05 00:00 TRT; no workflow dispatch in this turn. **PRODUCTION NOT FINAL.**
