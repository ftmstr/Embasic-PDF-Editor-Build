# V1129 — Trusted PUBLIC checkout: inherited Git TLS/config fail-open

Date: 2026-11-22, Europe/Istanbul. **PRODUCTION NOT FINAL.**

## Canonical authority and previous gates

PUBLIC editable repository: `ftmstr/Embasic-PDF-Editor-Build`, branch `main`. Started at V1128 `d3f53a61abcc4fcd17d80a76b44da6b471edb1df`. Previous V1126 distinct production/test APK physical/byte-identity validation and V1128 JSON/SHA evidence-writer fail-closed changes remain untouched. Historical PRIVATE template STRICT READ-ONLY.

The real `GIT_TERMINAL_PROMPT=0 git ls-remote --exit-code` failed DNS resolution, exit 128; independent `git -c protocol.file.allow=never clone --no-tags --no-single-branch --branch main` failed DNS, exit 128; no complete `.git`. A GitHub connector returned zero PR-associated runs and zero commit statuses on the starting commit, which **does not prove global Actions has no runs**. No hosted workflow dispatched, and the available connector lacks manual `workflow_dispatch` action. Trusted nonshallow checkout, remote/event/head parity, strict fsck, clean tree and V477–latest **NOT RUN**.

## P0 root cause

Official Git documentation states that **exporting `GIT_SSL_NO_VERIFY` with any value disables HTTPS certificate verification**. Existing Python `git_env()` propagated caller `GIT_SSL_NO_VERIFY`, `GIT_CONFIG_PARAMETERS` and alternate `GIT_DIR`/`GIT_WORK_TREE`; the Bash one-shot runner and manual-only hosted workflow likewise inherited these values. A caller environment could therefore suppress TLS validation or inject command configuration while the output was described as a trusted PUBLIC HTTPS checkout. This is a demonstrated **environment isolation defect** and local regression; an actual MITM or remote compromise was **not observed**.

Source: https://git-scm.com/docs/git (GIT_SSL_NO_VERIFY, GIT_CONFIG_GLOBAL, GIT_CONFIG_NOSYSTEM). Git configuration environment precedence: https://git-scm.com/docs/git-config.

## Minimum change

1. Python `tools/p0_public_checkout.py`: strip inherited `GIT_*` variables before re-introducing the explicit safe controls (GIT_CONFIG_GLOBAL=/dev/null, NOSYSTEM=1, TERMINAL_PROMPT=0, LFS_SKIP_SMUDGE=1, OPTIONAL_LOCKS=0, CONFIG_COUNT=0).
2. Bash `tools/p0_public_checkout_once.sh` and manual-only `.github/workflows/p0-trusted-public-checkout.yml`: clear inherited `GIT_*` variables **before first network Git command**, restore the same safe explicit controls. No trigger expansion, actions dispatch, new dependency, PRIVATE access, signer/secret or APK change.
3. Add source-bound `tests/test_v1129_git_environment.py` to inspect Python `git_env` via AST and exercise both Bash sanitizers with hostile environment input.

Test-first isolated reconstruction of original `git_env` and Bash environment prefix (not a complete remote checkout): **RED 4 tests, 3 failures, exit 1**. Minimum revised excerpts: **GREEN 4/4, exit 0**, Bash syntax **PASS**. These are scoped environment-isolation checks; the full canonical repository suite, actual certificate-handshake attack and Windows PowerShell 5.1/7 runtime are **NOT RUN**. The new test file was published with exact Git blob byte parity against its local source; updated Python/Bash/YAML Git blobs verified via remote content readback. Do not conflate remote Git file reads with a trusted nonshallow checkout.

## Hard release gate remains closed

No verified Gradle Wrapper / AGP/KGP task and variant discovery, production/test separate exact resolved SPDX/SBOM/NOTICE, signed distinct APK hashes, independent `aapt2`/`apksigner` tool and signer pins, actual Android `PdfRenderer` nonempty device run, V477–latest, Windows/Ubuntu packaging/runtime. ADR-006 **PROPOSED**. ADR-007 `junit:junit:4.13.2` EPL-1.0 is outside the default permissive allowlist: **BLOCKED_TEST_ONLY_EXCEPTION_REVIEW**, no waiver. Historical 51 Kotlin source candidates need ownership, PII, secret, asset/font and license provenance clearance before a PUBLIC migration; no migration attempted.

Production release gates: Build, Unit, Integration, Android, Windows, Ubuntu, Security, Dependency Verification, License/SBOM/NOTICE, Packaging and Signing/Rollback all **NOT RUN (0/11 PASS)**. Conditional 12–24-week forecast only **after** full PUBLIC trusted checkout, rights-cleared sources and functioning labs for all three platforms. No readiness date or unconditional FINAL ETA. **PRODUCTION NOT FINAL.**
