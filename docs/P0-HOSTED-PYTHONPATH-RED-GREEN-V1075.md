# V1075 — Fix real hosted-checkout Python import blocker (RED → GREEN)

**2026-10-28 ~10:07 TRT | PRODUCTION NOT FINAL**

## Authority, scope, and root cause

- Canonical PUBLIC repository: `ftmstr/Embasic-PDF-Editor-Build`, starting HEAD `30b4b8a19967a8dbffedb984f2c593409ed89327` (V1074). Historical PRIVATE repository is strictly READ-ONLY; no PRIVATE write or source migration occurred.
- The manual-only `.github/workflows/p0-trusted-public-checkout.yml` executes `python3 -m unittest discover -s tests -p 'test_p0_public_checkout.py' -v` from repository root. `tests/test_p0_public_checkout.py` imports `p0_public_checkout` from `tools/`, which is **not on Python's module search path by default**.
- **Actual RED reproduction on Git-blob-verified PUBLIC source:** `env -u PYTHONPATH python3 -m unittest discover -s tests -p 'test_p0_public_checkout.py' -v` -> exit **1**, `ModuleNotFoundError: No module named 'p0_public_checkout'`. This means a successfully cloned GitHub-hosted workflow would still fail during scoped tests. The prior V1074 corrected local environment but had not fixed the workflow.
- Added one line before the three test commands: `export PYTHONPATH="$PWD/tools${PYTHONPATH:+:$PYTHONPATH}"`. Added `test_checkout_tool_import_path_is_explicit` regression so this requirement is retained.
- The change is minimal and does not introduce a push, secret, third-party Action, PRIVATE reference, new dependency, or product source migration.

## Exact PUBLIC source identity and commits

| File | Prior PUBLIC Git blob | New PUBLIC Git blob |
| --- | --- | --- |
| `.github/workflows/p0-trusted-public-checkout.yml` | `d43a2aaab36a9082b090b65adfccb6997576d7b5` | `e4fab70254886505d05d84a3d91e895003ad124b` |
| `tests/test_p0_manual_workflow.py` | `7134a747f8c9b9275983408b213aa84f4c273e78` | `80bd49c9262cbe9403d76eaef83141cc67a3d660` |

PUBLIC commits: `63fd110d48f959788afb3ee2d27dba301a0b95a9`, `7f8f1a1fff9926c73d9e8ec3ff34eb18510b73a4`. Both messages include `[skip ci]`; no force push.

## Actually executed tests

| Test / target | Result |
| --- | --- |
| Original PUBLIC checkout unittest with missing PYTHONPATH | **FAIL (expected RED)**, exit 1, import error |
| New regression against original workflow | **FAIL (expected RED)**, exit 1 (7 pass / 1 fail) |
| Fixed PUBLIC checkout fixture tests | **PASS 10/10**, exit 0 |
| Fixed PUBLIC migration preflight synthetic tests | **PASS 14/14**, exit 0 |
| Fixed PUBLIC manual workflow policy tests | **PASS 8/8**, exit 0 |
| Python `py_compile` on PUBLIC tooling | **PASS**, exit 0 |
| YAML parse/manual-only/read-only token policy | **PASS**, actual parse |
| Bash `-n` extracted workflow shell | **PASS** |
| Entire patched workflow shell against a newly created local synthetic Git bare origin, matching `GITHUB_SHA` | **PASS**, exit 0, 10+14+8 tests, Git fsck, HEAD, non-shallow, clean worktree |
| Same synthetic workflow with deliberately mismatched event SHA | **Expected FAIL**, exit 1 |
| Actual PUBLIC `git ls-remote` | **FAIL**, DNS, exit 128 |
| Actual GitHub-hosted Actions workflow | **NOT RUN** (GitHub API lists zero runs; no dispatch capability in current tool surface) |
| Trusted full PUBLIC checkout | **NOT RUN** |
| Product Gradle/KMP/platform/security/license/release gates | **NOT RUN** |

This evidence proves the one-line fix for a **scoped checkout workflow failure** in local/synthetic conditions. It does **not** prove a GitHub-hosted run, production Build/Unit/Integration/Security, or source migration.

## Reproducible log checksums

- RED missing import: SHA-256 `f0876d1988cc6189e189f6908bff424859b4d34cb56e5723aa244618584f2abe`
- RED new regression: SHA-256 `462de56e014e7b81119e81aebc3ca7687939e9333ba013abad28220d26ab5335`
- GREEN 10 tests: SHA-256 `234faafb9f173e479908f8b3a0aa93a307f373326ee507c201cf152f9e358f19`
- GREEN 14 tests: SHA-256 `ee95486f415f4c8df4fcbed5eac0547f37741220daf27a45f43084bba9f5c4c4`
- GREEN 8 tests: SHA-256 `656a6bd46779840e52021d852e1a40eb07d8cf52c700bfcf6c83991c36b48154`
- Full synthetic workflow GREEN: SHA-256 `bd73a2bf992ba87d29613b0f02ffee03ac2dd2363ad923db0b5a3c0ad5c483d4`
- Deliberately mismatched SHA synthetic FAIL: SHA-256 `7eec2a85b08aebae3acae5e7f108fdafdc601cc7a183325f4053a7f01678ca81`

## P0 next and release gates

Next P0 is **one authorized real hosted manual workflow run** and run/job log read-back, not further verifier hardening. Then trusted full PUBLIC checkout, rights/privacy/license/secret-screened migration (byte-exact versus reconstructed/new separately), V477–latest regression execution, checksum convergence, strict resolved Gradle verification and License/SBOM/NOTICE, actual Android/Windows/Ubuntu release gates. Do not run unapproved Actions or write to PRIVATE.

Production Build, Unit, Integration, Android, Windows, Ubuntu, Security, Dependency Verification, License/SBOM/NOTICE, Packaging, Signing/Rollback **all NOT RUN** (**0/11 PASS**). PUBLIC reconstruction **NOT RUN**.

ADR-005 remains a standalone immutable workspace PoC, not integrated into product `commonMain`. PDF Arranger GPL-3.0 code and modules excluded. Desktop Apache PDFBox structural / Android PdfRenderer viewer baselines retained; Poppler/pikepdf not introduced; Android structural engine unselected.

**PRODUCTION NOT FINAL.**
