# V1114 — PUBLIC Exact-Blob Kotlin/Python Rerun on API-Scoped Sources

**Date:** 2026-11-08 ~14:35 TRT. **PRODUCTION NOT FINAL.**

## Canonical intake and P0 checkout blocker

- PUBLIC-only repository `ftmstr/Embasic-PDF-Editor-Build`, starting `main` HEAD `a88dba8b49c3c38642272f486d0274318052a588` (STATUS V1113). Last V1113 native Google Drive Rapor/Codex and authoritative starter/policy, PUBLIC recovery and historical reconstruction references reviewed. Historical PRIVATE `ftmstr/uygulama-baslangic-sablonu`: **READ-ONLY**, no writes, actions, PR, deletion, migration.
- GitHub Actions read-only GET: **0 runs**; connector has no dispatch action. No workflow triggered. Actual local `git ls-remote --exit-code https://github.com/ftmstr/Embasic-PDF-Editor-Build.git refs/heads/main`: **FAIL exit 128 / DNS**. Re-running the exact PUBLIC one-shot `tools/p0_public_checkout_once.sh`: **FAIL exit 128 / stage CLONE**, `head=null` and no product/scoped tests run by that runner. New real attempt log SHA-256 `7aa1a94b44154fa5869157d1adb3ef8c02633f85cd381f8866d1711a82983adb`.
- **Trusted full PUBLIC non-shallow Git checkout, full Git-object `fsck`, remote equality and clean pre/post release gate: NOT RUN.** API tree and locally reconstructed source files do not constitute a Git checkout.

## Concrete engineering execution on exact current PUBLIC code

Instead of adding more verifier code or publishing unlicensed PRIVATE source, this turn **executed current PUBLIC code** verified against canonical Git tree blob hashes:

1. Extracted **six exact source/test blobs** from prior evidence ZIPs. Their Git blob SHA-1 values matched the current PUBLIC tree, including the V1113 `SIGPIPE/gitlink` fix; mismatching or stale archive entries were **refused**, not used.
2. Reconstructed the two CURRENT independently authored Kotlin prototype files **from earlier locally verified sources plus official PUBLIC GitHub commit patches** (GitHub compare V1074→V1106 and V1107/V1108 commits). Computed Git blob hashes of the resulting bytes before testing:
   - `EditorWorkspace.kt`: **`cc20f008a4a1efe48688b69ca5293585ab9acbd5` MATCH**, 12,116 bytes.
   - `EditorWorkspaceSmoke.kt`: **`705d8b12ba84a1dfddc1027b7409506400f31ad7` MATCH**, 16,902 bytes.
3. **Total: 8/8 exact PUBLIC Git blob content identities MATCH.** Local snapshot is explicitly `PARTIAL_EXACT_PUBLIC_BLOB_SNAPSHOT_NOT_GIT_CHECKOUT`; not a full PUBLIC tree (some newer tests and the workflow are absent from the local subset).
4. Ran `PYTHONPATH=<isolated tools dir> PYTHONPYCACHEPREFIX=<outside source> python3 -m unittest discover -s tests -p 'test_*.py' -v`: **35/35 PASS**, exit 0. Includes actual PUB-scoped Python checkout, migration-preflight and V1113 runner regressions. Python test discovery is **partial**, so do not claim complete PUBLIC Python suite or product Unit.
5. Ran `kotlinc -J-Xmx768m EditorWorkspace.kt EditorWorkspaceSmoke.kt -include-runtime -d <outside source>/editor-workspace-v1114-isolated.jar` and `java -Xmx768m -jar <jar>`: compilation exit 0, **48/48 Kotlin/JVM PoC scenarios PASS**, exit 0. Includes 8k source import/selection and 10k page move/rotate/delete/undo/redo/export tests. This is actual current PUBLIC clean-room prototype bytecode, **not Gradle/KMP product integration**.
6. `bash -n tools/p0_public_checkout_once.sh` PASS. Source-only pattern scan of eight blobs initially flagged `api_key = 'abcdefgh1234567890'` in `tests/test_public_migration_preflight.py`, explicitly a synthetic **negative secret detection test fixture**. Not a production secret. No complete credential/asset/transitive dependency scan was performed; real Security gate **NOT RUN**.
7. Independently reran user-uploaded authoritative input integrity verifier: starter ZIP **142/142 SHA-256 MATCH** (archive SHA-256 `ff50a26027b1d3d8e34d846d1bfcb0ffe96929875a70ce72c1eb97b1177fb4f1`) and 17 policy Markdown files **17/17 MATCH**. Input-only results; **not PUBLIC reconstruction/License gate**.

No PRIVATE or historical production code was copied or published. No PRODUCT source/architecture/Gradle dependency changes were made in this turn: until approved complete checkout and rights, doing so would bypass P0.

## Remaining blockers and release gates

- PUBLIC currently lacks approved full PDF Editor root Gradle wrapper/configuration and functional platform module/sourceSets. Historical user-upload generic starter is *not* a working Editor build; incomplete strict verification metadata, resolved transitive licenses and FINAL NOTICE.
- Historical **51 Kotlin candidates remain BLOCKED** for source rights/privacy, secrets, SPDX/transitives, assets and provenance; dual product/recovered-source roots and Android isolated service/manifest resolution remain open.
- V477–latest complete verifier regression chain on a **trusted PUBLIC checkout**, PUBLIC reconstruction checksum convergence, strict Gradle resolved graph/SBOM/NOTICE, real Android/Windows/Ubuntu and installer/signing/rollback **NOT RUN**.
- Product Build **NOT RUN**; Unit **NOT RUN**; Integration **NOT RUN**; Android **NOT RUN**; Windows **NOT RUN**; Ubuntu **NOT RUN**; Security **NOT RUN**; Dependency Verification **NOT RUN**; License/SBOM/NOTICE **NOT RUN**; Packaging **NOT RUN**; Signing/Rollback **NOT RUN**. **0/11 production PASS**; PUBLIC reconstruction **NOT RUN**.
- Progress panel: **0% verified release gate coverage (NOT overall project completion)**. Conditional 12–24 weeks only **after** trusted checkout, source rights clearance, real platform test environments. If hypothetically prerequisites were met 2026-11-08, 2027-01-31 through 2027-04-25. They are **not met**; no defensible committed FINAL date.

## Clean-room and ADR-005

Do not import GPL-3.0 PDF Arranger implementation, fork/modules/runtime; no Poppler/pikepdf or preapproved Android structural engine. Preserve desktop Apache PDFBox structural and Android PdfRenderer viewer baseline. ADR-005 immutable domain workspace validated here as **isolated Kotlin/JVM PoC**, not product `commonMain` or UI adapter integration. Continue source clearance and product baseline before any Compose rewrite.

## Next P0

Authorized networked Codex/host **one real non-shallow PUBLIC clone or a justified manual-only workflow**; capture run ID/event SHA/HEAD/origin/main/remote SHA, strict fsck and clean before/after, exit codes and SHA log. Then full PUBLIC tooling regressions, controlled rights-cleared migration, byte-exact vs reconstructed/new ledger, public reconstruction checksum reconciliation, strict resolved Gradle graph/SPDX/SBOM/NOTICE, product/platform/security/packaging/rollback gates.

Every PUBLIC commit `[skip ci]`, no force push, PRIVATE READ-ONLY. **PRODUCTION NOT FINAL.**
