# V1126 — Dual APK physical/byte identity admission: RED to GREEN

**18 November 2026, TRT — PUBLIC ONLY, PRODUCTION NOT FINAL.**

## Baseline and top-priority real checkout

- Canonical writable repo `ftmstr/Embasic-PDF-Editor-Build`, `main`, starting HEAD `601a57426524b5243c5ed3d0d4e8405197e83b6e` (STATUS V1125). Verified full PUBLIC tree (97 entries, not truncated), `docs/STATUS.md`, GitHub Actions **0 runs**, and V1125 native Drive Rapor/Codex documents. PRIVATE `ftmstr/uygulama-baslangic-sablonu` **STRICT READ-ONLY**.
- Actual PUBLIC `git ls-remote --exit-code` and separate `git clone --no-tags --no-single-branch --branch main`: **FAIL exit 128**, github.com DNS unavailable. Actual stderr SHA-256: ls-remote `137c4578bf8e71fd67eb06ef89ac907a19bffabaf9eedd374c1b717d550f41e2`; clone `b76e47e9b8699a6739a1d46d51395ce3f8fc83fe486dd7faaccaca60a07c1255`. No `.git`; no trusted full non-shallow checkout, origin/main parity, strict fsck, clean before/after, or full V477-latest execution. Connector has no new manual `workflow_dispatch` action; zero hosted runs and **none launched**.
- No `gradle`, `./gradlew`, `adb`, `sdkmanager`, `aapt2`, `apksigner`, Windows PowerShell or `pwsh` on host. Real Gradle/AGP/KMP task discovery, Android compiled APKs, independent signing pins, device PdfRenderer, Windows/Ubuntu product runtime and true resolved dependency/SPDX/SBOM/NOTICE **NOT RUN**.

## Concrete consistency/security gap (not production exploit evidence)

The V1122 original `tools/v1122_dual_apk_preflight.py` checked product and instrumentation APKs *independently*, but did not check that these represented two **different physical files and byte contents**. A forged evidence manifest could reference the **same path**, two **hardlinks to one inode**, or distinct files with **identical bytes**, while self-declaring different package names. The validator would yield `LOCAL_FILE_GRAPH_PREFLIGHT_ONLY` for otherwise synthetic-consistent evidence. The later V1124 `tools/v1123_android_sdk_probe.py` already rejected the same alias classes, so the two gates were inconsistent.

**Actual RED** using new isolated `tests/test_v1126_dual_apk_identity.py` against untouched V1122 source: **3/8 FAIL, 5/8 PASS, exit 1**, proving exactly those three false negatives. The fixture intentionally uses fake ZIP APK structures and fake resolved Gradle evidence. This is a local proof of file/graph admission defect, **not evidence of exploitable real APKs**.

## Minimum original correction

Under `validate` in `tools/v1122_dual_apk_preflight.py`, retain each graph's already validated APK path and observed SHA-256. After independent graph checks, reject (fail-closed issues):
1. Product/test APKs with equal physical identity via `Path.samefile` (including same path and hardlink);
2. Product/test APKs with equal observed SHA-256 bytes, even if path/inode differ;
3. Failed physical file-identity check via OSError.

Sharing **one approved dependency artifact** between product and test graphs remains permitted. The tool remains a **read-only stdlib evidence preflight** and does not parse Android binary manifest packages, verify signing keys, attest Gradle resolution completeness, or run on a device.

The original V1122 `tests/test_v1122_dual_apk_preflight.py` fixture previously generated two **byte-identical fake APKs**. To keep its original 34 positive/negative checks meaningful under the strengthened invariant, only the fake test `classes.dex` byte marker was made name-specific; no acceptance logic was relaxed or fixture-specific workaround introduced.

**Actually run GREEN:** **8/8 NEW V1126 tests PASS** (exit 0) and **34/34 prior V1122 tests PASS** as regression using updated distinct fake fixtures (exit 0). Python `compileall` PASS. V1125 7/7 workflow and 12/12 dashboard suites deliberately **NOT re-executed**. These 42 scoped local Python checks are NOT product Unit/Integration/Security or Android PASS.

### Exact source bytes committed to PUBLIC

- Updated `tools/v1122_dual_apk_preflight.py`: local SHA-256 `74aaf09a95837a053530d74d79bf92d90b9b0c58e7de60049af666f45fb044d8`, PUBLIC Git blob `e266fce6069809562ef089bbfd6b8ff8f89723b9`.
- Updated V1122 synthetic regression fixture: SHA-256 `52f787c701ba5e07581e58584885ac12198a24006f6b8fd4f5482f64510e2251`, blob `f634e08324a932066dd0addbe7eb3312242eda0f`.
- New `tests/test_v1126_dual_apk_identity.py`: SHA-256 `c65554dbf7c66e642833977edcd7de681afd1de5471cceb8b1e4647c8731de50`, blob `d79e96e570409fd922499b3edc7dfe72781a84b5`.
- All three actual local `git hash-object` values match GitHub PUBLIC `fetch_file` blobs **3/3**.

## Remaining P0 release blockers and bounded claims

- Actual **two signed APKs** remain **NOT RUN**, with independently approved SDK/signing pins, full binary package/runner/target inspection and test APK vs product APK separately **resolved** JAR/AAR SHA/SPDX/THIRD_PARTY_NOTICES and SBOM not available.
- `junit:junit:4.13.2` EPL-1.0 remains **BLOCKED_TEST_ONLY_EXCEPTION_REVIEW**, ADR-007 **PROPOSED**. ADR-006 toolchain source-set migration remains **PROPOSED**. Historical **51 Kotlin source candidates** blocked pending rights/PII/secrets/asset/font/license/provenance approval; no PRIVATE code migrated.
- V1121 platform-only instrumentation remains unbuilt; real nonempty Android PdfRenderer device tests, full V477–latest eligible tests, Windows x64 / Ubuntu x64 installer/runtime, security/malformed/stress, signatures/rollback **NOT RUN**.
- Physical file identity and SHA comparisons are not atomic against an adversarial concurrent filesystem operator. A privileged actor might swap/revert files between operations; use an isolated immutable checkout/CI output workspace, independent publisher fingerprints and artifact provenance. A local preflight should never be promoted to release acceptance.
- All **11 production gates** Build, Unit, Integration, Android, Windows, Ubuntu, Security, Dependency Verification, License/SBOM/NOTICE, Packaging, Signing/Rollback: **NOT RUN — 0/11 PASS**. PUBLIC Reconstruction: **NOT RUN**. `0%` is verified release gate PASS coverage, not overall project completion. Android PDF viewer structural baseline remains PdfRenderer; desktop uses Apache PDFBox, no GPL-3.0 PDF Arranger source/runtime or Poppler/pikepdf.

## Next P0

Use a networked authorized host to obtain real non-shallow full PUBLIC checkout or one justified manual-only GitHub-hosted run, capture event SHA, exact remote HEAD/origin/main, git fsck, clean worktree and log SHA. Then rights-clear actual product, approve ADR-006/007, independently verify Gradle/AGP/Kotlin/SDK and plugin/artifact pins, discover real tasks and build signed product/test APKs. Produce separate actual APK resolved dependency closures with SPDX/SBOM/NOTICE; test `PdfRenderer` on real emulator/device, V477-latest and three-platform production acceptance.

Conditional planning **12–24 weeks only after** full trusted checkout, rights and Android/Windows/Ubuntu test labs are all ready. Hypothetical prerequisite readiness on 2026-11-18 would imply **2027-02-10 to 2027-05-05**, not a committed FINAL date.

Every PUBLIC commit includes `[skip ci]`; no force push or needless Actions; PRIVATE **STRICT READ-ONLY**. **PRODUCTION NOT FINAL**.
