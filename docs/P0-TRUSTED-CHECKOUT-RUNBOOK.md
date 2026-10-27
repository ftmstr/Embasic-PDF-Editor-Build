# P0 — Trusted PUBLIC checkout execution runbook

**2026-10-28 | PRODUCTION NOT FINAL**

Canonical repository: `ftmstr/Embasic-PDF-Editor-Build` (**PUBLIC**, `main`).
The former `ftmstr/uygulama-baslangic-sablonu` is **STRICTLY READ-ONLY** and must never be pushed to, deleted, or used as a replacement checkout.

## One-shot checkout on a Git-capable host

The checkout tool itself lives in the PUBLIC repository, so a fresh machine must **bootstrap it from a pinned, SHA-256-verified GitHub raw file before cloning**. Use an empty, non-existing destination directory and a working Git network connection:

```sh
curl --fail --location --silent --show-error \
  --output p0_public_checkout.py \
  https://raw.githubusercontent.com/ftmstr/Embasic-PDF-Editor-Build/2a9adfe1f1d0463d017b139104391ef06ef9e851/tools/p0_public_checkout.py
printf '%s  %s\n' \
  0d587147eb557ee2f5af3b8debf5d00d737ab6b4fba4de7007f00dad9048707d \
  p0_public_checkout.py | sha256sum --check
python3 p0_public_checkout.py --destination /absolute/path/Embasic-PDF-Editor-Build
cd /absolute/path/Embasic-PDF-Editor-Build
python3 -m unittest discover -s tests -p 'test_p0_public_checkout.py' -v
```

Alternatively, manually clone the exact PUBLIC repository on a trusted host and independently execute the integrity checks below; do not claim the one-shot tool ran unless it actually did. The pinned bootstrap source may lag a newer PUBLIC HEAD; after clone, compare against current `origin/main` and `docs/STATUS.md`.

The checkout tool is deliberately limited to the exact canonical PUBLIC HTTPS URL. It runs `git clone --no-tags --no-single-branch --branch main`, then requires the exact origin URL, non-shallow `main`, `HEAD == origin/main`, a clean worktree/index, successful `git fsck --full --strict --no-reflogs`, and no unreviewed Git submodules. It emits JSON with the checked commit and tracked-entry count. A local `file://` fixture is allowed **only** when both explicit test-only flags are passed. The tool does not execute project builds, GitHub Actions, or remote writes.

A successful fixture test **does not** establish that the real PUBLIC GitHub checkout succeeded. The real network attempt in V1064 failed because the executable environment could not resolve `github.com` (Git exit 128). Do not label the real checkout PASS until the command completes on the real PUBLIC remote with its exit code and JSON evidence.

## After successful real checkout — not before

1. Record `git rev-parse HEAD`, `git status --porcelain=v1`, `git rev-parse --is-shallow-repository`, `git fsck --full --strict`, `git ls-files -s`, and SHA-256 of the log/evidence. Re-read `docs/STATUS.md` **from that exact checkout**. Compare against the latest PUBLIC `main` immediately before any write.
2. Review historical PRIVATE product and recovered-source candidates **read-only**, with separate `byte_exact_recovery`, `reconstructed`, and `new_implementation` manifests. Historical `product/shared/build.gradle.kts` depended on `recovered-source/shared` outside `product`: never import only one subtree without resolving the source graph.
3. Exclude secrets, private documents, real case PDFs, signing material, non-cleared assets and license-unknown code. Human authorization is required before publishing; the PUBLIC preflight is a preliminary mechanical screen, not legal clearance.
4. On approved and complete PUBLIC sources only, run applicable V477–latest regressions; regenerate and verify reconstruction checksums; run `./gradlew --dependency-verification strict` with **actual existing** build/test tasks. Resolve complete dependency graph, transitive licenses, SBOM and THIRD_PARTY_NOTICES.
5. Execute and record genuine product Build, Unit, Integration, Android, Windows, Ubuntu, Security, Packaging and Signing/Rollback acceptance, including install/upgrade/uninstall and malformed/stress cases. **PASS only for commands actually executed and verified.** Everything else is FAIL or NOT RUN with evidence.

## Architecture and licensing

ADR-005 is still an isolated Kotlin workspace prototype, not a product `commonMain` integration. Keep desktop Apache PDFBox structural backend and Android PdfRenderer viewer baseline. Do not copy/fork/use GPL-3.0 PDF Arranger code, add Poppler/pikepdf to runtime, or select an Android structural engine without a separate PoC/ADR/license/ABI/performance/stress record.

Every PUBLIC GitHub commit requires `[skip ci]`, no force push. The historical Actions blackout ended 2026-10-05 00:00 TRT; do not trigger unnecessary workflows. PRIVATE is READ-ONLY. A Drive backup or API tree is **not** a trusted checkout. **PRODUCTION NOT FINAL.**
