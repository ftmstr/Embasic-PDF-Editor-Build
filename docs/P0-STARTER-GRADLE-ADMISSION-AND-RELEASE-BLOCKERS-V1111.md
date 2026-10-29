# V1111 — P0 Uploaded Starter Admissibility and REAL Gradle Release Blockers

**Evidence date:** 2026-10-29 ~20:31 TRT. **PRODUCTION NOT FINAL.**

## Canonical PUBLIC scope

Initial (and rechecked prior to this documentation write) PUBLIC `main` HEAD: `01fc6600a2422093e26961c501845de8faec22f9`, `docs/STATUS.md` V1108. Latest Google Drive report before the turn: V1110; **Drive reports are not newer GitHub source checkpoints**. Only PUBLIC `ftmstr/Embasic-PDF-Editor-Build` may be modified. Historical PRIVATE `ftmstr/uygulama-baslangic-sablonu` is **READ-ONLY**, was not written, and its old PASS results cannot certify PUBLIC.

GitHub Actions GET reports **0 runs**. Executable `git ls-remote https://github.com/ftmstr/Embasic-PDF-Editor-Build.git HEAD`: **FAIL, exit 128**, DNS `Could not resolve host: github.com`. No connector action is available to dispatch `workflow_dispatch` in this execution environment; actual GitHub-hosted workflow **NOT RUN**. Thus a trusted complete non-shallow PUBLIC clone, `origin/main` and `git fsck` admission **NOT RUN**. Public API tree/blob reads are not such a clone.

## Concrete new P0 finding — user-provided starter is NOT a drop-in recovered PDF Editor

The **user-uploaded** `Uygulama_Baslangic_Sablonu_v1.3.1(4).zip` was examined without extracting any source into PUBLIC. Its archive SHA-256 is `ff50a26027b1d3d8e34d846d1bfcb0ffe96929875a70ce72c1eb97b1177fb4f1`; prior V1106 verified the ZIP's own **142/142** payload hashes and separately the policy **17/17** uploaded files. **Those checks authenticate uploaded inputs only.**

This turn used Python stdlib ZIP/TOML parsing and a temporary isolated extraction for **scoped** starter policy scripts. The following were actually observed:

| Checked fact / release gate | Observed evidence | Classification |
|---|---|---|
| Starter file inventory | 143 file entries: 142 payload files + internal checksum manifest | static observation |
| Standard Gradle launchers | `gradlew`, `gradlew.bat`, `gradle/wrapper/gradle-wrapper.jar` all **ABSENT** | **BLOCKED**: cannot execute `./gradlew` from this ZIP |
| Strict Gradle metadata | `gradle/verification-metadata.xml` **ABSENT** | **BLOCKED**: strict verification not established |
| Resolved runtime licenses | `licenses/TRANSITIVE_RUNTIME_LICENSES.csv` only header; `build/reports/oss/resolved-runtime-components.txt` absent | **BLOCKED**: no actual resolved runtime licensing evidence |
| Final third-party notices | `THIRD_PARTY_NOTICES.md` explicitly `**Release-Status: NOT_FINAL**` | **BLOCKED** for release |
| ZIP's declared build versions | Gradle `9.3.1`, AGP `9.1.0`, Kotlin `2.4.10`, Compose Multiplatform `1.11.1` | **DECLARED ONLY**, not officially reverified |
| Historical PDF product Gradle declarations | Gradle `8.13`, AGP `8.13.2`, Kotlin `2.3.20` per PUBLIC `docs/P0-PUBLIC-MIGRATION-BLOCKER-MAP.md` | **DIFFERENT LINEAGE**, no automatic combination |
| Project identity | Generic `KmpAppStarter` with `:shared`, `:androidApp`, `:desktopApp`; three Gradle module scripts do not directly declare PDFBox | **NOT** a complete functional Embasic PDF Editor |
| Current PUBLIC repository tree | No full migrated product/root Gradle wrapper/modules at this checkpoint | actual PUBLIC Build/Unit/Integration **NOT RUN** |

**Actual isolated script execution:** `python3 scripts/check-oss-policy.py` **exit 0**, `python3 scripts/check-supply-chain.py` **exit 0**; `python3 scripts/check-dependency-verification.py` **exit 1** (missing XML); `python3 scripts/check-release-notices.py` **exit 1** (`NOT_FINAL`); `python3 scripts/audit-resolved-runtime-licenses.py` **exit 2** (missing resolved graph). These are **5/5 expected outcomes**, NOT 5 product-gate PASS. The failed release scripts are genuine **release blockers**, not benign warnings.

The independent one-off starter ZIP metadata audit initially yielded **13/14**, because a naive substring check misidentified an explanatory sentence mentioning `Release-Status: FINAL`; an anchored status-line check corrected this and re-execution gave **14/14 scoped metadata assertions PASS**. This correction was to the audit **fixture**, not product source. No external dependencies downloaded.

## Required decision to resume P0 migration (NO unreviewed source publication)

1. **Real authorized PUBLIC full checkout** via network-enabled Codex host or one justified manual hosted workflow. Record event SHA, checkout HEAD, origin/main, remote SHA, non-shallow/clean before and after tests, `git fsck`, command exit/log and digest. Do not use a GitHub API snapshot as checkout PASS.
2. Establish a **single reviewed product Gradle lineage** before any template-to-product copy. The user-uploaded v1.3.1 version catalog cannot be combined with historical product Gradle versions or Android source-set layout without current official SDK/API/dependency/license compatibility checks and ADR, and cannot be accepted as a missing Gradle wrapper.
3. Review **51 historical Kotlin candidates** with explicit source rights, privacy/PII, secrets, asset, SPDX/transitive license and provenance approvals; until then all remain **BLOCKED**. Resolve shared `product` vs `recovered-source` source roots plus Android isolated service/manifest collision. Keep `byte_exact_recovery`, `reconstructed`, and `new_implementation` segregated.
4. Obtain exact Gradle wrapper binary from authenticated supported distribution only after validating the declared Gradle and plugin matrix; validate wrapper JAR/checksum. Generate Gradle verification metadata from a real **resolved** graph, verify strict mode, resolved runtime/test/plugin licenses, full SBOM/NOTICE; do **not** fabricate a passing `verification-metadata.xml` or change `NOT_FINAL` to `FINAL` without evidence.
5. Run V477–latest product verifier regressions, PUBLIC reconstruction convergence, actual KMP/Gradle Build/Unit/Integration, Android/Windows/Ubuntu runtime, security/malformed/stress, packaging/signing/rollback. Record exact PASS/FAIL/NOT RUN.

## Current release-gate truth and dashboard ETA

**Build, Unit, Integration, Android, Windows, Ubuntu, Security, Dependency Verification, License/SBOM/NOTICE, Packaging, Signing/Rollback = all NOT RUN; 0/11 production PASS.** PUBLIC reconstruction NOT RUN. User's requested color PowerShell dashboard should show **0% verified gate coverage (NOT project completion)**. Previous scenario of **12–24 weeks after** trusted checkout, rights-cleared source and platform test environments is conditional only; these prerequisites remain unmet. No defensible committed FINAL date.

ADR-005 immutable workspace remains standalone Kotlin/JVM PoC, not production `commonMain`. PDF Arranger GPL-3.0 implementation and Poppler/pikepdf runtime remain excluded. Desktop Apache PDFBox structural and Android PdfRenderer viewer baselines remain unchanged. Android structural engine requires separate ADR/PoC/SPDX/ABI/size/performance/malformed/stress evidence.

All PUBLIC commits: `[skip ci]`; no force push; do not touch PRIVATE; no gratuitous Actions. **PRODUCTION NOT FINAL.**
