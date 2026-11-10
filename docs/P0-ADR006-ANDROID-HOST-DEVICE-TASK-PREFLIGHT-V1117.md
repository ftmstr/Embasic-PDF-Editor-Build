# V1117 — ADR-006 Android-KMP host/device test acceptance pilot (UNAPPROVED)

**10 November 2026 ~13:4x TRT • PRODUCTION NOT FINAL**  
**Scope:** User-uploaded generic KMP starter only; no product sources, Gradle dependencies, wrapper binaries, PRIVATE assets, GitHub Actions or platform runtime changed.

## Canonical and P0 checkout truth

- Verified PUBLIC `ftmstr/Embasic-PDF-Editor-Build` main starting HEAD `9a61a71dffb120f3cf669129a5f06b933e00ce25`, STATUS V1116. Reviewed current PUBLIC tree, latest V1116 native Google Drive Rapor/Codex and PDF Arranger clean-room research. Historical PRIVATE `ftmstr/uygulama-baslangic-sablonu` strictly **READ-ONLY**, never modified.
- GitHub Actions GET `total_count=0`; current connected GitHub surface cannot create `workflow_dispatch`. No Actions were triggered. A real `git ls-remote` attempt **FAIL exit 128 DNS** and a real `git clone --no-tags --no-single-branch --branch main` attempt **FAIL exit 128 DNS** before any checkout directory existed. The fresh clone stderr SHA-256 is `df6f951a3ddffbd95d280ac60c29c1e08487d16c1484009787eac18bb7774775`.
- No trusted full non-shallow PUBLIC clone, remote/HEAD parity, object `git fsck`, clean before/after, real V477–latest PUBLIC regressions or Gradle run. The host has **no `gradle` or PowerShell executable**. None of these gates is PASS.

## Technical evidence: official Android-KMP plugin API has two documented opt-in examples

Official Android-KMP guide says its `com.android.kotlin.multiplatform.library` host and instrumentation test source sets are **disabled by default**. The apply-plugin section shows `withHostTestBuilder {}.configure {}` and `withDeviceTestBuilder { sourceSetTreeName = "test" }`. The same page's migration section shows `withHostTest { ... }` and `withDeviceTest { instrumentationRunner=... }`. The applicable public API form must be confirmed **against the exact chosen AGP version during a genuine Gradle build**, not guessed from either example alone.

Sources (official):
- https://developer.android.com/kotlin/multiplatform/plugin (apply, migration and host/device test sections)
- https://kotlinlang.org/docs/multiplatform/multiplatform-compatibility-guide.html
- https://developer.android.com/build/migrate-to-built-in-kotlin

The user-uploaded `Uygulama_Baslangic_Sablonu_v1.3.1(4).zip` (SHA-256 `ff50a26027b1d3d8e34d846d1bfcb0ffe96929875a70ce72c1eb97b1177fb4f1`) is the generic `KmpAppStarter`, **not** the historical PDF Editor product. Its `shared/build.gradle.kts` explicitly has a legacy `androidLibrary { }` block and neither of the two Android test opt-in alternatives. Its `shared/src` contains `commonTest`, but **no `androidHostTest` or `androidDeviceTest` sources**. Simply creating test tasks therefore cannot prove that Android tests have run. The two Gradle lineages and absent wrapper/strict verification/resolved NOTICE are still blockers under proposed ADR-006.

## Actually delivered this turn: minimal isolated candidate, not a migration

Prepared a **Drive-only, unapproved, reversible** candidate change from the *uploaded generic starter*:
- change only `shared/build.gradle.kts`'s `androidLibrary { }` to `android { }`;
- add a host-test builder opt-in and a device-test builder opt-in based on the official application example;
- preserve all existing versions, compiler options, dependencies, plugin aliases, namespace and platform source sets;
- leave every other file untouched; do **not** supply new runtime dependencies or fabricate an instrumentation runner/test result;
- do **not** publish any user-uploaded starter code into PUBLIC until source rights, licence, PII/security and full-trusted-checkout preconditions are independently satisfied.

The candidate is **UNAPPROVED**; it might not compile on the declared AGP version until tested against actual Gradle. Revertibility and exact source input are documented with SHA-256; proposal output is a diff and isolated copy retained in the Google Drive V1117 evidence ZIP.

Independent stdlib Python regression suite on the candidate **12/12 PASS, exit 0**, including immutable ZIP identity, exact single-context replacement, no dependency import, preservation of existing configuration, diff bound, second-application rejection, multiple-block rejection, plugin-missing rejection, conflicting-test-builder rejection and explicit non-production status. These are **source transformation tests, not Gradle Unit/Android/Dependency Verification tests.**

## Exact acceptance conditions for the authorized Codex/Gradle host

Do **NOT** apply the candidate to PUBLIC product until separate provenance/rights approval and a trusted full PUBLIC checkout.

1. Verify a single accepted ADR-006 Kotlin/AGP/Gradle/JDK/SDK matrix and its exact plugin artifacts, wrapper JAR and distribution checksums. Choose the Android-KMP test builder API matching that specific resolved plugin. This pilot is an option, not a chosen API contract.
2. In an **approved disposable source tree**, apply the bounded candidate. Run `./gradlew --version` and `./gradlew :shared:tasks --all` with strict dependency verification, save actual task names, exit codes and logs. No task name invented from documentation can be marked PASS.
3. Add separately rights-cleared **non-empty** `src/androidHostTest` and `src/androidDeviceTest` tests, with approved exact test/runner dependencies and namespace. Confirm both appeared in discovered tasks and execute host and device tasks on supported OS/emulator/real device. `NO-SOURCE`, `SKIPPED` and task existence alone are **NOT** a passing Android test.
4. Review historical product/recovered-source two-root closure and Android isolated renderer service/manifest; preserve ADR-005 commonMain separation and byte-exact/reconstructed/new provenance.
5. Run complete PUBLIC V477–latest regressions, actual strict resolved Gradle plugin/compile/runtime/test graphs and SPDX/transitives, SBOM, THIRD_PARTY_NOTICES, Android APK/AAB and Windows/Ubuntu integration, malformed/stress/security, installer/signing/rollback. Missing evidence = NOT RUN or FAIL, never PASS.

## Truthful gate and time status

Build, Unit, Integration, Android, Windows, Ubuntu, Security, Dependency Verification, License/SBOM/NOTICE, Packaging and Signing/Rollback **all NOT RUN — 0/11 production PASS**. PUBLIC reconstruction NOT RUN. Prior V1115 70 Python and 48 Kotlin PoC PASS were **not re-executed in V1117**. Historical PRIVATE 41/41 and uploaded starter 142/142/policies 17/17 are not product release evidence.

The color PowerShell snapshot continues to count **only 11 actual production gates**, i.e. **0% verified release gate coverage**, not overall completion. Conditional planning is **12–24 weeks after** real trusted full checkout, source rights clearance and cross-platform labs are ready; if *hypothetically* all were ready on **2026-11-10**, a scenario would span **2027-02-02 through 2027-04-27**; prerequisites are not met and there is **no committed FINAL date**.

ADR-006 remains **PROPOSED / NOT APPROVED**. ADR-005 remains isolated Kotlin PoC, not product commonMain. Do not copy any GPL-3.0 PDF Arranger implementation; desktop Apache PDFBox structural and Android PdfRenderer viewer baselines remain, no Poppler/pikepdf or unapproved Android structural engine. PRIVATE strictly READ-ONLY; every PUBLIC commit `[skip ci]`; no force push; no unnecessary Actions. **PRODUCTION NOT FINAL**.
