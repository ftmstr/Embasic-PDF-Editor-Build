# V1081 — Historical Gradle verification coverage versus partial runtime license evidence

Date: 2026-10-28 ~16:00 TRT. **PRODUCTION NOT FINAL.**

## Canonical boundary
- Sole writable repository: PUBLIC `ftmstr/Embasic-PDF-Editor-Build`; initial HEAD `ed32509e64b933603fb22636e1aa255fd9977d86`, STATUS V1080.
- Historical PRIVATE `ftmstr/uygulama-baslangic-sablonu` was queried **READ-ONLY** at exact commit `e4e4b4f6ccd9d838b5ac5434b45fb8202d4ba786`. No PRIVATE commit, push, PR, Actions, deletion, or source migration.
- This is a **metadata-only audit of historical build supply-chain declarations**. It is not proof of Gradle resolution, artifact download, license clearance, SBOM completeness, or PUBLIC build success.

## Reproduced historical metadata observations
GitHub GET returned these exact historical files:
- `projects/embasic-pdf-editor/product/gradle/verification-metadata.xml`, Git blob `d1fc2d9380bc538207dec3c779daf1466fd9c464`, 163,902 UTF-8 bytes. Parsed **357 distinct component coordinates**, **625 artifact entries**, **625 syntactically valid 64-hex SHA-256 values**, **0 duplicate component coordinates**. `verify-metadata=true`, `verify-signatures=false`. **A syntactically populated checksum list does not prove that any artifacts were resolved and verified in this PUBLIC repository.**
- `KNOWN_RUNTIME_LICENSES.json`, Git blob `633c0e0354a1086999549280f0e37ca81ccc6940`, explicitly `PARTIAL_KNOWN_RUNTIME_ONLY`: **6** named runtime coordinates, all listed as Apache-2.0. All six coordinates appear among the historical 357 verification components. This is **not** a 6/357 runtime-coverage ratio because the 357 include build/plugin/test/other artifacts, not an independently resolved runtime-only graph.
- `KNOWN_RUNTIME_SBOM.spdx.json`, Git blob `821494261c90b492b8643cfa2a1f0496c78183bc`, SPDX 2.3, **6 packages** with distinct SPDX IDs; explicitly partial. `THIRD_PARTY_NOTICES.partial.md`, Git blob `60263296a961d9ba397927c8fce15ee0f6613c6a`, explicitly `NOT DISTRIBUTION-FINAL`.
- Three historical product Gradle files declare runtime dependencies `org.apache.pdfbox:pdfbox:3.0.8`, `org.jetbrains.kotlinx:kotlinx-coroutines-core:1.11.0`, `org.jetbrains.kotlinx:kotlinx-coroutines-android:1.11.0`. PDFBox-related transitive anchors in partial inventory do not establish the resolved graph. Historical Gradle file content is not migrated.
- The historical full Git tree GET (`truncated=false`, 1,942 entries) did not show a conventional top-level LICENSE/COPYING file for this product. **Absence of a conventional file does not establish ownership or lack of rights; publication permission remains unverified.**

## Engineering conclusion and P0 decision
A large historical `verification-metadata.xml` is present and structurally populated. The immediate blocker is **not** absence of a hash list; it is absence of a trusted PUBLIC product checkout and **actual strict Gradle resolution/verification evidence**, plus a **complete resolved runtime license/SBOM/NOTICE graph**. Do not regenerate or blindly copy historical metadata, do not assert the 357 components were downloaded, and do not use the six-package partial SBOM as production coverage.

Codex next steps on authorized trusted host, only after complete rights-cleared source migration:
1. `git clone --no-tags --no-single-branch --branch main https://github.com/ftmstr/Embasic-PDF-Editor-Build.git`; verify `HEAD`, `origin/main`, `git fsck --full --strict --no-reflogs`, clean index and `--is-shallow-repository=false`. Capture SHA/exit/log. Manual-only workflow can be dispatched once if authorized; current GitHub Actions GET returned **0 runs**.
2. Revalidate historical starter/policy and recovery/reconstruction checksums on approved bytes; keep byte-exact recovery separate from reconstructed/new. Source admission **35/35 BLOCKED** until legal/secret/privacy/provenance clearance and complete product/recovered source-set closure.
3. Inspect actual `./gradlew tasks --all` and choose real tasks; run `./gradlew --dependency-verification strict <actual build/test tasks>`. Record full resolved compile/runtime/test/plugin graphs, artifact hashes, complete SPDX license sources, SBOM and THIRD_PARTY_NOTICES; block unknown/transitive license. Historical metadata must be compared against the new accepted graph, not assumed authoritative.
4. Real product Build/Unit/Integration/Android/Windows/Ubuntu/Security/Packaging/Signing-Rollback acceptance with exit codes, artifacts and logs.

## P0 test/evidence classification
- Historical metadata structural check: **PASS_METADATA_ONLY** (357 distinct coordinates, 625/625 syntactically valid SHA-256 entries, 6/6 known partial runtime coordinates present). This was executed on GitHub GET UTF-8 historical contents with deterministic extraction; no Gradle or dependency downloads occurred.
- Real `git ls-remote` in this host: **FAIL** DNS, exit 128.
- Trusted PUBLIC full checkout: **NOT RUN**.
- Production Build / Unit / Integration / Android / Windows / Ubuntu / Security / Dependency Verification / License-SBOM-NOTICE / Packaging / Signing-Rollback: **all NOT RUN**; **0/11 PASS**.
- PUBLIC reconstruction checksum convergence: **NOT RUN**.
- No PRIVATE source bytes, third-party GPL code or confidential data were published.

## Architecture and clean-room
ADR-005 immutable workspace remains an independent Kotlin PoC; production `commonMain` integration **NOT RUN**. PDF Arranger GPL-3.0 source/modules/implementation are forbidden; desktop Apache PDFBox structural backend and Android PdfRenderer viewer remain baselines. Poppler/pikepdf not introduced; no Android structural engine chosen.

Every PUBLIC write uses `[skip ci]`, no force push. Actions blackout ended 2026-10-05 00:00 TRT, but unnecessary runs are prohibited. **PRODUCTION NOT FINAL.**
