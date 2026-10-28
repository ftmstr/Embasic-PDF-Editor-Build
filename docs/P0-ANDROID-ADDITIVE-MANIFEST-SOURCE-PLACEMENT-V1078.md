# V1078 — P0 Android application migration: collision-free source placement and additive isolated-service plan

**Date:** 2026-10-28 13:07 TRT  
**Status:** proposal + synthetic PoC evidence only — **PRODUCTION NOT FINAL**  
**Canonical PUBLIC baseline at intake:** `31028897ed17d0bfa07dedd96e0df066569a21ee` (V1077).  
**Historical PRIVATE reference (READ-ONLY):** `e4e4b4f6ccd9d838b5ac5434b45fb8202d4ba786`.

## Concrete new engineering finding

A read-only inventory comparison of the historical Android **application** Kotlin roots found **33** product Kotlin files and **7** separately recovered Kotlin files. Comparing paths relative to their respective `src/main/kotlin` roots yielded **0/7 collisions**. These are historical Git-tree observations, not an ownership or current PUBLIC source authorization.

The historical Android application Gradle plugin already uses its conventional `src/main/kotlin` source root; therefore, **after individual rights/license/privacy/provenance clearance**, the minimal candidate migration is to place the seven recovered app Kotlin files into the existing `androidApp/src/main/kotlin/` tree, preserving their relative package paths. **Do not add an external recovered-source Gradle sourceSet merely for these seven app files.** This finding does *not* resolve the separate `shared/commonMain` and `shared/androidMain` recovered source-set dependencies; those still require a controlled two-provenance migration.

The product and recovered Android manifests have the same relative target path, so **never overwrite** the product manifest. The product manifest already contains two activity declarations and privacy/security attributes. Retain those and **add exactly one reviewed isolated-service declaration** after source admission. The historical recovered manifest used a relative service name `.isolated.IsolatedPdfRendererService`; under the product Android namespace `com.embasic.pdfeditor` that would resolve to the wrong class. The recovered Kotlin class declares package `com.embasic.pdfeditor.android.isolated`.

### Independently drafted additive candidate, NOT migrated product source

Only after the seven source files and all references are approved, merge **one** service component into the existing product manifest application element, without replacing other attributes or activities:

```xml
<service
    android:name="com.embasic.pdfeditor.android.isolated.IsolatedPdfRendererService"
    android:exported="false"
    android:isolatedProcess="true"
    android:process=":embasic_pdf_renderer"
    android:stopWithTask="false" />
```

This is an **independently authored proposal**, not a copy of PRIVATE implementation or a claim that the service runs. Full FQCN avoids namespace-relative ambiguity. `exported=false`, private process name, and isolated-process attribute are necessary checks, not sufficient runtime/security proof. Real AGP merged-manifest inspection, component resolution, Binder/Parcel isolation, process death, malformed inputs, and stress tests remain required.

## Actually executed independent synthetic PoC

An offline synthetic Android manifest with two placeholder activities, restrictive application flags, and a stub service source under the conventional Kotlin root was generated. The existing PUBLIC `android_manifest_component_gate.py` was exercised with the candidate manifest:

- Wrong relative service name: **expected GateError** (class missing/package mismatch).
- Full service FQCN: **MECHANICAL_ANDROID_COMPONENT_PASS_ONLY**, **not** Android product PASS.
- Both activity declarations and `allowBackup=false`/`usesCleartextTraffic=false` survive the additive merge.
- Duplicate service insertion fails closed; isolated service attributes and source path are checked.
- **8/8 new synthetic PoC tests PASS**, exit 0.
- Re-ran current PUBLIC-scoped Python tests **42/42 PASS**, exit 0.
- Re-ran isolated Kotlin/JVM compilation exit 0, smoke **45/45 PASS**, exit 0.
- Scoped PUBLIC source Git blob identity **10/10 MATCH**; **not** trusted full checkout.
- Targeted secret-marker scan on three newly authored proposal files PASS; **not** a comprehensive security/license/privacy clearance.

No PRIVATE source bytes, manifest, signing material, binaries, PDF Arranger GPL-3.0 code, or license-uncleared assets were copied or committed. Proposal and synthetic evidence are kept in a separate ZIP for Drive backup; do not treat it as a canonical product tree.

## Remaining P0 release blockers

1. **Trusted full PUBLIC checkout** is still **NOT RUN**. Direct `git ls-remote` still **FAIL** due to DNS exit 128; the manual-only GitHub Actions workflow has **0 actual runs**. This environment has no workflow-dispatch tool; Codex/trusted Git host must run it and capture `GITHUB_SHA`, HEAD, `git fsck`, exit codes and logs.
2. Per-file PRIVATE-to-PUBLIC admission needs legal rights, SPDX/transitive license, secrets/PII, byte-exact vs reconstructed/new provenance, checksum, and human approval. The seven Kotlin files have **NOT** been migrated.
3. Resolve shared recovered-source graph separately, perform real Android AGP manifest merger and Gradle/KMP build, then instrumentation/runtime, dependency verification, SBOM/NOTICE, packaging/signing/rollback gates.
4. Execute V477–latest verifier regressions and PUBLIC reconstruction checksum convergence **after** trusted checkout and approved migration. Historical PRIVATE 41/41 SHA and starter/policy PASS must **not** be promoted to PUBLIC success.

## Required gate truth

Build **NOT RUN**; Unit **NOT RUN**; Integration **NOT RUN**; Android **NOT RUN**; Windows **NOT RUN**; Ubuntu **NOT RUN**; Security **NOT RUN**; Dependency Verification **NOT RUN**; License/SBOM/NOTICE **NOT RUN**; Packaging **NOT RUN**; Signing/Rollback **NOT RUN**. **0/11 production PASS.** PUBLIC Reconstruction **NOT RUN**.

ADR-005 immutable `EditorDocumentState`, `SourceDocumentRef`, `EditorPageRef`, `SelectionState`, `EditorAction`, `EditorExportPlan` and bounded `EditorHistory` remain an independent PoC, **not** a product `commonMain` integration. No large UI rewrite or engine replacement. PDF Arranger GPL-3.0 implementation is prohibited; desktop Apache PDFBox structural backend and Android PdfRenderer viewer baseline retained. Poppler/pikepdf excluded; Android structural engine unselected pending separate PoC/ADR.

PUBLIC-only commits require `[skip ci]`, no force push; PRIVATE strictly READ-ONLY. Actions blackout ended 2026-10-05 00:00 TRT, but no unnecessary Actions dispatch. **PRODUCTION NOT FINAL.**
