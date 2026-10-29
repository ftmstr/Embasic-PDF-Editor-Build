# V1106 — Authoritative user-upload starter/policy checksum recheck (NOT product acceptance)

Date: 2026-10-29 16:49 TRT. **PRODUCTION NOT FINAL.**

## Canonical source and priority

- Initial authoritative PUBLIC main: `4a6685daf92ecee18a85cdd8f73b968eaed06810` (STATUS V1105), not older V1075. The PRIVATE historical repo is **READ-ONLY**, never a commit/push/PR/Actions target.
- PUBLIC GitHub Actions GET reported **0 runs**. `git ls-remote https://github.com/ftmstr/Embasic-PDF-Editor-Build.git` still **FAIL** due to local DNS `Could not resolve host: github.com`, exit 128. Real trusted complete PUBLIC checkout **NOT RUN**. No workflow was dispatched in this turn; the GitHub connector has GET workflows but no authorized dispatch action.
- The current PUBLIC tree contains isolated Python tooling, Kotlin/JVM prototype and docs, **not** a migrated root `gradlew`/full Gradle product. Do not claim actual product Gradle Build or platform tests.

## Executed byte-level authority verification

The test input consisted **only of user-supplied local uploads**, and was not downloaded from PUBLIC GitHub:

1. `Uygulama_Baslangic_Sablonu_v1.3.1(4).zip`, independently computed archive SHA-256 `ff50a26027b1d3d8e34d846d1bfcb0ffe96929875a70ce72c1eb97b1177fb4f1`. Zip has 143 file members: one internal UTF-8 checksum manifest plus **142 files**. Used `ZipFile.read` directly, no file extraction, and verified precise member set and 142 per-file SHA-256 values: **142/142 MATCH**, 0 mismatches.
2. `FILE_MANIFEST_SHA256(1).txt` and 17 uploaded policy Markdown documents (upload copy suffixes normalized only in the in-memory filename comparison): **17/17 SHA-256 MATCH**, 0 mismatches. No policy text or secrets published to GitHub.
3. Independently authored stdlib Python negative fixtures for duplicate, malformed, traversal, absolute path, invalid UTF-8, corrupted hash and extra archive member. **9/9 synthetic regression tests PASS**. These are verification-tool tests, **NOT** the PUBLIC product Security/Unit gates.
4. Refreshed read-only color PowerShell release dashboard from the V1074 local artifact, with V1105 last-reported scoped tests **59/59 Python** and **46/46 Kotlin**, marked **not re-executed in this turn**. Dashboard locally executed **14/14 Python static/data contract tests PASS**; Windows PowerShell 5.1/PowerShell 7 executable unavailable here, so actual PowerShell runtime **NOT RUN**. Snapshot percentage is **0/11 = 0% proven production release gates**, NOT overall project completion. Conditional scenario remains **12–24 weeks after all prerequisites are ready**; without checkout, source clearance, and platform labs, no defensible fixed FINAL date.

## Strict scope limitations

**The 142/142 and 17/17 successes concern the uploaded starter/policy artifacts, not the PUBLIC repo's accepted source migration or the 41-file historical PRIVATE reconstruction.** They do not authenticate the full Git history, authorize publication of recovered source, verify current dependency versions/licensing, or establish a production release.

Historical 51 Kotlin source candidates remain **BLOCKED** for source rights, PII/privacy, secret, assets, SPDX/transitive licensing and provenance. Treat byte-exact recovery and reconstructed/new implementations separately, do not silently rebaseline mismatched checksums.

## Release gates (all NOT RUN)

Build; Unit; Integration; Android; Windows; Ubuntu; Security; Dependency Verification; License/SBOM/NOTICE; Packaging; Signing/Rollback: **0/11 PASS**. PUBLIC reconstruction: **NOT RUN**. V477–latest full verifier regressions on a trusted PUBLIC checkout: **NOT RUN**.

## Clean-room and architectural limits

PDF Arranger GPL-3.0 source/modules/implementation/runtime dependency **never copied**. Desktop Apache PDFBox structural and Android PdfRenderer viewer baselines unchanged; Poppler/pikepdf not admitted. Android structural engine needs separate ADR + license/transitive/ABI/package/performance/malformed/stress PoC. ADR-005 immutable Kotlin common editor workspace is an isolated prototype, **not** Gradle product `commonMain` integration.

## P0 next

Obtain authorized actual full non-shallow PUBLIC clone (or one deliberately dispatched manual-only hosted workflow), collect run ID/event SHA/HEAD/origin/main/fsck clean pre/post evidence; run V477–latest regressions on canonical source. Then rights-cleared product/recovered-source two-surface migration and checksum convergence, strict resolved dependency/license/SBOM/NOTICE verification, genuine Android/Windows/Ubuntu runtime and packaging/signing/rollback.

All PUBLIC writes use `[skip ci]`; no force push; no PRIVATE writes or unnecessary Actions. **PRODUCTION NOT FINAL.**
