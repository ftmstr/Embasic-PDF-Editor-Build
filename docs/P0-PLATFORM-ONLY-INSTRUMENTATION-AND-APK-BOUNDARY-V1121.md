# V1121 — Android platform-only instrumentation PoC and strict transcript evidence

**2026-11-12 ~13:45 Türkiye (TRT). PRODUCTION NOT FINAL.**

## Canonical intake and first-priority network/Actions result

- PUBLIC writable repository `ftmstr/Embasic-PDF-Editor-Build`, branch `main`. Starting canonical `main` HEAD `50ee8ef234c123250e5ba151ee31bea1c9e6193a` (V1120); read `docs/STATUS.md`, tree, GitHub Actions GET **0 runs**, and V1120 native Drive Rapor and Codex docs. All historical PRIVATE access **READ-ONLY**; no PRIVATE write, PR, Actions, deletion or source migration.
- Attempted actual `git ls-remote` and a separate canonical PUBLIC `git clone --no-tags --no-single-branch --branch main` in an empty path. Both **FAIL DNS exit 128**, `github.com` name resolution unavailable. Clone log SHA-256 `f0e17bf95476e6f91e1412aac98b7601b24e4cc0425ee63da5578e521ba388f2`; no `.git` checkout directory exists. The installed GitHub connector offers workflow reads/re-runs but **no new manual `workflow_dispatch` action**; none was started.
- As a result: trusted full non-shallow PUBLIC clone, strict `git fsck`, HEAD/origin/main/remote event SHA parity and pre/post clean tree, Gradle and V477–latest complete product/source regression chain **NOT RUN**. GitHub API blob equality is not a trusted full Git checkout.

## New original PUBLIC code (prototype and tooling only)

Independent **JUnit-free / AndroidX-free platform instrumentation prototype**:
- `prototypes/android-platform-instrumentation/src/androidDeviceTest/kotlin/org/embasic/pdfeditor/platformtest/PlatformOnlyPdfInstrumentation.kt`, SHA-256 `cb0c5c4164c2fbaf3bd47365683cb997b8c7daea6a94cef1734a6bb9abb42148`, Git blob `30ed21b406369f63af7f31b31a53fdb98948d90a`: extends Android platform `Instrumentation` and attempts two explicit test cases on a platform test thread: (1) create a 96×144 **synthetic** white PDF with black interior marker, render using platform `PdfRenderer`, inspect interior and exterior pixels/contrast after starting bitmap as magenta; (2) reject malformed synthetic PDF input. Fail-closed count and result bundle, no raw user content/errors in telemetry, cache-only temporary files and page/bitmap/descriptor cleanup.
- `prototypes/android-platform-instrumentation/manifest/AndroidManifest.xml.template`, SHA-256 `1ee5e48eb96c9a3469c3440ecef9828203c565fd1df8586c6e5f8802f2094ff5`, Git blob `34ccdf603ded65a461ddfea6924c0f41a53b8696`. Unresolved `@TEST_PACKAGE@` and `@TARGET_PACKAGE@` are **deliberate**; no guessed Android application or test package, not ready to package.
- `prototypes/android-platform-instrumentation/README.md`, SHA-256 `5cc12996b578933ff2ec8515218ffc5176227f1ccbdda241f75fda22175bd1db`, Git blob `7c2512cf7a4d202b0a941fa2a36e638cc8dec6d1`: explicitly **STAGING, NOT APPROVED, NOT BUILT/EXECUTED ON ANDROID**.

Separate **new fail-closed host transcript checker**:
- `tools/v1121_instrumentation_transcript.py`, SHA-256 `e4888b02b7ed7b1d1e7d30c066a12f6cb5c2897e7eabad0ec5e65954eb144d20`, Git blob `c85e2f94fc2ae565e217bb4026c7f68e3d699877`. Accepts captured `adb shell am instrument` output and **actual adb exit code**, rejects missing/duplicate/contradictory status keys, wrong/duplicate Android instrumentation exit code, explicit failures, malformed/untrusted Unicode/control characters and oversized transcripts. Positive check emits `LOCAL_TRANSCRIPT_FORMAT_PASS_NOT_ANDROID_PROVENANCE`; `android_runtime=NOT_VERIFIED`, `production_gate=NOT_RUN`, never an Android acceptance claim. Transcript alone cannot authenticate the device, signed APK or Gradle build.
- `tests/test_v1121_instrumentation_transcript.py`, SHA-256 `d2d6c823085c920db054e6207cd06410a605e94ae46993b464587658f598e8c9`, Git blob `c23a17e632ccde250856dbdbbf314cec9ca71e28`.
- `tests/test_v1121_platform_runner_source.py`, SHA-256 `5eaa2420d81f5ded6a0173bedeb0a2adac85aa211ab875bd12b50fdfef5be303`, Git blob `c054e38ab241c705b585a7c226ab46110d5723b9`.

**6/6 exact local `git hash-object` Git blob IDs matched the canonical PUBLIC `fetch_file` read-back after creation.** These are original self-authored source files without new third-party source/dependency/artifact. No historical 51 blocked Kotlin candidates, binaries, APK, JAR/AAR or GPL-3.0 PDF Arranger code was migrated.

## Actually executed tests — scoped, NOT a product/platform release

- New `python3 -m unittest discover -s <isolated>/tests -p 'test_*.py' -v` on exact published sources: **30/30 PASS exit 0**; 20 transcript parsing positive/negative/fuzz/boundary checks + 10 platform runner source/manifest acceptance checks. Also Python source compilation PASS and XML manifest template parse PASS. The latter static checks do **not compile** or execute Android SDK APIs.
- Ran host transcript tool with **explicitly synthetic** success-formatted output: **LOCAL FORMAT PASS, Android runtime NOT VERIFIED**. With nonzero `adb` status, returned **FAIL exit 65**. Both are controlled fabricated test data, not a true device log.
- Real Android compile/Gradle/SDK/emulator/physical device/ADB/PowerShell: **NOT RUN**, not available here. The Android runner's platform API signatures and color calibration still require an actual Android SDK and device.
- V1120 prior 15/15 standalone Kotlin and 10/10 dashboard results **not re-executed or promoted**. Prior V1115 70/70 Python and 48/48 isolated Kotlin are history, not this turn's product tests.

## ADR-007 JUnit EPL-1.0 and separate production/test APK dependency closure

User policy `11-ACIK-KAYNAK-LISANS-POLITIKASI(2).md` default allowlist §2: Apache-2.0, MIT, BSD-2-Clause, BSD-3-Clause, ISC, Zlib. §7 distinguishes external build-only tooling from embedded/redistributed runtime, **not a blanket waiver for the test APK**. Official JUnit 4 `junit:junit:4.13.2` is **EPL-1.0**, separate approval required. AndroidX Test versions `runner/core:1.7.0` / `ext:junit:1.3.0` remain **candidates pending** actual resolved transitive license/hash/NOTICE evidence. None were added or approved. Sources:
- https://junit.org/junit4/license.html
- https://junit.org/junit4/dependencies.html
- https://developer.android.com/jetpack/androidx/releases/test

The original platform-only runner **avoids the direct JUnit/AndroidX test framework dependency**, but it is not yet Gradle or test APK validated. Actual product **APK** and separate **instrumentation test APK** require independent resolved dependency closure, exact AAR/JAR/component SHA-256, SPDX, test-only EPL scope decision, SBOM/THIRD_PARTY_NOTICES, proof that test dependencies are absent from shipped product, plus signed APK and runner/target identity. Neither graph, APK nor transitive artifacts are available; both release gates **NOT RUN**. No `EPL` exception granted. ADR-007 and ADR-006 remain **PROPOSED/NOT APPROVED**.

Official Android platform runner methods `Instrumentation.onCreate/onStart/finish` and PdfDocument/PdfRenderer APIs exist, but documentation does not certify that this new source compiles/works under the chosen Android-KMP toolchain:
- https://developer.android.com/reference/android/app/Instrumentation
- https://developer.android.com/reference/android/graphics/pdf/PdfDocument
- https://developer.android.com/reference/android/graphics/pdf/PdfRenderer.Page
- https://developer.android.com/kotlin/multiplatform/plugin

## Exact Codex P0 gates for the next authorized host

1. Obtain one actual non-shallow PUBLIC trusted clone or one justified manual-only GitHub-hosted run, capture real event SHA, branch/origin/main/remote parity, `git fsck --full --strict --no-reflogs`, clean pre/post, all exits and SHA256 logs; fail closed on DNS.
2. Decide ADR-006 toolchain + ADR-007 test-runner/allowlist policy **before** product migration. Use only approved verified Gradle wrapper/SDK/runtime artifacts. Inspect `:shared:tasks --all` and test APK Gradle test runner integration, since the JUnit-free prototype's manifest still contains deliberate package placeholders and Java/Kotlin Android plugin specifics may require changes.
3. Independently inspect Gradle **resolved** production APK runtime and instrumentation test APK runtime graphs and artifacts/NOTICE/SBOM; verify separate actual APK contents and signing; unknown license or JUnit EPL without explicit review remains BLOCKED.
4. Run real nonempty host/device tests against synthetic `PdfRenderer` marker/malformed cases, capture device API, pixel acceptance, runner output, actual adb exit, run count, test APK SHA. Do **not** treat transcript parser alone as proof.
5. Rights-cleared original product migration, V477–latest complete regressions, strict Gradle, Android/Windows/Ubuntu runtime/security, package/install/upgrade/uninstall/signing/rollback.
6. All 11 production Build/Unit/Integration/Android/Windows/Ubuntu/Security/Dependency Verification/License-SBOM-NOTICE/Packaging/Signing-Rollback gates **NOT RUN (0/11 PASS)**; PUBLIC reconstruction **NOT RUN**. 51 historical Kotlin files still rights/PII/secret/provenance/SPDX BLOCKED. ADR-005 isolated PoC, desktop PDFBox structural and Android PdfRenderer viewer baseline maintained, no Poppler/pikepdf.

## Dashboard and conditional ETA

Read-only PowerShell dashboard **0% verified release gate PASS coverage**, NOT overall product completion. Real Windows PowerShell 5.1/7 execution **NOT RUN**. Conditional planning **12–24 weeks AFTER** trusted PUBLIC checkout, source clearance and cross-platform labs are ready. Hypothetical prerequisite readiness on **2026-11-12** → **2027-02-04 to 2027-04-29**; prerequisites not met, **no committed FINAL date**.

All PUBLIC commits include `[skip ci]`; **no force push**, no unnecessary Actions, **PRIVATE STRICT READ-ONLY**. **PRODUCTION NOT FINAL**.
