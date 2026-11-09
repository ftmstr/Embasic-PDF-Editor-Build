# ADR-006 (PROPOSED) — PDF Editor product Gradle lineage & Android-KMP source-set admission

**Decision status: PROPOSED / NOT APPROVED / NO RUNTIME MIGRATION.**  
**Evidence date:** 2026-11-09 ~13:05 TRT. **PRODUCTION NOT FINAL.**  
**Canonical repository:** PUBLIC `ftmstr/Embasic-PDF-Editor-Build` main, starting HEAD `5c94ccaa91ab7797c17bc5163ed2564f59d1e865` (V1115). PRIVATE historical repository strictly READ-ONLY.

## Context: two different sources, neither a ready product build

The **user-uploaded** `Uygulama_Baslangic_Sablonu_v1.3.1(4).zip` (SHA-256 `ff50a26027b1d3d8e34d846d1bfcb0ffe96929875a70ce72c1eb97b1177fb4f1`) is a *generic KmpAppStarter*, NOT a recovered/rebuilt Embasic PDF Editor, and its source, assets and dependency manifest are **not authorized for automatic PUBLIC import**. Its exact byte-level `gradle/libs.versions.toml` declares:

| Coordinate | Uploaded starter declaration | Historical PDF Editor declaration from existing PUBLIC migration record |
|---|---|---|
| Gradle | `9.3.1` | `8.13` |
| Android Gradle Plugin | `9.1.0` | `8.13.2` |
| Kotlin/KGP | `2.4.10` | `2.3.20` |
| Android compile/target SDK | `36/36` | `36/36` |
| JDK target | `17` | `17` |
| Compose Multiplatform | `1.11.1` | not an approved exact product coordinate |

The historic versions are *read-only Git-tree/report declarations*, not resolved dependency graphs or a tested PUBLIC product. Source: `docs/P0-PUBLIC-MIGRATION-BLOCKER-MAP.md`. There are 51 historical Kotlin source candidates **BLOCKED** by rights, privacy/PII, secret, asset, SPDX/transitive license and provenance questions, plus dual product/recovered-source roots and Android manifest/isolated-service conflicts.

## Up-to-date official compatibility research (DOES NOT CERTIFY RESOLVED ARTIFACTS)

Official Kotlin KMP compatibility guide:
- Kotlin KGP `2.4.0–2.4.10` fully supported with Gradle `7.6.3–9.5.0` and AGP `8.5.2–9.1.0`. The uploaded starter's triple (`2.4.10, 9.3.1, 9.1.0`) lies **inside** this published range.
- Kotlin `2.3.20–2.3.21` fully supported with Gradle `7.6.3–9.3.0` and AGP `8.2.2–9.0.0`; the historical triple is **also within** its respective documented range. **Compatibility ranges are not a successful build of either codebase**.
  https://kotlinlang.org/docs/multiplatform/multiplatform-compatibility-guide.html

Official Android Gradle Plugin matrix:
- AGP `9.1` requires at least Gradle `9.3.1`. AGP `8.13` requires at least Gradle `8.13`. Thus no simple version-table incompatibility is proven in either declared lineage.
  https://developer.android.com/build/releases/about-agp
- AGP 9.1 published release notes list JDK `17` and Gradle `9.3.1` baseline, but that does **not** prove an installed SDK or product build.
  https://developer.android.com/build/releases/agp-9-1-0-release-notes

**Substantive source-set and test trap:** The uploaded `shared/build.gradle.kts` uses `com.android.kotlin.multiplatform.library` and `kotlin { androidLibrary { ... } }`. Google's official migration guide states `androidLibrary { }` is deprecated starting AGP `9.1.0-alpha09` and `android { }` is the replacement for AGP >= `8.12.0`; the current `androidLibrary { }` declaration is a **migration/deprecation risk**, NOT a demonstrated Gradle compile failure. The new KMP Android library plugin disables host and instrumentation tests by default; the starter does not explicitly configure `withHostTestBuilder` or `withDeviceTestBuilder`. Before claiming Android test-task coverage, explicitly enable suitable test builders in the reviewed project and verify tasks actually exist and execute. Its new plugin uses a single variant (not app-level flavors/build types). 
  https://developer.android.com/kotlin/multiplatform/plugin

Google's official AGP 9 migration guide says AGP 9 enables built-in Kotlin and forbids combining its application/library Android plugin with `org.jetbrains.kotlin.multiplatform` on the **same module**, although a separate KMP library using `com.android.kotlin.multiplatform.library` is supported. Preserve distinct `:androidApp` and `:shared` modules; do not accidentally merge Android app into KMP library.
  https://developer.android.com/build/migrate-to-built-in-kotlin

JetBrains Compose compatibility guide lists `1.11.1` and explains that Compose Compiler plugin should be matched to Kotlin version. This does **not** certify every transitive, native, binary or license obligation.
  https://kotlinlang.org/docs/multiplatform/compose-compatibility-and-versioning.html

Official Gradle `9.3.1` release published 2026-01-29. Official distribution and separate SHA-256/PGP signature files exist; **the user's wrapper ZIP SHA-256 value was only internally consistent between the uploaded `build.gradle.kts` and `gradle-wrapper.properties`, NOT independently fetched, signed or verified here**. No distribution JAR/ZIP downloaded or packaged.
  https://docs.gradle.org/9.3.1/release-notes.html
  https://services.gradle.org/distributions/

## Actually executed static intake on uploaded local bytes (not product Gradle)

An independent Python `zipfile`/`tomllib` test script ran **14/14 PASS**, checking exact uploaded archive identity, five declared version fields, wrapper checksum *consistency only*, absence of the wrapper executable scripts/JAR, absence of strict `gradle/verification-metadata.xml`, missing resolved runtime graph and header-only transitive license CSV, explicit `THIRD_PARTY_NOTICES.md` `NOT_FINAL`, generic project identity, legacy `androidLibrary { }`, and missing explicit Android host/device test opt-in. These are static **observations and expected blockers**, not release acceptance. Source and test logs retained in V1116 Drive evidence pack; no uploaded template code was published in PUBLIC.

The starter cannot pass production:
- no `gradlew`, `gradlew.bat` or `gradle/wrapper/gradle-wrapper.jar`;
- no `gradle/verification-metadata.xml` and no actual resolved runtime dependency graph;
- incomplete `THIRD_PARTY_NOTICES.md` marked `NOT_FINAL`;
- no verified source rights/closure for historical PDF Editor product;
- no Android/Windows/Ubuntu real product build, test, runtime or packaging.

## Proposed decision (NOT APPROVED; NO CODE/APK/GRADLE EDIT PERFORMED)

**Defer the irreversible build-lineage choice until a trusted, full PUBLIC checkout and rights-cleared product source-set graph are available.** Maintain both historical and starter triples as separate **non-authoritative candidates**. Do NOT blindly merge starter Kotlin 2.4.10/AGP 9.1.0/Gradle 9.3.1 into the historical Kotlin 2.3.20/AGP 8.13.2/Gradle 8.13 product. The project must choose **one** officially reviewed matrix and record it in a follow-up **ACCEPTED** ADR (not by changing this proposal's status without evidence).

If the new Android-KMP library plugin is selected, explicitly design:
1. `:androidApp` application module separate from `:shared` KMP library; `commonMain` domain not dependent on platform renderer classes;
2. a deliberate switch from deprecated `androidLibrary { }` DSL to current `android { }` DSL only as part of a Gradle-verified migration; actual Android host/device test builders and task discovery, with no claim that tests run merely because source files exist;
3. reconciliation of historical product and recovered-source source-set roots and isolated renderer service class/manifest, with byte-exact vs reconstructed vs new provenance recorded per file;
4. independent pinned wrapper JAR/distribution verification, strict resolved dependency metadata, full transitive SPDX/NOTICE/SBOM, all required security and OS runtime/installer/signing/rollback gates.

**Stop conditions:** no real trusted PUBLIC checkout; unknown source owner/PII/secrets/assets/license; unexpected dependency license; wrapper digest or Gradle metadata mismatch; missing Android host/device test coverage; missing platform runtime evidence. Do not bypass one gate by replacing it with static inspection. If source or test environments are unavailable mark NOT RUN.

## Decision impact and controlled sequence

- Current product Gradle Build, Unit, Integration, Android/Windows/Ubuntu, Security, Dependency Verification, License/SBOM/NOTICE, Packaging, Signing/Rollback: **all NOT RUN (0/11 PASS)**. PUBLIC reconstruction and V477–latest full trusted regressions: **NOT RUN**.
- ADR-005 existing independently authored Kotlin workspace remains **isolated PoC**; no production `commonMain` integration. Desktop Apache PDFBox structural and Android PdfRenderer viewer baselines unchanged. GPL-3.0 PDF Arranger code/modules/fork/runtime prohibited; no Poppler/pikepdf or selected Android structural engine.
- Next P0: real authorized PUBLIC full non-shallow checkout or one justified hosted manual-only workflow, actual `git fsck`/HEAD/clean evidence, then source legal/security admission and reviewed toolchain ADR acceptance, then actual Gradle dependency resolution and all platform gates.
- PRIVATE `ftmstr/uygulama-baslangic-sablonu` **STRICT READ-ONLY**; PUBLIC commits `[skip ci]`, no force push, no gratuitous Actions. **PRODUCTION NOT FINAL**.
