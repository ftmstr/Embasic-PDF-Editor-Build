# V1082 — Manual P0 checkout now discovers the complete PUBLIC tooling test suite

Date: 2026-10-28 ~17:02 TRT. **PRODUCTION NOT FINAL.**

## Canonical scope and root cause

- PUBLIC `ftmstr/Embasic-PDF-Editor-Build` main at turn start: `40276045869146f5c8652b4ad391481ca8650695` (STATUS V1081). Sole writable repository is PUBLIC. PRIVATE `ftmstr/uygulama-baslangic-sablonu` remains strictly **READ-ONLY**.
- Read-only GitHub Actions runs GET: **0 runs**. No dispatch. Container `git ls-remote` against PUBLIC failed DNS, exit **128**; a genuine complete remote checkout, GitHub-hosted workflow run, and `git fsck` of canonical clone remain **NOT RUN**.
- Root cause in the existing manually dispatched workflow: its Python test commands explicitly enumerated only three files. Since V1076 and V1080 added `test_android_manifest_component_gate.py` and `test_public_source_set_closure.py`, the hosted workflow would silently omit those regression modules. This is a **test coverage gap**, not a product failure.
- Minimal PUBLIC-only fix: replace three file-specific `unittest discover` invocations with `python3 -m unittest discover -s tests -p 'test_*.py' -v`. Replace two-file `py_compile` with `python3 -m compileall -q tools tests`. No new GitHub Actions triggers, third-party actions, secrets, dependency or runtime engine changes. Keep manual-only, read-only token, canonical remote, dispatch SHA equality, clean/non-shallow checkout and `git fsck` conditions unchanged.
- New regression in `tests/test_p0_manual_workflow.py` ensures the full discovery command exists and the old partial enumeration is rejected.

## Executed RED → GREEN evidence

1. Local scope-limited source extraction from previous evidence ZIPs: 12 PUBLIC workflow, Python tool/test and Kotlin PoC files. All **12/12 Git blob SHA-1 values matched** the current PUBLIC main tree before patch. This is not a full checkout, nor source-rights approval.
2. Baseline PUBLIC Python tests **58/58 PASS**, exit 0, before new regression.
3. Add new regression before workflow change: workflow policy test **1 expected FAIL** (RED), 9 tests run; root cause confirmed missing all-suite discovery.
4. Patch workflow and regression: **59/59 PUBLIC Python tooling tests PASS**, exit 0; `compileall -q tools tests` exit 0. The hosted workflow itself is **NOT RUN**.
5. Independent Kotlin/JVM isolated workspace: `kotlinc` exit 0; `java -cp ... EditorWorkspaceSmokeKt` **45/45 PASS**, exit 0. This is not product KMP/Gradle Unit/Integration acceptance.
6. YAML structural parse with PyYAML **PASS**, extracted shell script `bash -n` **PASS**; not a GitHub Actions hosted execution or full workflow schema check.
7. Limited secret/PRIVATE implementation scan of the two changed files **PASS_PATTERN_ONLY**. No PRIVATE source or PDF Arranger GPL implementation copied. Exact published Git blob IDs after writes: workflow `6f14995cc4e8a08e07bf31bcec5ac5b4589e4283`; workflow policy test `78cfa97165cebc6202b5f68711835ed68f645e19`.
8. All repo commits use `[skip ci]`; no force push, no PRIVATE write, no Actions dispatch.

## Evidence package

`V1082_PUBLIC_Full_Test_Discovery_Evidence.zip` contains the PUBLIC-scoped source extraction, RED and GREEN logs, Kotlin compile/smoke logs, Git probe error, SHA-256 checksums and syntax logs. ZIP SHA-256 `66ab71fd41acc8e62e173ad159fcebf92dcc3cfb108e1a8123207aae720118a0`. The package is a **local conversation artifact**; not a PUBLIC product checkout or verified Drive repo backup.

## Production gates and next action

| Production gate | Status |
|---|---|
| Build | NOT RUN |
| Unit | NOT RUN |
| Integration | NOT RUN |
| Android | NOT RUN |
| Windows | NOT RUN |
| Ubuntu | NOT RUN |
| Security | NOT RUN |
| Dependency Verification | NOT RUN |
| License/SBOM/NOTICE | NOT RUN |
| Packaging | NOT RUN |
| Signing/Rollback | NOT RUN |
| PUBLIC reconstruction checksum convergence | NOT RUN |

**0/11 verified production release gates** (this is *not* an overall engineering completion percentage). Historical PRIVATE starter 142/142, policy 17/17, recovery 41/41, V519 tests and historical dependency metadata are **not** PUBLIC PASS. 35 recovered Kotlin migration candidates remain **BLOCKED** pending independent rights, license, privacy, secret and provenance review.

**P0 remains** authorized trusted full PUBLIC checkout/manual hosted workflow with real run ID/event SHA/HEAD/origin/main/`git fsck` logs; V477–latest regressions, controlled rights-cleared migration and separate byte-exact versus reconstructed/new provenance; PUBLIC checksum convergence; strict resolved Gradle dependency verification/transitive License/SBOM/NOTICE; actual Build/Unit/Integration/Android/Windows/Ubuntu/Security/Packaging/Signing-Rollback.

**Architecture:** ADR-005 immutable common editor workspace remains standalone Kotlin PoC, **not** product `commonMain`. PDF Arranger GPL-3.0 source/module/implementation remains excluded; desktop Apache PDFBox structural baseline and Android PdfRenderer viewer baseline unchanged. No Poppler/pikepdf or Android structural engine choice without separate PoC, license, ABI, malformed/stress and ADR.

**PRODUCTION NOT FINAL.**
