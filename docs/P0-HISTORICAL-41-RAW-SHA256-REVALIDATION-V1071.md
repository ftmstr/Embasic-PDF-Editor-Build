# V1071 — Fresh raw-byte SHA-256 check of the coherent 41-file historical reconstruction snapshot

Date: 2026-10-28 ~07:00 TRT. **PRODUCTION NOT FINAL.**

## Canonical authority and safety
- Sole writable repository: `ftmstr/Embasic-PDF-Editor-Build` PUBLIC main; starting HEAD `23081eba4af28035595b7f410349f728a5ae64ba`. PRIVATE `ftmstr/uygulama-baslangic-sablonu` was accessed **READ-ONLY**.
- Historical manifest commit: `5ec86225eb9047324772ad2b2a1ae7b55a493e14`; manifest blob `e6b9daf909207c35a33a3201438a60aa67a4310b`.
- Historical coherent candidate: `aa8a1a88c274439d0e825c73acff21a6145cb114`, tree `46d7c77e86a98a338b679a5d62b9d3f21076fede` (2026-09-03). This is **not** a current source baseline.
- No PRIVATE source code, binary, user data, credentials, third-party implementation or assets were migrated/published. Only previously public historical path/hash metadata is documented here.

## New executed finding: 41/41 raw-byte SHA-256 MATCH
In six read-only connector batches (indices 1–7, 8–14, 15–21, 22–28, 29–35, 36–41), the exact 41 files were fetched from historical candidate commit `aa8a1a88...` using GitHub file reads with Base64 encoding. Each response was decoded to raw bytes *inside the execution isolate* and hashed with a SHA-256 implementation checked against standard empty-string and `abc` vectors (**2/2 PASS**). Every computed SHA-256 was compared with the original 41-entry manifest, rather than with a silently rewritten baseline.

**Observed: 41 MATCH / 0 MISMATCH / 0 NOT RUN; 165,341 historical bytes.** The 43,705-byte Gradle wrapper JAR was included in the raw-byte audit. Git blob identities also agree with the V1070 per-file historical tree record. No private raw bytes were retained in the PUBLIC repository.

This materially strengthens V1070's 41/41 Git-blob identity result: the historical manifest now has a **fresh, per-file, raw-byte SHA-256 check against a single coherent historical commit**. It does **NOT** prove a trusted executable checkout, up-to-date product source, security fixes, licensing/rights clearance, PUBLIC reconstruction checksum convergence or production readiness. In particular, later PRIVATE snapshots were known to diverge; do not roll back subsequent security/Android/Gradle fixes or copy historical code without approval.

## Verified digest index
Each digest below was recomputed from candidate raw bytes and equals the original manifest entry. Full PRIVATE bytes are deliberately excluded.

| # | Historical product-relative path | Observed = manifest SHA-256 | Result |
|---:|---|---|---|
| 1 | `ADR-001-RECONSTRUCTION-PROVENANCE.md` | `d62e951b14e5da752dff2b4ea4900856f3ceff93e8127a9e4dbb237ec423f442` | MATCH |
| 2 | `ADR-002-DESKTOP-PDFBOX-BACKEND.md` | `caa89aea7ab79d47b568ade07e21c5be67c4f3416b921d7b460958c58cefd152` | MATCH |
| 3 | `ADR-003-MONETIZATION-BOUNDARY.md` | `b437bc8810f870dee91e5a0cc24b302f26df794fb1c368b0128435dc93ba24b1` | MATCH |
| 4 | `DEPENDENCY_DECLARATIONS.md` | `17b303957685e4908e5347b0e0b06a8481530f4bb8271fee37f6a923ccecc67c` | MATCH |
| 5 | `androidApp/README_RECONSTRUCTION.md` | `c09ff174d3385fdf00b5eec1703ea788bb090f29b36c036d04acca7745f5784c` | MATCH |
| 6 | `androidApp/build.gradle.kts` | `e8530e76e90ab5760a581bec28a6ecc96461c3b93130b778e153d5f8215ca506` | MATCH |
| 7 | `androidApp/src/main/kotlin/com/embasic/pdfeditor/AndroidPdfViewerActivity.kt` | `6a23ba0a985335dd6dcaa8fc0f320c90ca38b6ed765c4b8ce44f5d7585911a7c` | MATCH |
| 8 | `androidApp/src/main/kotlin/com/embasic/pdfeditor/MainActivity.kt` | `ba7efaee6d36649ad9f72b829eeae90ffffdaf7f377741bddb32ea38f42db816` | MATCH |
| 9 | `build.gradle.kts` | `569d68015ca3208fcb501a010c834346741eca191b2d1a75a7ac498e890bd2de` | MATCH |
| 10 | `desktopApp/build.gradle.kts` | `f45469eda469e93850e7ef7e274a6e46fe19ef5aa1080035006f5d8cd1155955` | MATCH |
| 11 | `desktopApp/src/main/kotlin/com/embasic/pdfeditor/desktop/DesktopMain.kt` | `516a48f1243a2b920120fd24c3c7e65e2af5711052e7cb00526bbe1134816f7e` | MATCH |
| 12 | `desktopApp/src/main/kotlin/com/embasic/pdfeditor/desktop/DesktopPdfBackend.kt` | `3389538f453ce895e046eabd1fe68c825c10d7e5a6e16945b2493100eb05a214` | MATCH |
| 13 | `desktopApp/src/main/kotlin/com/embasic/pdfeditor/desktop/RenderGenerationGate.kt` | `3f6fdeac1c49d47d9537e36d7d16ca152dee9bafc854dc8ff8c767468f474804` | MATCH |
| 14 | `desktopApp/src/test/kotlin/com/embasic/pdfeditor/desktop/DesktopPdfBackendTest.kt` | `37b94c867e1c131828270c21636e30fb78247febf34cd767539741f7f4650733` | MATCH |
| 15 | `gradle.properties` | `9f6e0b3fe4774a20371add12421271166fa7ade24758f4fed0f2eb48ea0261b0` | MATCH |
| 16 | `gradle/wrapper/gradle-wrapper.jar` | `81a82aaea5abcc8ff68b3dfcb58b3c3c429378efd98e7433460610fecd7ae45f` | MATCH |
| 17 | `gradle/wrapper/gradle-wrapper.properties` | `1bb6d43ff8af30abb0eaf03fe58f636ed9b37f758a748bf30a9cebd809639c9d` | MATCH |
| 18 | `gradlew` | `734b3879d3501dce471cf0522d3bcbafe76873d9fc5129345b67fb43bd15e933` | MATCH |
| 19 | `gradlew.bat` | `57931b17dd228e5c24dac90e815d0bf82477e831a4618dfab4136f5446b42a9f` | MATCH |
| 20 | `settings.gradle.kts` | `e3d6f654ea6998d227083bc0e3ed515004f211091baf99563370516c8b0a151f` | MATCH |
| 21 | `shared/build.gradle.kts` | `8ed45b4e29e9d7683b6495196bbcda45d3691339bd41bdc993be6861cc26051d` | MATCH |
| 22 | `shared/src/androidInstrumentedTest/kotlin/com/embasic/pdfeditor/reconstructed/AndroidFileTokenLedgerStoreInstrumentedTest.kt` | `ae3b430e3da6deac543e1d8c23b87563e809c3322f0b13a38360bba88cb469aa` | MATCH |
| 23 | `shared/src/androidMain/kotlin/com/embasic/pdfeditor/androidpdf/AndroidPdfRecentRepository.kt` | `6dedb1dce45e689f6f7b77032288d2e86bb296a65a951c5dba71d602014919ae` | MATCH |
| 24 | `shared/src/androidMain/kotlin/com/embasic/pdfeditor/androidpdf/AndroidPdfUriValidator.kt` | `6b117d812ca85141346fe36187d33c0e8cef8ce6596bdd412dccd367c25295fd` | MATCH |
| 25 | `shared/src/androidMain/kotlin/com/embasic/pdfeditor/androidpdf/AndroidRecentPdfResolver.kt` | `832c9aaa6abd84faa861481fd2f927974c6fa602620e07717be7685e3b6ed5f7` | MATCH |
| 26 | `shared/src/androidMain/kotlin/com/embasic/pdfeditor/reconstructed/AndroidFileTokenLedgerStore.kt` | `f88f6e3640f0dd4d9202572b566bf25f405c2b4156a3b5722267731fcdfcf850` | MATCH |
| 27 | `shared/src/commonMain/kotlin/com/embasic/pdfeditor/reconstructed/MonetizationPolicy.kt` | `91c751bfe32e35c038899b62a20002e8e71852ef6afebeeeef6808082ba66096` | MATCH |
| 28 | `shared/src/commonMain/kotlin/com/embasic/pdfeditor/reconstructed/PdfRenderSizePolicy.kt` | `2cdfdbb78c641351510d35a4e3e434781a239666dca9cbee6d3d7822e7e733c9` | MATCH |
| 29 | `shared/src/commonMain/kotlin/com/embasic/pdfeditor/reconstructed/TokenLedger.kt` | `9a7f6d443feced72bee7ad6d7bdf76d03eb02bf1c3b1868e3b51683945976e44` | MATCH |
| 30 | `shared/src/commonMain/kotlin/com/embasic/pdfeditor/reconstructed/TokenLedgerStateCodec.kt` | `5bde790dbfc57c304bf367815178ac01543c5d30d721da3c5a91ad25d0392530` | MATCH |
| 31 | `shared/src/commonTest/kotlin/com/embasic/pdfeditor/integration/PdfViewerControllerIntegrationTest.kt` | `901cf12b313ed421faf6ec1c2a3653cfce24274376b7c93ee022a01593d00ae1` | MATCH |
| 32 | `shared/src/commonTest/kotlin/com/embasic/pdfeditor/pdf/PdfNavigationPolicyTest.kt` | `b4488b90f70fdd527f4c18428024188604ad3881192f97c29152182a60775b3a` | MATCH |
| 33 | `shared/src/commonTest/kotlin/com/embasic/pdfeditor/reconstructed/MonetizationPolicyTest.kt` | `360eccbc02b4bcb6e08a341b1e4b113f1c776d2f7c94e0a6f99b055793b44067` | MATCH |
| 34 | `shared/src/commonTest/kotlin/com/embasic/pdfeditor/reconstructed/PdfRenderSizePolicyTest.kt` | `cab033d714473e324ee5e118d6e183765682ca52e4074398ec15bcdd8b6b5291` | MATCH |
| 35 | `shared/src/commonTest/kotlin/com/embasic/pdfeditor/reconstructed/TokenLedgerStateCodecTest.kt` | `85e16f2002bf8fae50b8eb70e32e6795a5e43953ed8f4295df09b2e0e8ea5251` | MATCH |
| 36 | `shared/src/commonTest/kotlin/com/embasic/pdfeditor/reconstructed/TokenLedgerTest.kt` | `2ab7e002265de59cff1efa68e0605216ee21631b26cab9f823b595ea34d3deef` | MATCH |
| 37 | `shared/src/desktopMain/kotlin/com/embasic/pdfeditor/reconstructed/DesktopFileTokenLedgerStore.kt` | `f63abe30ecde1b996d41216f34b0a0efb8983fbe57d498264bccc5e5976c6726` | MATCH |
| 38 | `shared/src/desktopMain/kotlin/com/embasic/pdfeditor/time/EpochClock.jvm.kt` | `a48ef8051a41bc92ca98db5f216258746eddcd42c4c393d1140782bb7066f43e` | MATCH |
| 39 | `shared/src/desktopTest/kotlin/com/embasic/pdfeditor/reconstructed/DesktopFileTokenLedgerStoreTest.kt` | `7635c3fcb1ba78884f1571d1ee042eed0f40c5f02c62498f0bc70fd5f9ab8169` | MATCH |
| 40 | `tools/check_ad_privacy_consent_policy.py` | `1bf3b2a6deb1a235758d91865d6e60ec90c6899ca0eed8de6799c44295abb0fe` | MATCH |
| 41 | `tools/check_monetization_ui_boundary.py` | `c0507b86b2923c7897c918a891ff523a43e5a34a2dc94fcfef9525c8c57561b4` | MATCH |

## Independently executed scoped tests in this turn
- PUBLIC-source-matched isolated Python checkout fixtures **10/10 PASS**; migration preflight **14/14 PASS**; Python `py_compile` PASS.
- Isolated Kotlin/JVM workspace compile PASS and smoke **45/45 PASS**.
- Six locally executed source/test files matched the corresponding PUBLIC main Git blob IDs **6/6 PASS**. These are **tool/PoC tests only**, not product Unit, Integration, Build or Security gate PASS.
- Direct `git ls-remote` to PUBLIC **FAIL** (DNS `github.com`, exit 128). Trusted full PUBLIC checkout **NOT RUN**.

## Remaining production release gates
Build **NOT RUN**; Unit **NOT RUN**; Integration **NOT RUN**; Android **NOT RUN**; Windows **NOT RUN**; Ubuntu **NOT RUN**; Security **NOT RUN**; Dependency Verification **NOT RUN**; License/SBOM/NOTICE **NOT RUN**; Packaging **NOT RUN**; Signing/Rollback **NOT RUN**. **0/11 PASS**. PUBLIC reconstruction **NOT RUN**; V477–latest regressions **NOT RUN**; starter 142/142 and policy 17/17 historical records were not rerun on PUBLIC.

## Immediate P0 path
1. Obtain **trusted full PUBLIC checkout** on Git-capable Codex/local host; verify `git fsck --full --strict`, `origin/main`, clean worktree, non-shallow checkout and repository provenance. Keep PRIVATE strictly READ-ONLY.
2. On a separate read-only historical checkout, independently reproduce the 41 raw SHA-256 matches with `sha256sum -c`; retain logs, distinguish this historical baseline from latest security-corrected source.
3. Review latest product + recovered-source + Android source-set/manifest closure and later security changes; scan secrets, personal data, licenses, transitive dependencies and provenance; allowlist only approved files for PUBLIC migration. Do not auto-restore old code or rebaseline stale manifests.
4. Run V477–latest regressions, PUBLIC checksum convergence, strict Gradle dependency verification, resolved License/SBOM/NOTICE, actual product build/unit/integration, Android/Windows/Ubuntu runtime, security, packaging, signing/rollback.
5. ADR-005 immutable `commonMain` workspace is **isolated PoC**, not product integration. PDF Arranger GPL-3.0 code/modules/runtime excluded; desktop Apache PDFBox structural and Android PdfRenderer viewer baselines retained. No Poppler/pikepdf or premature Android structural engine/Compose selection.

Actions blackout ended 2026-10-05 00:00 TRT; do not dispatch unnecessary Actions. All PUBLIC writes `[skip ci]`; no force push; PRIVATE READ-ONLY. **PRODUCTION NOT FINAL.**
