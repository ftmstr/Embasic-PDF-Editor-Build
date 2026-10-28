# V1079 — Seven-file Android intake risk ledger (historical READ-ONLY review)

**2026-10-28 ~14:00 TRT — PRODUCTION NOT FINAL**

## Authority and scope

- Canonical PUBLIC repo: `ftmstr/Embasic-PDF-Editor-Build`; starting `main` HEAD `d591297e36d3a22acdf4915250a7ae065357ed27`, `docs/STATUS.md` V1078. This document is new PUBLIC analysis only; no product or historical source migration.
- Historical PRIVATE `ftmstr/uygulama-baslangic-sablonu` at `e4e4b4f6ccd9d838b5ac5434b45fb8202d4ba786` was read **only** via GitHub Git tree/file APIs. **Never** write, push, PR, dispatch Actions, or delete it.
- No PRIVATE Kotlin source bytes, real PDF, asset, license-uncertain binary, credential, or user data were copied to PUBLIC. The seven historical paths, Git blob SHA-1 identifiers and sizes below are *metadata only*, not byte-exact SHA-256 recovery evidence or permission to redistribute.
- The historical starter/policy and 41-file reconstruction checks are not PUBLIC PASS. A GitHub API file read is not a trusted full Git checkout.

## Seven historical Android app Kotlin candidates — migration admission BLOCKED

| Historical recovered-source suffix | Git blob SHA-1 | Tree size (bytes) | Rights/license/privacy review | Admission |
|---|---|---:|---|---|
| `android/AndroidPdfViewerViewModel.kt` | `017cd7c6e4867a3ef32a0066f69491655ca1d1c5` | 1036 | NOT VERIFIED | BLOCKED |
| `android/isolated/AndroidIsolatedPdfPlatformServices.kt` | `589d4fb058c3a36db5c639f09b0b75b17b031006` | 19251 | NOT VERIFIED | BLOCKED |
| `android/isolated/IsolatedPdfIpcPolicy.kt` | `dc4e42e5f7d39c6643409915778f4e71d9549761` | 1131 | NOT VERIFIED | BLOCKED |
| `android/isolated/IsolatedPdfProtocol.kt` | `d2338c2694b852ac640dd633efb8a2246bbed16c` | 1315 | NOT VERIFIED | BLOCKED |
| `android/isolated/IsolatedPdfRendererClient.kt` | `66ced7eeee95defd48cc2d2d1c351d9560bff233` | 15266 | NOT VERIFIED | BLOCKED |
| `android/isolated/IsolatedPdfRendererService.kt` | `aa6299062f52742eacb96bbed0e00ed3702f29b9` | 19120 | NOT VERIFIED | BLOCKED |
| `android/isolated/IsolatedRuntimeAttestationPolicy.kt` | `3f57605a44fac06979af493136a1dd8ab7f47cd5` | 796 | NOT VERIFIED | BLOCKED |

Historical Git tree reported **57,915 bytes** across these seven candidates. All seven GitHub file responses matched the corresponding historical tree blob IDs (7/7 *metadata identity*). No candidate is promoted to `byte_exact_recovery` or `reconstructed` without authoritative source-byte SHA-256 and provenance.

## New focused read-only security/license triage

- Seven textual candidate contents were inspected through read-only GitHub connector calls. **0/7 contained a per-file SPDX/license header marker** in the inspected leading region. This does **not** establish that they are unlicensed or prohibited; ownership, repository-level licenses, third-party origin and redistribution rights remain **NOT VERIFIED**.
- A targeted credential-pattern heuristic flagged **1/7** files. Focused manual code-context classification found the string to be a **Kotlin-interpolated, runtime-generated UUID token**, not a confirmed embedded credential. **0 confirmed hard-coded credentials from this narrow check**. This is not a complete secret, PII, or security audit; no token string or private code is reproduced here.
- The seven recovered Android app paths do not collide with the historical product Android app Kotlin paths (**0/7 relative-path collisions**), but this is **not a buildable seven-file migration**: imports require historical `recovered-source/shared/src/androidMain` and `recovered-source/shared/src/commonMain` definitions (and product shared sources). The source-set dependency closure, Kotlin symbol resolution, and licensing remain **NOT RUN** on the PUBLIC product.
- The historical product and recovered `AndroidManifest.xml` files collide by path. **Do not overwrite** product manifest. After rights clearance, merge only reviewed service declarations with fully qualified service class and preserve existing activity/security attributes; V1078 additive manifest PoC is synthetic only.

## Actually executed tests in this turn

- Extracted previously PUBLIC-Git-blob-matched source/test snapshot from V1078 evidence ZIP. `PYTHONPATH=<evidence>/public_scoped/tools python3 -m unittest discover -s <evidence>/public_scoped/tests -p 'test_*.py' -v` -> **42/42 PASS**, exit 0. Source snapshot is not a full checkout.
- Standalone Kotlin/JVM prototype `kotlinc EditorWorkspace.kt EditorWorkspaceSmoke.kt -include-runtime -d ...` -> **PASS**, exit 0; `java -jar ...` -> **45/45 PASS**, exit 0. Not product Gradle/KMP acceptance.
- New metadata-only migration ledger tests `python3 -m unittest -v test_ledger`: initial test fixture's **wrong total-byte expectation** yielded RED (1 FAIL); corrected expectation to historical Git tree sum **57,915**; rerun **8/8 PASS**, exit 0. This tests the **blocked** decision and rejects unsupported byte-exact/FINAL/approval promotion; not migration or security PASS.
- PowerShell dashboard static contracts: **12/12 PASS**; actual PowerShell runtime **NOT RUN**.
- Executable PUBLIC `git ls-remote`: **FAIL** DNS, exit 128; trusted complete PUBLIC Git checkout and manual GitHub-hosted workflow **NOT RUN**. GitHub Actions GET showed **0 runs** at turn start. No dispatch.
- Source rights/legal review, resolved Gradle dependencies, source-byte SHA-256 for seven candidates, Android device/emulator runtime, Windows and Ubuntu product tests **NOT RUN**.

## Production gates — no false promotion

**Build / Unit / Integration / Android / Windows / Ubuntu / Security / Dependency Verification / License-SBOM-NOTICE / Packaging / Signing-Rollback: all NOT RUN (0/11 PASS).** PUBLIC Reconstruction **NOT RUN**. Historical PRIVATE tests and independent synthetic tooling tests are not product gate PASS.

## P0 next actions

1. **Trusted full PUBLIC checkout**, preferably authorized manual-only GitHub-hosted workflow, with run ID, event SHA, HEAD, origin/main, non-shallow clone, `git fsck`, clean tree, exact logs and exit codes; no verifier hardening detour.
2. **Per-file source rights/privacy/license/provenance approval** before any PRIVATE byte migration. Resolve historical source graph including `shared/commonMain` and `shared/androidMain`, independently revalidate SHA-256, and record `byte_exact_recovery` versus `reconstructed/new` without conflation.
3. Reviewed additive Android manifest integration and actual Gradle/KMP build, V477–latest regressions, PUBLIC reconstruction checksum convergence, strict resolved dependency verification and complete License/SBOM/NOTICE, Android/Windows/Ubuntu/security/package/sign/rollback gates.
4. ADR-005 immutable common editor domain remains isolated PoC, not product `commonMain` implementation. Do not copy PDF Arranger GPL-3.0 code; retain desktop PDFBox structural and Android PdfRenderer viewer baselines; no Poppler/pikepdf or unapproved Android structural engine.

All PUBLIC writes must include `[skip ci]`; no force push. Actions blackout ended 2026-10-05 00:00 TRT but no unnecessary dispatch. **PRODUCTION NOT FINAL.**
