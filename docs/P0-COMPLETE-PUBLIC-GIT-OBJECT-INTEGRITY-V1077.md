# V1077 — Complete PUBLIC Git object-content integrity via API (NOT a trusted checkout)

**2026-10-28 ~12:00 TRT | PRODUCTION NOT FINAL**

## Authority and scope

- Canonical PUBLIC `ftmstr/Embasic-PDF-Editor-Build` `main` before this report: `a663bbd8020dc8f5e5ed23cbc7808c0b4c947ded` (V1076).
- Git commit's **tree SHA**: `9d24e1a11c19a435c93ecd0bc6208db4cfc70b47`. The GitHub `git/trees/main` response labels its top-level `sha` as the commit SHA; the authoritative tree SHA was read from the Git commit object. This distinction was independently checked.
- Recursive Git tree response: **`truncated=false`**, 47 entries: **27 blob objects**, **20 nested tree objects**. No gitlinks. Total tracked blob bytes reported: **213,068**.
- GitHub Actions GET: **0 runs**. No dispatch, no force push. PRIVATE `ftmstr/uygulama-baslangic-sablonu` was **not written to**; PRIVATE recovery history is not PUBLIC product test evidence.

## New substantive P0 integrity evidence

All **27 current PUBLIC blob contents** were fetched separately from the GitHub connector, UTF-8 content encoded into bytes, and each `SHA1("blob <length>\\0" + content)` and byte length was independently compared with the Git tree's recorded blob SHA and size. **27/27 PASS, zero mismatches**. SHA-1 is used here as the existing Git object-identity format, **not** as a substitute for SHA-256 supply-chain assurance.

Using the recursive PUBLIC Git tree metadata, all **20 nested Git tree objects plus the root** were independently serialized and checked using local `git hash-object -t tree --stdin`. **21/21 PASS**, root `9d24e1a11c19a435c93ecd0bc6208db4cfc70b47`, matching the commit object's tree SHA.

Ten PUBLIC code/test/workflow files extracted from earlier PUBLIC evidence archives were separately revalidated using local `git hash-object`: **10/10 PASS**. This is a **scope-limited source extraction**, not a complete local checkout.

**Important:** These API object checks establish the complete current PUBLIC *tracked-content object identity* at this snapshot. They do **not** establish a non-shallow clone, full Git history, `git fsck`, trusted Gradle checkout, or product build/release readiness. The GitHub-hosted manual workflow remains **NOT RUN**, and direct `git ls-remote` still **FAILS** due to DNS (exit 128).

## Actually executed regression and prototype tests

- Re-executed the ten Git-blob-matched PUBLIC-scoped Python tools/tests: `PYTHONPATH=tools python -m unittest discover -s tests -p 'test_*.py' -v`: **42/42 PASS**, exit 0.
- Independently compiled the PUBLIC Git-blob-matched Kotlin workspace prototype with `kotlinc` and executed `java -jar`: **45/45 PASS**, compiler/runtime exit 0. This is a standalone PoC, **not** a product KMP/Gradle build.
- PowerShell dashboard Python static/data contract suite: initial V1077 JSON failed **1/12** because a new scoped-test description used lowercase `not` instead of contract-required `NOT`. Corrected only the dashboard JSON; rerun **12/12 PASS**, exit 0. PowerShell 5.1/7 actual runtime **NOT RUN**.
- Git tree metadata recomputation using local `git hash-object -t tree`: **21/21 PASS**, exit 0.
- Python `py_compile` for scoped PUBLIC tooling: PASS.
- No PRIVATE source/asset/manifest bytes migrated.

## Reproducible evidence artifact

Evidence package: `V1077_PUBLIC_Tracked_Object_Integrity_Evidence.zip`, SHA-256
`0f6926d2e78b5c024a2b3e72b1abce330eea779d0f98b2a7ad3f3bdddd18a113`.

The ZIP contains the PUBLIC-scoped source/test extract, Git metadata and local independent tree-verification script, actual Python/Kotlin/dashboard logs, PowerShell read-only dashboard, per-file SHA-256 inventory and a scope-limitation README. ZIP CRC PASS; **no PRIVATE source bytes, credentials, proprietary assets, or bundled Kotlin runtime JAR**. The package is a supplemental local artifact, **not a canonical PUBLIC Git commit or verified Drive backup**.

## Release gates (production)

| Gate | Status |
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

**0/11 production gates PASS; production gate pass coverage 0%.** The 27/27 API blob integrity, 21/21 tree integrity, 42/42 Python tests and 45/45 isolated Kotlin smoke are **not** product release gates. Historical PRIVATE 41/41 SHA-256, starter 142/142 and policy 17/17 must not be promoted to PUBLIC acceptance.

## Clean-room and ADR-005

- PDF Arranger GPL-3.0 source, implementation and runtime dependencies were **not copied or introduced**. Only independent clean-room architectural behavior remains admissible.
- Desktop Apache PDFBox structural backend and Android PdfRenderer viewer baseline remain unchanged. No Poppler/pikepdf; no premature QPDF/PdfBox-Android engine decision.
- ADR-005 immutable `EditorDocumentState`, `SourceDocumentRef`, `EditorPageRef`, `SelectionState`, `EditorAction`, `EditorExportPlan`, bounded `EditorHistory` remain a **standalone Kotlin PoC**, not production `commonMain` Gradle integration.

## P0 next action — do not extend verifier hardening indefinitely

1. Obtain a **real authorized complete PUBLIC clone** (or dispatch the already-prepared manual-only GitHub Actions workflow once); collect exact `GITHUB_SHA`, HEAD, origin/main, non-shallow flag, clean status, `git fsck`, scoped test logs and exit codes. GitHub Actions blackout ended 2026-10-05 00:00 TRT; unnecessary runs remain prohibited.
2. Rights/secret/license/privacy-screen the historical dual-source graph and Android service/manifest collision. Do not copy PRIVATE source into PUBLIC without explicit per-file provenance and approval. Preserve byte-exact vs reconstructed/new distinction.
3. After trusted checkout and screened migration, execute V477–latest verifiers, PUBLIC reconstruction checksum convergence, strict resolved Gradle dependency/license/SBOM/NOTICE, actual build/unit/integration/platform/packaging/signing/rollback gates.
4. Only then integrate ADR-005 `commonMain` domain and Swing/Android adapters; Compose rewrite later.

**All GitHub writes: PUBLIC only, `[skip ci]`, no force push. PRODUCTION NOT FINAL.**
