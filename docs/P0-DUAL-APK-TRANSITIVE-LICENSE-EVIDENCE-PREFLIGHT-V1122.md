# V1122 — Separate production/test APK file-and-transitive-graph preflight

**2026-11-13 ~22:4x TRT • PRODUCTION NOT FINAL**  
**PUBLIC canonical starting HEAD:** `ebd19257e798103498e58aceb3c6ea031a3b475f`, STATUS V1121. PRIVATE historical template repository remains **STRICT READ-ONLY**.

## First-priority live Git and hosted result

Genuine canonical `GIT_TERMINAL_PROMPT=0 git ls-remote --exit-code https://github.com/ftmstr/Embasic-PDF-Editor-Build.git refs/heads/main` returned **FAIL 128**, DNS failure `Could not resolve host: github.com`. A **separate genuine** `git clone --no-tags --no-single-branch --branch main` also **FAIL 128**, `CLONE` stage; no `.git` directory. Actual clone stderr SHA-256 `b98f8fea5748b9dfcb0e79fbda28c7261c328cbbbf966052732c31a550b0b4ff`. GitHub Actions API GET: **0 runs**. Current connector exposes workflow read and rerun, but no manual `workflow_dispatch` creation action. No hosted workflow was initiated. Actual full trusted non-shallow checkout, remote HEAD parity, strict `git fsck`, clean pre/post, full V477–latest trusted source regression **NOT RUN**.

## Concrete new PUBLIC engineering work: two APK evidence preflight

Created two **original permissive/stdlib-only** PUBLIC source files:
- `tools/v1122_dual_apk_preflight.py` SHA-256 `59fbad76ec7aed9a5aaedf158f8caf1c8e5b319084a6c414435f1757865b1552`; Git blob `c199d1dd2a10662f2f8faac79f863b2df989db0d`.
- `tests/test_v1122_dual_apk_preflight.py` SHA-256 `67cfc3ffdd030cecaf68764e7a79aff660ebf0ad84bcec2b570eaadc93406688`; Git blob `830f45e72f1f52c6e39e61a6ccd3bd1a57fd56fd`.

Both Git blobs **2/2 exact match** between actually executed local bytes and canonical PUBLIC `fetch_file` read-back. No PRIVATE/proprietary/GPL source, Android JAR/AAR/SDK, PDF input, signing credential or runtime dependency was added.

Tool independently requires **production** and **instrumentation** APK evidence as two graphs and two real local files. It checks relative safe file paths and symlinks, SHA-256 of each supplied APK and resolved component artifact, bounded APK ZIP CRC/entries/manifest+DEX presence, distinct product/test package labels and target package relationship, component/root graph reachability, duplicate/orphan/unresolved transitive edges, explicit per-component SPDX allowlist and nonempty notices. It rejects JUnit `junit:junit` in **both** graphs pending separate EPL decision, and prohibits AndroidX/JUnit/Hamcrest test-library coordinates in the product graph. Strict current PUBLIC repository/HEAD and mandatory `PRODUCTION NOT FINAL` fields are checked; a Gradle resolution report path and file SHA must be provided.

**Scope limitation is deliberate:** a forged syntactically correct report, synthetic APK ZIP, manually asserted license or user-written “ACTUAL_GRADLE_RESOLUTION” label can make a *local file-format preflight* look consistent. Therefore even a positive result is **`LOCAL_FILE_GRAPH_PREFLIGHT_ONLY`, explicitly `gradle_runtime=NOT_VERIFIED`, `android_apk_identity=NOT_VERIFIED`, `signatures_and_sbom=NOT_VERIFIED`, `production_gate=NOT RUN`, `production_final=false`**. The tool does **not** claim cryptographic provenance/Gradle model completeness, binary AndroidManifest identity, signing trust, package store compliance, legal SPDX approval, actual SBOM, or license acceptance. Those require independent authorized hosted execution and manual review.

## Actually executed original tests

- `python3 -m unittest discover -s tests -p 'test_v1122_*.py' -v`: **34/34 PASS, exit 0**, with synthetic local ZIP/manifest fixtures, graph cycles and boundaries, incorrect/omitted APK/component SHA, orphan/missing transitive edges, malformed/duplicate JSON keys, path traversal/symlink, JUnit/EPL even with forged `MIT`, AndroidX leak, unknown/composite SPDX, absent NOTICE, stale HEAD/Gradle evidence and fake FINAL release.
- New dashboard JSON/PowerShell contract tests: **16/16 PASS, exit 0**, static check only, NOT actual Windows PowerShell.
- Explicit **real-evidence P0 pending manifest** supplied with missing APKs, missing graphs and missing Gradle report: validator **BLOCKED, exit 65**, with nine distinct failure reasons. Positive *synthetic* fixtures **do not count** as Android/build/license PASS. Across new local tests **50/50 PASS** scoped to file/schema/evidence controls; last V1121 30+10 tests **not rerun**.

## Gradle and Android source constraints

No `gradle`, `adb`, `sdkmanager`, `pwsh/powershell` executables or physical Android/Windows lab here. No approved product Gradle root/wrapper/sourceSets were imported. Gradle official docs confirm strict verification checks metadata against independently approved checksums/signatures; bootstrapping from untrusted repositories alone **cannot establish authenticity**. The Android Gradle `androidDependencies` report separates variant classpaths, but neither a task list nor resolved graphs were executed here:
- https://docs.gradle.org/current/userguide/dependency_verification.html
- https://developer.android.com/build/dependency-verification
- https://developer.android.com/build/dependency-resolution-errors

The user project's license policy §2 permits Apache-2.0, MIT, BSD-2-Clause/3-Clause, ISC and Zlib by default, not automatic EPL-1.0. `junit:junit:4.13.2` still needs **BLOCKED_TEST_ONLY_EXCEPTION_REVIEW** under ADR-007 **PROPOSED**; no exception or artifact downloaded. The JUnit-free platform instrumentation from V1121 remains **UNBUILT prototype**, no device result. Independent production APK and test APK resolved transitive SPDX/hash/NOTICE/SBOM graphs are **NOT RUN**. ADR-006 remains PROPOSED; historical 51 Kotlin candidates still **BLOCKED** for rights/PII/secrets/fonts/assets/transitive license and provenance.

## P0 sequence and actual production gates

First: an authorized networked **real full PUBLIC clone** (or single justified hosted manual-only run) with event/HEAD/origin/main equality, non-shallow, strict `git fsck`, clean before/after and signed logs. Then source clearance, approved exact Gradle/AGP/KGP matrix, real `:shared:tasks --all`, actual resolved production and instrumentation dependencies and artifact/NOTICE/SBOM manifests, independent real signed APK hash/package validation, and two **nonempty** platform-only Android `PdfRenderer` synthetic pixel/malformed tests on emulator/device. Complete V477–latest eligible tests and actual Android/Windows/Ubuntu runtime, security, packaging, signing and rollback acceptance.

**Build, Unit, Integration, Android, Windows, Ubuntu, Security, Dependency Verification, License/SBOM/NOTICE, Packaging, Signing/Rollback: ALL NOT RUN, 0/11 PASS.** PUBLIC reconstruction NOT RUN. This gives **0% verified release gate coverage**, NOT 0% engineering completion. Conditional only: 12–24 weeks **after** actual trusted checkout, source rights and all three platform testing labs are ready. If hypothetically all ready 2026-11-13, scenario **2027-02-05 to 2027-04-30**; prerequisites not met, not a committed FINAL date.

ADR-005 isolated immutable editor PoC, desktop Apache PDFBox structural and Android PdfRenderer viewer baseline unchanged. No GPL-3.0 PDF Arranger code/fork/module/runtime, no Poppler/pikepdf or unapproved Android structural engine. Every PUBLIC commit `[skip ci]`, no force push/unnecessary Actions; PRIVATE **STRICT READ-ONLY**. **PRODUCTION NOT FINAL**.
