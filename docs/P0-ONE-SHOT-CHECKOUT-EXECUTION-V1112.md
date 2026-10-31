# V1112 — Canonical PUBLIC One-Shot Checkout Execution & Evidence (NOT FINAL)

**2026-10-31 10:17 TRT — PUBLIC `main`**. **PRODUCTION NOT FINAL.**

## Authority, P0 blocker, and nonclaims

- Starting canonical PUBLIC HEAD: `ef56d7a46ea32d99a6b5dd886292ae66d601dad8` (V1111). PRIVATE `ftmstr/uygulama-baslangic-sablonu` remains strictly **READ-ONLY**; no PRIVATE writes, issue, PR, Actions or deletion.
- GitHub Actions GET `total_count=0`; a manual hosted `workflow_dispatch` action is not exposed in the current GitHub integration. No Actions were dispatched.
- Real local `git ls-remote` and the new one-shot clone attempted the exact PUBLIC HTTPS URL, both **FAIL DNS** (`Could not resolve host: github.com`, exit **128**). Trusted non-shallow full PUBLIC checkout, `git fsck` of remote objects, origin/main equality and clean before/after actual tests are **NOT RUN**. The failure has `checkout-evidence.json` and log SHA-256; a failed checkout is not a passing release gate.

## Concrete new engineering delivery

Added independently authored, stdlib/Git-only files to PUBLIC:
- `tools/p0_public_checkout_once.sh` — single, read-only, Linux/Bash orchestration (PUBLIC-only clone, remote and event/expected SHA admission, non-shallow/clean index checks, strict `git fsck`, then existing PUBLIC Python tooling tests and optional standalone Kotlin PoC smoke, both **scoped only**). Keeps test artifacts and Python cache **outside** the clone; never pushes, modifies PRIVATE, dispatches workflow or runs Gradle production release.
  - Tested exact file Git blob: `f74b68f341a66ad67d6dd172b8339e55ad54cac0`.
  - SHA-256: `75a3319504b58ed76ea0bd05fc9489bfa53633e17b37e353a1163bf27fcb92ac`.
- `tests/test_p0_checkout_once.py` — 8 independent offline safety and fail-closed argument tests: **8/8 PASS** from the exact local code bytes, Git blob `481430aa5db5e648febe6358559ee9498348e799`. Not product Unit/Security.
- Separately updated **user-deliverable PowerShell release-gates dashboard** (in evidence ZIP, not GitHub source) with V1112 canonical HEAD and a distinct actual failed checkout section. Independent Python contract/evidence tests **20/20 PASS**. PowerShell 5.1/7 executable not installed: dashboard runtime **NOT RUN**.

The Python test and Bash parser were actually executed in this container; no assertions that the full PUBLIC checkout or product was built. The exact Bash source uploaded to GitHub was byte-matched using local `git hash-object` and subsequent GitHub blob read-back. One trailing whitespace discrepancy in the first locally written file was removed, then the exact hosted Git blob byte stream was re-tested, preserving source provenance.

## Actual failed checkout record

One of the repeat executions (source exactly matching the published PUBLIC blob):
- `EMBASIC_EXPECTED_PUBLIC_SHA=7240098f881d20384cadd806c0951c3221c1930a p0_public_checkout_once.sh --output /mnt/data/embasic_v1112/evidence/real_attempt_v2/20261031-public`
- `exit_code=128`; `failed_or_completed_stage=CLONE`; `head=null`; `remote_main=null`; `public_tooling_tests=NOT RUN`; `isolated_kotlin_smoke=NOT RUN`; `production_release_gates=NOT RUN`.
- Execution log SHA-256: `3980f362ef15d9d3e3035c53df571f8eb613505c02b2ce3d155957c1890c33f1`.
- A caller-specified `EMBASIC_EXPECTED_PUBLIC_SHA` is a fail-closed baseline only and must be updated to the current canonical PUBLIC HEAD when executing on an authorized host, not treated as successful local checkout.

## Exact authorized-host handoff

Using a trusted network-capable Linux/Codex environment, first compare current PUBLIC HEAD and review the runner Git blob and checksum. If the runner source is already present in a verified checkout:

```bash
chmod +x tools/p0_public_checkout_once.sh
export EMBASIC_EXPECTED_PUBLIC_SHA="$(git ls-remote --exit-code https://github.com/ftmstr/Embasic-PDF-Editor-Build.git refs/heads/main | cut -f1)"
mkdir -p "$HOME/embasic-p0"
bash tools/p0_public_checkout_once.sh --output "$HOME/embasic-p0/checkout-$(date -u +%Y%m%dT%H%M%SZ)"
```

Capture and compare the runner-produced `checkout-evidence.json`, `runner.log` and `SHA256SUMS.txt`. The runner does **not** automatically import historical product files or clear license/privacy risks. Do not mark stage `CLONE` exit 128 or synthetic fixtures as PASS. A status of `SUCCESS_SCOPED_ONLY` is only checkout/tooling proof, **not** product final.

## P0 product and supply-chain blockers still intact

PUBLIC tree lacks full rights-cleared PDF Editor product/root Gradle wrapper, Android/desktop modules and source-set integration. Historical **51 Kotlin candidates remain BLOCKED** pending rights, secrets/PII/privacy, SPDX/transitive asset/license and provenance review. Historical product/recovered-source dual-root and Android isolated-service/manifest class mismatch require deliberate reconciliation. `byte_exact_recovery`, `reconstructed`, `new_implementation` must remain separate, with later security fixes preserved.

V477–latest full verifier regressions in trusted PUBLIC checkout **NOT RUN**; PUBLIC reconstruction checksum convergence **NOT RUN**; historical uploaded starter 142/142, policy 17/17 and PRIVATE 41/41 evidence are **not** PUBLIC reconstruction acceptance. Strict resolved Gradle verification, complete License/SBOM/NOTICE, actual product Build/Unit/Integration, Android/Windows/Ubuntu, security/malformed/stress, packaging/signing/rollback **all NOT RUN**.

**0/11 production release gates PASS; 0% _verified gate coverage_, not overall engineering completion.** Conditional planning only: **12–24 weeks after** trusted full checkout + source rights clearance + platform test environments; a hypothetical 2026-10-31 start would imply 2027-01-23 through 2027-04-17, **not a delivery commitment**.

PDF Arranger GPL-3.0 implementation/modules/runtime dependency forbidden; no Poppler/pikepdf or unapproved Android structural engine. Desktop Apache PDFBox structural and Android PdfRenderer viewer baselines preserved. ADR-005 immutable workspace still standalone Kotlin PoC, **not** production `commonMain`.

All PUBLIC commits require `[skip ci]`, no force push. Actions blackout ended 2026-10-05; no gratuitous dispatch. **PRODUCTION NOT FINAL.**
