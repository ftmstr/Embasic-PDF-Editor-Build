# V1123 — Read-only Android SDK APK identity/signature preflight

**13 November 2026 · PRODUCTION NOT FINAL**

## Canonical intake and actual live attempt

- Writable authority **PUBLIC** `ftmstr/Embasic-PDF-Editor-Build` `main`. Verified start HEAD `c680130e4e65933729076067535ed32e4801c331` (V1122), `docs/STATUS.md`, PUBLIC tree, GitHub Actions GET **0 runs**, and native Google Drive V1122 Rapor/Codex content. Historical PRIVATE `ftmstr/uygulama-baslangic-sablonu` **STRICT READ-ONLY**.
- A real `git ls-remote --exit-code` and a **separate** `git clone --no-tags --no-single-branch --branch main` using exact canonical PUBLIC Git HTTPS both **FAIL exit 128** because `github.com` DNS cannot be resolved. Actual stderr for clone SHA256 `a2f75866cfa26e758c8f5b68f155c30b0de7940ac59a4eecc83272498db4bf2e`; clone yielded no `.git` checkout. Current connected GitHub actions list no `workflow_dispatch` creation operation; 0 runs, no manual hosted run initiated.
- Consequently **trusted non-shallow full checkout, remote/origin/main/event parity, strict `git fsck`, clean before/after and full V477–latest product source tests NOT RUN**. No product Gradle root/wrapper/sourceSets, Android SDK, `adb`, `sdkmanager`, `aapt2`, `apksigner`, PowerShell, physical Windows or Android test device available in this runtime.

## New original PUBLIC source (NOT product release or Android build)

Added read-only:
- `tools/v1123_android_sdk_probe.py` SHA256 `47aa9e92959ee996734ea06622b61f1dadc6b9ca6e02b150445de5b08a9edfd6`, PUBLIC Git blob `54ff5be5448d9815bc0029aeff7767187eb950b4`.
- `tests/test_v1123_android_sdk_probe.py` SHA256 `84dd447bee136e61130fac3eee6235093d8efcb2ee077a05c39278621a4536f6`, PUBLIC Git blob `2608d9cf9714603770f0b481adc152208c4ae6b9`.
- **2/2 exact Git blob equality** checked between locally executed source/test bytes and canonical PUBLIC GitHub `fetch_file` after publication. Both original stdlib-only scripts; NO APK, AAR/JAR, signing credential, PDF, external dependency, PRIVATE or GPL source copied.

The probe takes separate *production APK* and *instrumentation APK* paths with **approved expected package/test package/runner**, independently pre-pinned SHA-256 for `aapt2` and `apksigner` executables, and expected signer certificate SHA-256 pins for each package. It runs only read operations (argv list, never shell):
1. `aapt2 dump badging <apk>` for each APK; require exact single package and a **single** test instrumentation line matching runner + target package; reject instrumentation in product APK.
2. `apksigner verify -Werr --print-certs <apk>` for both, require exit 0, one signer digest and independent pinned signer SHA-256 match. This is *not* a signing operation.
3. Check APK contents' SHA256 **before and after** tool executions, reject modification, missing/symlink files, impossible package fields, forged/missing tool pin, changed outputs, unexpected signers, oversized/non-UTF8 SDK outputs and timeout. No secrets, keystore or network required.

**Strict limitation:** CLI reads tool outputs and matches caller-supplied pins. It does not independently attest SDK binary provenance, Git commit, Gradle toolchain/variant completeness, signing-key custody, Android manifest binary semantics across all SDK versions, Android device/install/runtime, licence approval, SBOM or NOTICE. With *fake* tools and *fake* APK files, local format can still pass. A positive result is only `LOCAL_SDK_OUTPUT_PREFLIGHT_ONLY`, with `production_gate=NOT RUN`, `android_test_execution=NOT RUN`, `gradle_resolved_graph=NOT_VERIFIED`, `license_sbom_notice=NOT_VERIFIED`, `production_final=false`. Real SDK output needs to be reviewed on a trusted host; format variations may require a scoped correction, not a bypass.

## Actually run V1123 tests — **28/28 PASS**, no previous suite repeated

- Four new, independent groups of seven original Python/stdlib tests were **actually run**: 7/7, 7/7, 7/7, 7/7 PASS, exit0. An initial unsliced attempt exceeded the command timeout and has **no PASS claim**; all test cases were subsequently executed in four completed slices. Total new tests **28/28 PASS**.
- Negative cases: wrong app/test package, malformed or absent instrumentation runner/target, missing/wrong signer, multi-signer, duplicate package, fake/incorrect SDK tool SHA, fake caller-supplied signer pin, nonzero SDK exit, missing/identical/symlink APK, changed APK during tool run, oversized/non-UTF8/blank outputs, timeout/invalid timeout, malformed package; no-shell/read-only source contract. Positive output uses **explicit fake SDK executables and FAKE APK bytes** and is labelled LOCAL ONLY. This is not an observed real Android success.
- A separate **real environment** invocation with absent SDK executables returned **BLOCKED exit 65**; host has no `aapt2`, `apksigner`, Gradle, ADB, physical Android device or Windows PowerShell. **Actual Android binary package identity, signature verification and device test NOT RUN**.

## Official tools and admission conditions

Google's Android Developer documentation recognizes `aapt2 dump badging` as manifest metadata inspection and `apksigner verify --print-certs` with `-Werr` as APK signature verification. These are narrow tools; a successful command does not prove supply-chain integrity or app functionality:
- https://developer.android.com/tools/aapt2
- https://developer.android.com/tools/apksigner

On an **authorized trusted full PUBLIC checkout** with a rights-cleared, approved, verified exact Android SDK/AGP/KGP/Gradle matrix:
- discover **actual** tasks via `./gradlew tasks --all`, run strict dependency verification, produce real APK/test APK and bound each to actual current Git HEAD;
- pre-approve independent SDK executable and APK signing cert pins **from a trusted approved source**, not from the same APK output. Avoid assuming product and test APK signer keys are identical;
- run the probe on physical APK files, retain commands, exit, tool/APK SHA, device/API, aapt2/apksigner raw logs and log digests, investigate tool format differences;
- separately produce full **resolved** production/test APK dependencies with exact AAR/JAR SHA, SPDX/transitives, SBOM and THIRD_PARTY_NOTICES; review `junit:junit:4.13.2` EPL-1.0 test-only exception (still **BLOCKED**, ADR-007 PROPOSED);
- run nonempty `PdfRenderer` synthetic black/white raster and malformed tests on emulator/physical device with captured runner/ADB/log/APK hashes. A transcript parser alone is not device provenance.

## Release gates and source/clean-room scope

All production **Build, Unit, Integration, Android, Windows, Ubuntu, Security, Dependency Verification, License/SBOM/NOTICE, Packaging, Signing/Rollback** gates **NOT RUN (0/11 PASS)**; PUBLIC reconstruction NOT RUN. V1122 34/34 and 16/16 scoped tests **NOT repeated** or promoted this turn. ADR-005 original Kotlin workspace and ADR-006/007 remain isolated/proposed. Historical 51 Kotlin candidates and product/recovered-source migration **BLOCKED** pending rights, PII/secrets, font/asset provenance, transitive SPDX; existing desktop Apache PDFBox structural / Android PdfRenderer viewer baseline unchanged, no GPL-3.0 PDF Arranger code or Poppler/pikepdf. No product code/dependency/wrapper changed.

PowerShell snapshot must state **0% verified production gate coverage**, not total project completion. Scenario-only timeline: **12–24 weeks after** full trusted checkout + source rights + all platform labs are ready; hypothetical readiness on 2026-11-13 gives 2027-02-05 through 2027-04-30, **not a committed delivery date**. PUBLIC commits **`[skip ci]`**, no force push/unnecessary Actions. PRIVATE **STRICT READ-ONLY**. **PRODUCTION NOT FINAL**.
