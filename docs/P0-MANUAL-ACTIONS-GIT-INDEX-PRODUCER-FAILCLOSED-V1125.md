# V1125 — Manual PUBLIC checkout workflow: Git index producer fail-closed RED → GREEN

**18 November 2026, Europe/Istanbul · PRODUCTION NOT FINAL.**

## Canonical authority and actual first-priority result

- PUBLIC writable repository: `ftmstr/Embasic-PDF-Editor-Build` `main`, starting HEAD `98a877a29e7320e4ead611b141aad8e00191eeb7` (V1124). `docs/STATUS.md`, complete 95-entry PUBLIC Git tree, GitHub Actions GET **0 runs**, and V1124 native Drive Rapor/Codex were read. Historical PRIVATE `ftmstr/uygulama-baslangic-sablonu` remains **STRICT READ-ONLY**.
- Actually ran `git ls-remote --exit-code` against canonical PUBLIC HTTPS and a separate `git clone --no-tags --no-single-branch --branch main`. Both **FAIL, exit 128**, `github.com` DNS cannot resolve. Exact local stderr SHA-256: ls-remote `137c4578bf8e71fd67eb06ef89ac907a19bffabaf9eedd374c1b717d550f41e2`; clone `d0c78cd59e7d57f53085cc64570b78be68f1f74de91bae578c4adbae76e44dea`. No full checkout directory; no Git object `fsck`, clean before/after, origin/main/remote/event SHA equality or complete V477–latest tests.
- The connected GitHub plugin can read/write PUBLIC contents and read/rerun existing jobs but has **no `workflow_dispatch` creation action**. Actions GET **0** existing runs. No workflow was triggered. Host lacks `gradle`, `adb`, `sdkmanager`, `aapt2`, `apksigner` and `pwsh/powershell`; real Gradle task discovery, APK identity, test-APK device execution, Android/Windows/Ubuntu production runtime **NOT RUN**.

## Concrete manual-only hosted workflow defect

File `.github/workflows/p0-trusted-public-checkout.yml` originally performed:

```bash
if git ls-files --stage | awk '$1 == "160000" { found=1 } END { exit !found }'; then
  echo 'Unexpected gitlink/submodule in PUBLIC repository' >&2
  exit 1
fi
```

Under `set -Eeuo pipefail`, a failing **producer** `git ls-files --stage` causes the pipeline to return nonzero, entering the `if`'s *no-gitlink* branch even when a gitlink appears in partial output. An index I/O error can therefore be misclassified as a clean scan. This is a checkout verifier defect, **not evidence of a real GitHub Actions compromise**. The separate one-shot shell runner was already hardened at V1113; this fix applies specifically to the manual-only GitHub Actions YAML.

Test-first reproduction created **seven new independent stdlib tests** in `tests/test_v1125_manual_workflow_gitlink_failclosed.py`: manual-only/read-only workflow, healthy no-gitlink index, actual gitlink index, producer failure with gitlink, producer failure without gitlink, empty output with producer failure, and safe index-then-grep structure. Against unchanged original workflow: **4/7 FAIL, 3/7 PASS**, exit 1 (expected RED). The minimum fix captures a **complete** tracked index outside the checkout:

```bash
git ls-files --stage > "$ROOT/tracked-index.txt"
if grep '^160000 ' "$ROOT/tracked-index.txt"; then
  echo 'Unexpected gitlink/submodule in PUBLIC repository' >&2
  exit 1
else
  scan_status="$?"
  if [[ "$scan_status" -ne 1 ]]; then
    echo 'Gitlink scan error: blocked' >&2
    exit 1
  fi
fi
```

With `set -e`, any producer failure immediately aborts the workflow; grep exit 1 is the *only* accepted no-match result. After fix, **7/7 tests PASS**, exit 0, and the extracted workflow Bash script `bash -n` **PASS**. These are **local fixture tests**, not a real hosted run. No new CI trigger, write permission, third-party Action or secret was added.

Exact source artifact hashes (local `git hash-object`, GitHub tree/blob read-back):
- `.github/workflows/p0-trusted-public-checkout.yml`: SHA-256 `e1a9a6b3406190fb10d88f1a2e879ba0b7ce69994cf9a547a99857ab7e9ac201`; Git blob `e4257c3c2bedc2ac2255a3e4b4d145b1da17c23a`.
- `tests/test_v1125_manual_workflow_gitlink_failclosed.py`: SHA-256 `57cbe6d429f4bf19d818d262a350cef92eea88c91835363b6657db3b42ff6558`; Git blob `e0c0b350ef887a0b933536d1c6fe6a2874b4c3f8`.
- During the upload bridge one Unicode em dash was initially doubly UTF-8 encoded in the workflow content. The error was independently found by comparing local `git hash-object` against PUBLIC tree blob and corrected through a third `[skip ci]` PUBLIC content commit. The **final** Git blob matches original, executed source bytes exactly. This encoding repair did not change workflow behavior. Both final files have **2/2 exact verified source Git blob matches**.

## Unresolved real acceptance gates

- Only the manual checkout integrity guard was improved; **no actual workflow run**. The real full PUBLIC checkout gate is still **NOT RUN** after network FAIL, despite read-only PUBLIC REST access.
- ADR-006 Gradle/KMP/AGP toolchain and ADR-007 test-only license **PROPOSED**. `junit:junit:4.13.2` EPL-1.0 remains **BLOCKED_TEST_ONLY_EXCEPTION_REVIEW** under the user permissive license policy; no exception or resolved JUnit/AndroidX artifacts.
- No rights-cleared product migration: historical **51 Kotlin candidates** remain BLOCKED by ownership, PII/secrets, fonts/assets, SPDX/transitive licenses and provenance. ADR-005 is isolated Kotlin prototype, not product.
- No actual resolved production APK versus instrumentation APK **transitive SPDX/SBOM/THIRD_PARTY_NOTICES** or strict Gradle verification. No real signed APKs, independent pins, `aapt2`/`apksigner`, Android PdfRenderer tests on device, Windows/Ubuntu installer/upgrades/uninstall/security/runtime or V477–latest full regressions.
- PDF Arranger GPL-3.0 source/fork/module/runtime remains excluded; desktop Apache PDFBox structural / Android PdfRenderer viewer design baseline unchanged.

**All 11 production release gates** — Build, Unit, Integration, Android, Windows, Ubuntu, Security, Dependency Verification, License/SBOM/NOTICE, Packaging, Signing/Rollback — **NOT RUN (0/11 PASS)**. PUBLIC Reconstruction separately NOT RUN. 0% is **verified production-gate coverage**, not overall engineering completion. Local 7/7 workflow tests cannot be counted as release Unit/Security PASS.

## P0 follow-up and conditional scenario

On an authorized networked host: first obtain a trusted **non-shallow PUBLIC clone** or one justified manual-only hosted run. Capture run ID/event SHA, origin/main/remote HEAD parity, complete index scan, strict `git fsck`, clean pre/post, exact commands/exits/host toolchain/log SHA; hosted run must prove this patched workflow passes. Then source rights approval, exact approved Gradle/Android test task/variant discovery, separate true product/test APK dependency and license closures, real `aapt2`/`apksigner` with independently approved tool and signer pins, device pixel/malformed regression, V477–latest and cross-platform acceptance.

**Hypothetical conditional planning: 12–24 weeks AFTER** trusted checkout, rights and Android/Windows/Ubuntu test labs are all ready. If ready on 2026-11-18, that would be **2027-02-10 to 2027-05-05**. They are not ready; there is **no committed FINAL date**.

PUBLIC commits include **`[skip ci]`**, no force push or unnecessary Actions; PRIVATE **STRICT READ-ONLY**. **PRODUCTION NOT FINAL.**
