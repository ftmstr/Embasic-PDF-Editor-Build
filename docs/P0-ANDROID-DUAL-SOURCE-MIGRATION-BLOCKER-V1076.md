# V1076 — P0 historical dual-source graph and Android isolated-service admission blocker

**2026-10-28 ~11:04 TRT | PRODUCTION NOT FINAL**

## Authority and non-migration boundary

- Only canonical writable repository: `ftmstr/Embasic-PDF-Editor-Build` (PUBLIC), starting HEAD `e3ebdc976082ae46b654b2eb22b6dc8b5b320565` (V1075). PRIVATE `ftmstr/uygulama-baslangic-sablonu` remains strictly READ-ONLY; its `main` was confirmed at historical HEAD `e4e4b4f6ccd9d838b5ac5434b45fb8202d4ba786`.
- This turn **did not migrate any PRIVATE product/recovered-source file**, manifest, XML, asset, binary, credential, or source code into PUBLIC. Only independently authored Python admission tooling/tests and this aggregate metadata report were published, with `[skip ci]`, no force push.
- GitHub Actions GET returned **0 runs**. There is no available workflow-dispatch tool in this execution surface; no run was initiated. Actual `git ls-remote` to PUBLIC still **FAIL**, DNS exit 128. Trusted full PUBLIC checkout **NOT RUN**.

## Concrete source graph discovery — read-only historical metadata

The complete, non-truncated historical PRIVATE Git tree has **399 `product/` blobs** (1,563,857 tree-reported bytes) and **39 `recovered-source/` blobs** (144,465 bytes). The `shared` Gradle module combines both default `product/shared/src` and explicit external `../../recovered-source/shared/src` roots:

| Historical source set | Product Kotlin | Recovered Kotlin | Combined |
|---|---:|---:|---:|
| `shared/commonMain` | 12 | 22 | 34 |
| `shared/androidMain` | 4 | 6 | 10 |
| `shared/desktopMain` | 2 | 0 | 2 |

The declared external roots resolve to real historical tree locations; no relative Kotlin source-path collisions were found across these specific roots. This is **not** a semantic class-name collision scan or a compile result.

**Additional P0 Android migration blocker:** Seven recovered Android application Kotlin files exist outside the product Android application source root, but historical `product/androidApp/build.gradle.kts` has no corresponding external source-root declaration. The recovered Android application also has a separate `AndroidManifest.xml` at the same relative location as the product manifest. The product manifest does not declare the isolated PDF service; the recovered manifest does. Blind file copying would overwrite one manifest and silently lose settings/components.

Read-only XML and Kotlin declaration comparison exposed a further **candidate namespace mismatch**: the recovered manifest's relative isolated-service name would resolve under the product app namespace to a different fully qualified class than the recovered Kotlin service declaration. This is a **migration design blocker**, not evidence of a failing currently built PUBLIC Android app (no product has been migrated). The reviewed migration must preserve product manifest attributes, merge the service explicitly, use a verified fully qualified component name, and compile/bind-test the service on a real device.

**Tests actually executed on GitHub API historical metadata:** **16/16** topology/source-root assertions PASS and **7/7** isolated-service mismatch characterization assertions PASS. These are read-only metadata assertions, **not** product build/security PASS.

## Independently authored PUBLIC migration regression

New files, with no PRIVATE/PDF Arranger source copied:

- `tools/android_manifest_component_gate.py`: read-only, fail-closed mechanical preflight for isolated Android service name resolution, source class/package match, private process, `exported=false`, and malformed/DTD/symlink input rejection. Its PASS explicitly states `production_gate=NOT RUN`.
- `tests/test_android_manifest_component_gate.py`: ten **synthetic** fixtures, including RED-equivalent relative component mismatch and correct fully qualified name. Actual local execution: **10/10 PASS**, exit 0, `py_compile` PASS. Standard-library imports only; targeted secret-marker and prohibited-runtime import scans found no matches. These are **not** license/secret clearance for PRIVATE candidates.

A limited PUBLIC snapshot was assembled from earlier PUBLIC evidence ZIPs plus the new files. **10/10 Git blob identities MATCH** current PUBLIC tree, Python tests **42/42 PASS** exit 0 (10 new + 32 existing), Kotlin standalone workspace **45/45 PASS** after compilation exit 0. This is a **scoped reconstruction**, not a trusted complete Git checkout, Gradle build, Android runtime or product unit acceptance.

## Source rights and supply-chain hold

The historical product Gradle properties had no direct signing password values in the inspected file, and the wrapper properties declare a distribution checksum; this narrow read-only inspection is not a complete secrets or dependency audit. Historical direct runtime license and SBOM files are partial; resolved transitive License/SBOM/NOTICE remains **NOT RUN**. Historical 41/41 SHA, starter 142/142 and policy 17/17 remain PRIVATE evidence, never PUBLIC production PASS.

The 399+39 historical blobs remain **quarantined**, pending trusted PUBLIC checkout, source-by-source rights/privacy/license/secret/provenance decisions and an explicit dual-surface migration plan. No unauthorized source or asset is published.

## Next critical path

1. Obtain one authorized **real** manual GitHub-hosted PUBLIC checkout or trusted host clone. Capture run ID, event SHA, clean non-shallow `main`, `git fsck`, exit/log SHA; do not mistake the current zero Actions runs for PASS.
2. Resolve the historical two-root `shared` source graph and **separate Android app source/manifest collision** in a reviewed migration layout. Preserve `byte_exact_recovery` vs `reconstructed`/`new_implementation` provenance and explicit legal/security clearance.
3. Run `PYTHONPATH=tools python3 -m unittest discover -s tests -p 'test_*.py' -v` in trusted PUBLIC checkout, then V477–latest applicable verifiers, reconstruction checksum convergence, strict resolved Gradle dependency/license/SBOM/NOTICE, real product and platform gates.
4. Implement ADR-005 immutable common workspace in actual `commonMain` only after trustworthy product baseline. Keep desktop Apache PDFBox structural backend, Android PdfRenderer viewer; PDF Arranger GPL-3.0 source/implementation forbidden, Poppler/pikepdf excluded, Android structural engine unselected without separate ADR/PoC.

## Production release gates

| Gate | State |
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
| PUBLIC Reconstruction | NOT RUN |

**0/11 production gates PASS. PRODUCTION NOT FINAL.** The source-graph finding and synthetic tests must not be promoted to production acceptance.
