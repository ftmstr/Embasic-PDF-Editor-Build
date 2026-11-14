# V1124 — Android APK/SDK file-identity race and alias hardening (RED → GREEN)

**14 November 2026 · PUBLIC ONLY · PRODUCTION NOT FINAL**

## Canonical authority and actual first priority

- Read PUBLIC `ftmstr/Embasic-PDF-Editor-Build` `main` / `docs/STATUS.md`, complete nontruncated 93-entry Git tree, zero hosted GitHub Actions runs, and native Drive V1123 Rapor/Codex. Starting canonical HEAD `2a84936f1751862f54a289639af17131393722a5`. Historical PRIVATE repository **STRICT READ-ONLY**: no writes, PRs, Actions, deletion, force push, or source migration.
- Actually attempted both `git ls-remote --exit-code` and **separate** `git clone --no-tags --no-single-branch --branch main` using exact PUBLIC HTTPS. Both **FAIL exit 128, github.com DNS cannot resolve**; clone stderr SHA-256 `33099603509ce92606ab73961185ab4968871a691a3562b1a32e5ae2bf178678`; no `.git`. The current GitHub connector has no `workflow_dispatch` create operation; no manual hosted workflow was initiated (Actions runs still 0). **Trusted full non-shallow checkout, origin/main/remote/event SHA equality, strict `git fsck`, worktree clean pre/post, complete V477–latest source regressions NOT RUN.**
- Host's `gradle`, `adb`, `sdkmanager`, `aapt2`, `apksigner`, PowerShell 5.1/7 executables unavailable. No **real Android SDK, Gradle tasks/variants, resolved production/test APK graphs, signed packages, device testing, Windows/Ubuntu runtime, SBOM/NOTICE** exercised.

## Concrete bug class and minimal original PUBLIC change

The existing read-only `tools/v1123_android_sdk_probe.py` only rejected **leaf** symlinks for its SDK executables and APK paths. An ancestor symbolic link could therefore bypass the intended no-symlink condition. It rejected identical *pathnames* but not separate hardlink names or byte-identical products/test APKs. It SHA-256 pinned SDK executables only **before** calls and compared APK hashes only **before and after**; replacement of a tool or replacement of an APK with identical bytes/new inode could escape its original checks. These are **locally reproduced security preflight weaknesses**, not proof of real Android exploitation.

The minimal revised file (`tools/v1123_android_sdk_probe.py`) now:
1. Rejects symlinks anywhere along the absolute path to each SDK executable and APK.
2. Rejects product and instrumentation APK aliases with `os.path.samefile` and rejects identical APK bytes (a real distinct signed test package must have different package metadata).
3. Records `st_dev`, `st_ino`, size and nanosecond mtime/ctime for both APK files and both SDK tools before validation and requires their identities remain stable after validation.
4. Re-hashes both **SDK executables at the end** against independently supplied pins, in addition to existing before/after APK SHA-256. Keeps output status `LOCAL_SDK_OUTPUT_PREFLIGHT_ONLY`; there is **no** new signing action, secret, network dependency or runtime/test artifact.

**Important residual risk:** before/after identity checks and path checks are **not atomic** across adversarial concurrent filesystem mutations. A privileged attacker able to replace files between syscalls, preserve metadata or subvert the host can still evade a local preflight. Use a trusted immutable/isolated CI workspace with independently sourced SDK/package/signing pins; never claim cryptographic origin from this script. Windows/macOS path semantics and hardlinks must receive real platform validation.

## Test-first proof — scoped local tests, not Android

New original `tests/test_v1124_apk_identity_hardening.py` exercises 11 focused tests: one valid unchanged synthetic format, four ancestor-symlink attacks, same-inode hardlinks, separate files with identical bytes, SDK tool mutation after initial pin, SDK tool atomic replacement with same bytes, APK atomic replacement with identical bytes, and rejection without mutating a legitimate APK.

- **First RED:** 11 tests attempted against original exact PUBLIC V1123 source blob `54ff5be5448d9815bc0029aeff7767187eb950b4`. Results: **9 expected FAIL, 1 harness ERROR, 1 PASS**. Harness ERROR was a separate fixture issue (calculating SHA of deliberately nonexistent tool path), corrected before GREEN; **the harness error is not counted as a product bug**.
- **After scoped fix GREEN:** Python 3.13 stdlib `unittest` **11/11 PASS**, exit 0, source `compileall` PASS. New read-only PowerShell/dashboard/data contract **8/8 PASS**, exit 0. Total this turn's new local controls **19/19 PASS**, **not** product Unit, Security, Android, Windows or installer PASS.
- Revised PUBLIC source SHA-256 `92deb9bc08a51068f6fffa1c7f97e246ad0872c40d8b2d6bcb62a778a4264f22`, Git blob `998b8dc180df01bb93b60b9123a2ccfdadd98a87`. New test SHA-256 `6343ee9141c268398e1c844a7cd383e3f2ea4dc20da45ec0c9e087f0394bf3f1`, Git blob `3603d1e57ff439b658fda46e5d987b302e474597`. Both local `git hash-object` values and GitHub contents API read-back **2/2 exact MATCH**.
- Original V1123 mock-SDK **28/28** and dashboard **12/12** suites **NOT repeated**. All actual SDK outputs/test files are still **NOT RUN**; this turn's scripted SDK outputs are strictly mocked.

## Dependency/legal/source admission and release truth

- ADR-006 exact KMP/Gradle/AGP toolchain and ADR-007 test runner/license **PROPOSED**. `junit:junit:4.13.2` **EPL-1.0** is outside user's default permissive allowlist: **BLOCKED_TEST_ONLY_EXCEPTION_REVIEW**. No exception approved. The V1121 JUnit-free platform-only Instrumentation prototype is **UNBUILT**.
- Actual `--dependency-verification strict` **NOT RUN**. No known rights-cleared product Gradle project/wrapper or actual resolved **production APK versus test APK** separate dependencies, SHA-256, SPDX, SBOM, THIRD_PARTY_NOTICES or signatures.
- Historical 51 Kotlin recovered-source candidates **BLOCKED** pending ownership, secrets/PII, exact SHA, asset/font provenance and transitives. ADR-005 original Kotlin domain prototype only; PDF Arranger GPL-3.0 code/fork/runtime excluded; desktop PDFBox structural backend and Android PdfRenderer viewer baseline unchanged; no Poppler/pikepdf.
- All 11 production Build/Unit/Integration/Android/Windows/Ubuntu/Security/Dependency Verification/License-SBOM-NOTICE/Packaging/Signing-Rollback gates **NOT RUN (0/11 PASS)**. PUBLIC reconstruction separately **NOT RUN**. Dashboard percent means only verified production release gate PASS coverage, **not overall project completion**. Actual Windows PowerShell execution **NOT RUN**.

## Authorized next P0

1. Use an authorized networked host for an actual **trusted non-shallow PUBLIC clone** or one justified manual-only GitHub hosted checkout run. Save event/origin/main/remote/HEAD SHA, `git fsck --full --strict --no-reflogs`, clean before/after, exact command/exit/host versions and log SHA-256.
2. Rights-clear canonical product/recovered source; decide ADR-006/007 and independently verify wrapper/Gradle toolchain. Discover actual tasks/variants; use strict resolved dependency metadata with independent provenance. Explicitly distinguish production APK vs instrumentation APK and test-only EPL review.
3. Build signed production+test APKs, verify separate package/runner/target and independent signer/SDK pins on a trusted actual Android SDK host; execute **nonempty** synthetic PdfRenderer raster/malformed instrumentation on emulator/physical device. Confirm current probe's behavior on **real** `aapt2`/`apksigner` outputs; adjust only with evidence and regression.
4. Run V477–latest eligible PUBLIC regression chain, then actual Android, Windows, Ubuntu security/runtime/package/install/upgrade/uninstall/signing/rollback tests. Never promote local mock tests to release gates.

**Conditional ETA only:** 12–24 weeks **after** actual checkout, source-rights approval and three-platform test laboratories are all ready. Hypothetically ready 2026-11-14 -> **2027-02-06 to 2027-05-01**; prerequisites are not met and no committed FINAL date exists.

**PUBLIC commits all `[skip ci]`, no force push, no unnecessary Actions; PRIVATE STRICT READ-ONLY. PRODUCTION NOT FINAL.**
