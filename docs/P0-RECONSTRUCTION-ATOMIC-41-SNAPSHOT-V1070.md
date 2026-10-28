# V1070 — Historical reconstruction manifest has a coherent 41-file Git-tree checkpoint

Date: 2026-10-28 ~06:00 TRT. **PRODUCTION NOT FINAL.**

## Authority and safety
Sole writable repository: `ftmstr/Embasic-PDF-Editor-Build` PUBLIC main. Former PRIVATE `ftmstr/uygulama-baslangic-sablonu` was queried **READ-ONLY** through GitHub GET APIs; no PRIVATE writes, source migration, binaries, assets, secrets or user documents were copied. This file publishes **path, hash and commit metadata only**. A historical Git-tree match is NOT a PUBLIC reconstruction gate PASS or license/rights approval.

## New P0 finding — atomic historical content snapshot located
- Historical 41-entry manifest: `projects/embasic-pdf-editor/product/RECONSTRUCTION_SHA256SUMS.txt` (Git blob `e6b9daf909207c35a33a3201438a60aa67a4310b`), manifest-writing commit `5ec86225eb9047324772ad2b2a1ae7b55a493e14` (2026-09-09).
- **Coherent historical Git commit:** `aa8a1a88c274439d0e825c73acff21a6145cb114` (2026-09-03 05:07:25 UTC; commit message: `test(embasic): add V120 privacy consent fail-closed validator`; tree `46d7c77e86a98a338b679a5d62b9d3f21076fede`).
- GitHub GET `/git/trees/{sha}?recursive=1` returned `truncated=false` for both the manifest-writing tree and candidate tree. **41/41 product-relative manifest paths are present as Git blobs in the single candidate commit and 41/41 blob IDs equal the independently established expected content blob IDs.** Candidate file modes: `100644`, `100755`.
- For the **32** entries that matched the manifest SHA-256 at its writing commit, expected Git blob IDs were taken from that commit's tree; V1068 had already calculated their raw-byte SHA-256 (22 directly + 10 additionally) and established MATCH.
- For the **nine** origin-divergent entries (#4, #22, #26, #29, #30, #35, #36, #37, #39), expected Git blob IDs came from V1069's individually fetched earlier Git revisions with raw-byte SHA-256 **9/9 MATCH**.
- The candidate's 41 Git blob identities were compared **against these 41 previously SHA-256-anchored identities**. This is a **new 41/41 atomic Git-tree identity match**, not a fresh 41-file SHA-256 recomputation or a trusted executable full checkout. Re-run raw SHA-256 against a trusted checkout before PUBLIC convergence certification.
- This finding **supersedes the earlier uncertainty about whether one historical tree exists**. It does NOT authorize automatically restoring the 2026-09-03 revision; later fixes may be security-critical, and product source graph/Gradle/dependency/license/privacy checks remain unresolved.
- Comparison checkpoints: `7d8513f81c38f79fb5d68669f159087ebc168ff6` = 39/41 (two missing tool files); `065a9581e39f00cbac24f353c01fc59bf4b85f6f` = 40/41 (one missing tool); `aa8a1a88c274439d0e825c73acff21a6145cb114` = **41/41**; manifest-writing `5ec86225eb9047324772ad2b2a1ae7b55a493e14` = 32/41; later pinned `e4e4b4f6ccd9d838b5ac5434b45fb8202d4ba786` = 22/41.

## Reproducible Git blob identity evidence (all 41)
Each `expected Git blob SHA-1` equals the candidate commit's blob ID at `projects/embasic-pdf-editor/product/<relative path>`. `MATCH` is a byte-identity assertion from Git object IDs, **not a production gate**.

| # | Relative product path | Expected Git blob SHA-1 | Git mode | Candidate | SHA-256 anchor |
|---:|---|---|---|---|---|
| 1 | `ADR-001-RECONSTRUCTION-PROVENANCE.md` | `4680902eb4383cb917ad942a8b0688a1094894e1` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 2 | `ADR-002-DESKTOP-PDFBOX-BACKEND.md` | `a5c7d5482b8accaba42aec85327c5cb2e632ff48` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 3 | `ADR-003-MONETIZATION-BOUNDARY.md` | `4be7fbf1ee9053dc8e2be61eb60a91e630250b54` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 4 | `DEPENDENCY_DECLARATIONS.md` | `c969ad20a9f130dd77db5793b40a32bccf570cf1` | 100644 | MATCH | V1069 older raw SHA-256 |
| 5 | `androidApp/README_RECONSTRUCTION.md` | `fd1a9631bde56a93981b16fd27fda3e3d6c4d81e` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 6 | `androidApp/build.gradle.kts` | `d4b821413230b8e869c70b7eeac99dbe31cc346d` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 7 | `androidApp/src/main/kotlin/com/embasic/pdfeditor/AndroidPdfViewerActivity.kt` | `4d08702b8a0b3546e75518523a469c96112d4b44` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 8 | `androidApp/src/main/kotlin/com/embasic/pdfeditor/MainActivity.kt` | `6cf5f641dc5cb6b46590a527439d9d1edb49b017` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 9 | `build.gradle.kts` | `ffb206fca8187e7963b180471c46b0c2a0176e53` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 10 | `desktopApp/build.gradle.kts` | `d3fa825ea82d7411bbea963c040b1805c212e365` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 11 | `desktopApp/src/main/kotlin/com/embasic/pdfeditor/desktop/DesktopMain.kt` | `fdecd41f3e0f6f3493cf82ecd812e034fab18ad9` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 12 | `desktopApp/src/main/kotlin/com/embasic/pdfeditor/desktop/DesktopPdfBackend.kt` | `f57dca915498ce752d7cda910c8bbaa3e86a7284` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 13 | `desktopApp/src/main/kotlin/com/embasic/pdfeditor/desktop/RenderGenerationGate.kt` | `98bebbdf9de7b2e75bc735e265f09f64db31906f` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 14 | `desktopApp/src/test/kotlin/com/embasic/pdfeditor/desktop/DesktopPdfBackendTest.kt` | `d4ee291540d13dc94a9d952a1bd606bce9e5a6ed` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 15 | `gradle.properties` | `e0a508bbb02fcfbb593a138c7a414734a8dd324b` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 16 | `gradle/wrapper/gradle-wrapper.jar` | `9bbc975c742b298b441bfb90dbc124400a3751b9` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 17 | `gradle/wrapper/gradle-wrapper.properties` | `ccf4a0811ea88da2fe2f4e35f8bdfd6f282b3562` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 18 | `gradlew` | `faf93008b77e7b52e18c44e4eef257fc2f8fd76d` | 100755 | MATCH | V1068 origin raw SHA-256 |
| 19 | `gradlew.bat` | `9b42019c7915b971238526075306ffba3b666dd5` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 20 | `settings.gradle.kts` | `79f036fa018439a3c4c93eb5b349b30840efc6d3` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 21 | `shared/build.gradle.kts` | `5bfb1afd6b40b9c17ae6d718c7f4102b199d2a61` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 22 | `shared/src/androidInstrumentedTest/kotlin/com/embasic/pdfeditor/reconstructed/AndroidFileTokenLedgerStoreInstrumentedTest.kt` | `000a5684349ded573996e03e2fc6a84661f87d34` | 100644 | MATCH | V1069 older raw SHA-256 |
| 23 | `shared/src/androidMain/kotlin/com/embasic/pdfeditor/androidpdf/AndroidPdfRecentRepository.kt` | `1cd28038df82d45f4b0f46346ae5bb5c373865d7` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 24 | `shared/src/androidMain/kotlin/com/embasic/pdfeditor/androidpdf/AndroidPdfUriValidator.kt` | `6b83eaca43e9573195c0cac454fb8c1ac3ff3af2` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 25 | `shared/src/androidMain/kotlin/com/embasic/pdfeditor/androidpdf/AndroidRecentPdfResolver.kt` | `46d871b1166e83b8ea1be08b110e2580ee4c54b4` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 26 | `shared/src/androidMain/kotlin/com/embasic/pdfeditor/reconstructed/AndroidFileTokenLedgerStore.kt` | `07ae35970b0cab75c0b52ee63fa2d440fa31de5a` | 100644 | MATCH | V1069 older raw SHA-256 |
| 27 | `shared/src/commonMain/kotlin/com/embasic/pdfeditor/reconstructed/MonetizationPolicy.kt` | `4d78762143a8341b10683fb8276bfd18eca916c5` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 28 | `shared/src/commonMain/kotlin/com/embasic/pdfeditor/reconstructed/PdfRenderSizePolicy.kt` | `26be0ad8c58325a0c2557fad50dc25bf766bf793` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 29 | `shared/src/commonMain/kotlin/com/embasic/pdfeditor/reconstructed/TokenLedger.kt` | `6cd39b3090c4938e7cfba00e6636bbf5123495a9` | 100644 | MATCH | V1069 older raw SHA-256 |
| 30 | `shared/src/commonMain/kotlin/com/embasic/pdfeditor/reconstructed/TokenLedgerStateCodec.kt` | `d30648587a314b6bba78756a9b2f35bdb2cc36b7` | 100644 | MATCH | V1069 older raw SHA-256 |
| 31 | `shared/src/commonTest/kotlin/com/embasic/pdfeditor/integration/PdfViewerControllerIntegrationTest.kt` | `f44d910b56efe396ea03eadeeac45c234599b5f2` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 32 | `shared/src/commonTest/kotlin/com/embasic/pdfeditor/pdf/PdfNavigationPolicyTest.kt` | `639ebdaa64b297cac6ec274531e151611d8e9b63` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 33 | `shared/src/commonTest/kotlin/com/embasic/pdfeditor/reconstructed/MonetizationPolicyTest.kt` | `eaaa99479bc7b700daaca6206f0ce5f2ed760295` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 34 | `shared/src/commonTest/kotlin/com/embasic/pdfeditor/reconstructed/PdfRenderSizePolicyTest.kt` | `c8be3c75e7123c674bb1e1342a1b0cae8de8fd84` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 35 | `shared/src/commonTest/kotlin/com/embasic/pdfeditor/reconstructed/TokenLedgerStateCodecTest.kt` | `2e089c6d41b3366e74b01f18992e05b07c4660a5` | 100644 | MATCH | V1069 older raw SHA-256 |
| 36 | `shared/src/commonTest/kotlin/com/embasic/pdfeditor/reconstructed/TokenLedgerTest.kt` | `846d7750955b26f557ad7b67b91a55cdfa6b4af5` | 100644 | MATCH | V1069 older raw SHA-256 |
| 37 | `shared/src/desktopMain/kotlin/com/embasic/pdfeditor/reconstructed/DesktopFileTokenLedgerStore.kt` | `eda8b0e927e192bfef8aff8076e6279bb226050e` | 100644 | MATCH | V1069 older raw SHA-256 |
| 38 | `shared/src/desktopMain/kotlin/com/embasic/pdfeditor/time/EpochClock.jvm.kt` | `c6c8305a740f97b4cbc252d15c2d9e376e7aa35e` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 39 | `shared/src/desktopTest/kotlin/com/embasic/pdfeditor/reconstructed/DesktopFileTokenLedgerStoreTest.kt` | `79fec8be9f68258e0d2b50d8b0756a2e7e1b9d3b` | 100644 | MATCH | V1069 older raw SHA-256 |
| 40 | `tools/check_ad_privacy_consent_policy.py` | `1ef7962de25a11872cd48cfc1b7173a62363efbf` | 100644 | MATCH | V1068 origin raw SHA-256 |
| 41 | `tools/check_monetization_ui_boundary.py` | `fe09d8fb9b1416245a5f06e60679050580630cb6` | 100644 | MATCH | V1068 origin raw SHA-256 |

## Executed scoped checks and limitations
- Historical GET tree inspection: 2 trees, both `truncated=false`; 41/41 expected paths resolved; 41/41 candidate blob identity matches. Candidate is a **single historical commit**, not a mixed per-file reconstruction.
- Locally re-executed isolated PUBLIC evidence (separate Linux runtime): Python checkout fixtures **10/10 PASS** + migration preflight **14/14 PASS**, Python `py_compile` PASS; Kotlin/JVM prototype **45/45 PASS**. These are **not product Build/Unit/Integration/Security PASS**.
- Executable `git ls-remote` PUBLIC **FAIL** (DNS `github.com`, exit 128); trusted complete PUBLIC checkout **NOT RUN**.
- PUBLIC source migration, V477–latest product regressions, authoritative starter/policy revalidation, full PUBLIC reconstruction checksum convergence, strict dependency verification, resolved license/SBOM/NOTICE, real Gradle/platform tests, packaging/signing/rollback **NOT RUN**. Historical PRIVATE starter 142/142 and policy 17/17 must not be promoted.
- Production gates: Build **NOT RUN**; Unit **NOT RUN**; Integration **NOT RUN**; Android **NOT RUN**; Windows **NOT RUN**; Ubuntu **NOT RUN**; Security **NOT RUN**; Dependency Verification **NOT RUN**; License/SBOM/NOTICE **NOT RUN**; Packaging **NOT RUN**; Signing/Rollback **NOT RUN**. **0/11 PASS**. PUBLIC Reconstruction **NOT RUN**.

## P0 engineering path
1. On a trusted Git-capable Codex/local host, checkout PUBLIC `main`, verify `git fsck --full --strict`, `git rev-parse --is-shallow-repository` false, clean tree and exact origin/main HEAD. Preserve PRIVATE strictly READ-ONLY.
2. In a **separate temporary read-only historical checkout**, verify 41 SHA-256 values at candidate `aa8a1a88...` using the historical manifest; capture logs. Keep that historical snapshot distinct from the later product baseline.
3. Review all later changes (especially security/Android ledger/Gradle) and product + recovered-source + Android manifest source graph; license/secret/PII/provenance scan and human rights clearance before any allowlisted PUBLIC migration. Never blindly revert to old code or overwrite manifest.
4. Run V477–latest verifier regressions, PUBLIC checksum convergence, strict dependency verification/resolved license/SBOM/NOTICE, Gradle build/unit/integration and Android/Windows/Ubuntu runtime, security, packaging, signing/rollback.
5. ADR-005 remains isolated Kotlin PoC pending verified product baseline. PDF Arranger GPL-3.0 source/modules/implementation/runtime dependency excluded; desktop Apache PDFBox structural and Android PdfRenderer viewer baselines retained; no Poppler/pikepdf or premature Android engine/Compose selection.

Actions blackout ended 2026-10-05 00:00 TRT; avoid unnecessary dispatch. All PUBLIC writes `[skip ci]`; no force push. PRIVATE READ-ONLY. **PRODUCTION NOT FINAL.**
