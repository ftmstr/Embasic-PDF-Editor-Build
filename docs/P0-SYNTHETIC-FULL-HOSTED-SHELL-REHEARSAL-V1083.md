# V1083 — Execute complete manual-checkout shell against a synthetic Git origin with actual PUBLIC tooling tests

Date: 2026-10-28 ~18:00 TRT. **PRODUCTION NOT FINAL.**

## Canonical authority, permissions and provenance

- Sole writable repository: `ftmstr/Embasic-PDF-Editor-Build` PUBLIC main; initial HEAD `7dd1b0b2f607992f16ab7d08049025e11b62083e`, `docs/STATUS.md` V1082. PRIVATE `ftmstr/uygulama-baslangic-sablonu` remains strictly READ-ONLY. No PRIVATE source, asset, credentials, binary or GPL implementation published; no PRIVATE write, Actions dispatch, or force push.
- Actual PUBLIC Actions GET: **0 runs**. The connected GitHub API exposes no workflow-dispatch action; container `git ls-remote` fails with `Could not resolve host: github.com`, exit **128**. Consequently actual PUBLIC hosted checkout is **NOT RUN**, not PASS.
- V1082 evidence ZIP furnished twelve PUBLIC-scoped Python/Kotlin/workflow source files. Independent local `git hash-object` for all **12/12** matches the initial PUBLIC Git tree SHA-1 entries. This verifies those specific source bytes, not a complete PUBLIC checkout. Historical starter 142/142, policy 17/17, PRIVATE 41/41 SHA and V519 tests are **not** PUBLIC PASS.

## Concrete P0 execution performed — no new verifier

Reused the *existing* `.github/workflows/p0-trusted-public-checkout.yml` shell body (unchanged in PUBLIC) in a **temporary synthetic local Git repository** populated with the exact twelve PUBLIC-scoped source/test/workflow bytes and an explicitly synthetic `docs/STATUS.md`. The only modification to the extracted **temporary shell copy** was replacing the PUBLIC Git remote URL with an absolute local `file://` synthetic bare Git origin. The PUBLIC workflow file and remote repo were not modified.

- Initialized synthetic Git `main`, committed fixture, cloned it into a local bare origin. Synthetic commit SHA: `c8fa273d8a59f514d57c96fbfef3fbb3e9bfaef0`. This SHA **is not a PUBLIC commit**.
- Executed the entire hosted shell body with `GITHUB_SHA` set to the synthetic commit and a temporary `GITHUB_STEP_SUMMARY` path: **PASS**, exit **0**. It executed clone, origin/main/remote/event-SHA equality, non-shallow/clean checkout, `git fsck --full --strict --no-reflogs`, all **59/59 actual PUBLIC-scoped Python tooling regressions**, and Python `compileall`. The 59 tests are real PUBLIC source bytes but run inside a **synthetic fixture**; they do not establish a hosted PUBLIC checkout.
- Negative event-SHA test with `GITHUB_SHA=000...000`: **expected FAIL**, exit **1**, no success summary produced. This is a correctly rejected fixture.
- Separately executed local PUBLIC-scoped Python tests: **59/59 PASS**, exit **0**; `compileall`: exit **0**. Isolated Kotlin/JVM compilation: exit **0**; smoke: **45/45 PASS**. All are tooling/PoC tests, not product Unit/Build/Integration/Security acceptance.
- No new Python verifier or production engine was added; priority remains obtaining a real trusted PUBLIC checkout.

## Evidence and limitations

Local evidence archive: `V1083_Synthetic_Hosted_Workflow_Rehearsal_Evidence.zip`, SHA-256 `82865a469909e147d1348e24d6ec6d65541c8009d3bb4d0922b8edc1e9f66bf9`, 7,071 bytes. Includes synthetic workflow logs, event-SHA negative log, actual scoped test logs, Kotlin smoke log, DNS error log, and provenance JSON. No PRIVATE source bytes. The evidence ZIP is a local conversation artifact, not a verified PUBLIC checkout or repository content.

**Interpretation:** This removes uncertainty that the V1082 workflow shell can discover all 59 current PUBLIC tooling tests in a non-shallow synthetic Git execution. It **does not** remove the primary network/dispatch blocker or certify the real hosted environment. No new product code, source migration, or production gate acceptance.

## Release gates and architecture

Build / Unit / Integration / Android / Windows / Ubuntu / Security / Dependency Verification / License-SBOM-NOTICE / Packaging / Signing-Rollback: **all NOT RUN (0/11 PASS)**. PUBLIC reconstruction checksum convergence **NOT RUN**. Historical 35 recovered Kotlin candidates remain **BLOCKED** pending rights, privacy, secret, license and provenance approvals. Strict resolved Gradle dependency graph and complete transitive license/SBOM/NOTICE **NOT RUN**.

ADR-005 immutable common editor workspace remains an isolated Kotlin PoC, not product `commonMain`. PDF Arranger GPL-3.0 source/modules/runtime dependencies excluded under clean-room policy; desktop Apache PDFBox structural and Android PdfRenderer viewer baselines preserved; no Poppler/pikepdf or preselected Android structural engine.

## Immediate P0 handoff

On an authorized GitHub Actions/Codex host, **run the existing manual-only PUBLIC workflow once**, record run/job ID, event SHA, HEAD/origin/main/remote equality, `git fsck`, complete logs, test counts and SHA-256. If unavailable, record **NOT RUN**; never substitute the synthetic fixture result. Then perform V477–latest regressions, approved source migration with byte-exact versus reconstructed provenance, PUBLIC reconstruction checksum convergence, strict resolved Gradle + License/SBOM/NOTICE, actual product build/unit/integration/platform/security/packaging/signing/rollback. All PUBLIC repo writes `[skip ci]`, no force push; no unnecessary Actions; PRIVATE READ-ONLY. **PRODUCTION NOT FINAL.**
