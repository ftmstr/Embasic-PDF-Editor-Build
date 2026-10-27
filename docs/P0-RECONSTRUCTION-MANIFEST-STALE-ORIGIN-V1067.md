# V1067 — P0 reconstruction checksum mismatch: historical origin traced

Date: 2026-10-28 03:00 TRT. **PRODUCTION NOT FINAL.**

## Authority / boundaries

Only PUBLIC `ftmstr/Embasic-PDF-Editor-Build` `main` is writable. PRIVATE `ftmstr/uygulama-baslangic-sablonu` is an inactive **READ-ONLY** historical source. No PRIVATE files, third-party implementations, assets, keys, case data or license-unclear source were migrated. This is independently written provenance metadata, not product source or a release claim.

Starting PUBLIC HEAD: `7497bdd8bdb2b5b63b31b71b96e20e040a9e39bf`. The PUBLIC `docs/STATUS.md` remains authoritative. PRIVATE snapshot audited: `e4e4b4f6ccd9d838b5ac5434b45fb8202d4ba786`.

## Root cause: authoritative manifest predates legitimate-looking later edits (not an authorization finding)

The historical `product/RECONSTRUCTION_SHA256SUMS.txt` was last changed on **2026-09-09 19:10:16 UTC** by commit `5ec86225eb9047324772ad2b2a1ae7b55a493e14`. At that exact commit, `product/androidApp/build.gradle.kts` has SHA-256 **e8530e76e90ab5760a581bec28a6ecc96461c3b93130b778e153d5f8215ca506**, **matching** the manifest entry (746 bytes, Git blob `d4b821413230b8e869c70b7eeac99dbe31cc346d`).

The same file was subsequently modified:
- 2026-09-13 commit `fae8ddae497ae54a13ffd0ab8a25e40431f3a212`: SHA-256 `7315ea8f762f180bc85fe8f5b627a4e49bc9b011eef3fba31d778777b5fe283a` (2374 bytes).
- 2026-09-20 commit `1b70a9c126a5ed8b179291a30aac674210031164`: SHA-256 `e366158a614d0fc0bcc5df46a44bdfb20579bcfd1f4af7252a42768addb94c22` (2413 bytes).
- 2026-09-22 commit `ee207716665a302bf97ac30556228ef79030c5cd`: SHA-256 `549a79bd5edcebf07c85a6095c543037a3a1b7b69e7e8d23f79b45b1664c6396` (2490 bytes, Git blob `ee0b0a26433c10bc3020b674f4feb95fafc7c184`).
- The pinned PRIVATE snapshot `e4e4b4f6ccd9d838b5ac5434b45fb8202d4ba786` has the **same** SHA-256 and Git blob as the 2026-09-22 version.

These five SHA-256 results were recomputed from connector-returned **base64-decoded bytes**, with independent SHA-256 implementation checked against the standard empty-string and `abc` vectors (2/2 PASS). The expected manifest hash is therefore **verified as the historical September 9 file content**, while the current historical snapshot contains a later file revision. This establishes **manifest staleness relative to subsequent edits** as the proximate cause of the sampled mismatch. It does **not** establish whether the edits were authorized, whether the latest revision is build-correct, or whether any file is eligible for public release. **Do not blindly rewrite the manifest.**

## Actual V1067 scoped execution

From the previously attached V1066 evidence ZIP, `sha256sum -c` verified all 13 manifest-listed evidence files. Re-executed `python -m unittest -v test_p0_public_checkout.py`: **10/10 PASS**; `test_public_migration_preflight.py`: **14/14 PASS**; Python `py_compile`: PASS; Kotlin 1.9.0/JRE 21 isolated compile: PASS; Kotlin smoke: **45/45 PASS**. All six source/test Git blob IDs matched PUBLIC HEAD `7497bdd8...` via connector read-back. These are **scoped tooling and prototype tests only**; not product Build/Unit/Security gates. Local `git ls-remote` to PUBLIC **FAIL (DNS github.com)**; trusted full checkout **NOT RUN**.

Historical 41-entry manifest: V1066 sampled **2 MATCH / 1 MISMATCH**, remaining **38 NOT RUN** in this V1067 investigation. PUBLIC reconstruction convergence **NOT RUN**. Historical starter 142/142 and policy 17/17 are not PUBLIC PASS.

## P0 next actions

1. Obtain **trusted full PUBLIC checkout** with `python tools/p0_public_checkout.py --help` and the documented runbook, then verify `git fsck --full --strict`, clean tree and exact origin/main/HEAD.
2. Preserve historical manifest as a dated baseline; verify all 41 historical entries against pinned snapshot and at manifest-writing commit; classify each difference with commit history, source rights, secret/PII, license and provenance disposition. Separate `byte_exact_recovery`, `reconstructed`, `new_implementation`. No unreviewed migration.
3. Check shared external source-set closure and Android 7 Kotlin + 1 XML + 1 manifest integration; verify merged manifest and isolated renderer service using actual Gradle and Android tests.
4. Execute V477–latest verifier regressions, strict dependency verification, resolved licenses/SBOM/NOTICE, product build/unit/integration, Android/Windows/Ubuntu, security, packaging and signing/rollback gates. Log **PASS/FAIL/NOT RUN** with commands, exit codes, logs, SHA-256, and platform.

## Clean-room / ADR-005

No PDF Arranger GPL-3.0 source, modules, implementation or runtime dependency copied. No Poppler/pikepdf. Desktop Apache PDFBox structural backend and Android PdfRenderer viewer baseline retained. Android structural engine requires a separate PoC, license/transitive/ABI/package/performance/malformed/stress evidence and ADR; QPDF/PdfBox-Android not preselected. ADR-005 immutable `commonMain` workspace remains an isolated PoC, not integrated production KMP. Do not pursue large UI rewrite/Compose migration ahead of release gates.

All PUBLIC writes `[skip ci]`, no force push, no unnecessary Actions. Blackout ended 2026-10-05 00:00 TRT. PRIVATE strictly READ-ONLY. **PRODUCTION NOT FINAL.**
