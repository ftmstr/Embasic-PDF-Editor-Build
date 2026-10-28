# V1069 — Historical reconstruction: nine manifest-origin hashes traced to earlier Git revisions

Date: 2026-10-28 ~05:00 TRT. **PRODUCTION NOT FINAL.**

## Canonical and scope
- Sole writable repository: `ftmstr/Embasic-PDF-Editor-Build` PUBLIC `main`. Starting verified HEAD: `a9852b40cea79e1cb860f56369de578528145a9c`.
- Former PRIVATE repository is **strictly READ-ONLY**. The paths, commit IDs and hashes below are historical provenance **metadata only**. No PRIVATE source, asset, binary, secret, user PDF, or third-party implementation was copied.
- Historical manifest: `projects/embasic-pdf-editor/product/RECONSTRUCTION_SHA256SUMS.txt`, blob `e6b9daf909207c35a33a3201438a60aa67a4310b`, manifest-writing commit `5ec86225eb9047324772ad2b2a1ae7b55a493e14`.
- Previous V1068 audit: at manifest-writing commit **32 MATCH / 9 MISMATCH**; later pinned PRIVATE snapshot **22 MATCH / 19 MISMATCH**. These are historical checks, not PUBLIC reconstruction convergence.

## New executed read-only provenance trace
For each of the **nine** mismatching-at-origin entries, inspected its PRIVATE Git commit history READ-ONLY, fetched an earlier committed file with the GitHub connector using `encoding=base64`, decoded the actual bytes, calculated SHA-256 without text normalization, and compared it to the original manifest hash. SHA-256 implementation self-tests: empty and `abc` **2/2 PASS**.

**Result: all 9/9 original manifest SHA-256 values match an identifiable *earlier committed file revision*.** The mismatch at the manifest-writing commit is therefore not evidence of untraceable/random hash values. It is consistent with a manifest retaining hashes from earlier revisions. It does **not** prove that the manifest represented one coherent Git tree or that any earlier version is the authorized product source.

| Manifest # | Historical relative path | Earlier Git commit (matching content) | Original manifest SHA-256 | Recomputed |
|---:|---|---|---|---|
| 4 | `DEPENDENCY_DECLARATIONS.md` | `655d99025fc12a7accf949db2c68e7bb92817589` | `17b303957685e4908e5347b0e0b06a8481530f4bb8271fee37f6a923ccecc67c` | MATCH |
| 22 | `shared/src/androidInstrumentedTest/kotlin/com/embasic/pdfeditor/reconstructed/AndroidFileTokenLedgerStoreInstrumentedTest.kt` | `7d8513f81c38f79fb5d68669f159087ebc168ff6` | `ae3b430e3da6deac543e1d8c23b87563e809c3322f0b13a38360bba88cb469aa` | MATCH |
| 26 | `shared/src/androidMain/kotlin/com/embasic/pdfeditor/reconstructed/AndroidFileTokenLedgerStore.kt` | `7c5c7be23fd3248fac2d62d670ac8476d55a19c2` | `f88f6e3640f0dd4d9202572b566bf25f405c2b4156a3b5722267731fcdfcf850` | MATCH |
| 29 | `shared/src/commonMain/kotlin/com/embasic/pdfeditor/reconstructed/TokenLedger.kt` | `3d288001b92885db0a1735c9dd23aafe82ae4cbe` | `9a7f6d443feced72bee7ad6d7bdf76d03eb02bf1c3b1868e3b51683945976e44` | MATCH |
| 30 | `shared/src/commonMain/kotlin/com/embasic/pdfeditor/reconstructed/TokenLedgerStateCodec.kt` | `b6eb5b8357e78be391587369baaf7a6f081be605` | `5bde790dbfc57c304bf367815178ac01543c5d30d721da3c5a91ad25d0392530` | MATCH |
| 35 | `shared/src/commonTest/kotlin/com/embasic/pdfeditor/reconstructed/TokenLedgerStateCodecTest.kt` | `fbcfcb7e671df67b66b8c09e7d9b94ebf68cee3a` | `85e16f2002bf8fae50b8eb70e32e6795a5e43953ed8f4295df09b2e0e8ea5251` | MATCH |
| 36 | `shared/src/commonTest/kotlin/com/embasic/pdfeditor/reconstructed/TokenLedgerTest.kt` | `2646d26f6cd82cebac6cfcdc6676f6fc1d490af0` | `2ab7e002265de59cff1efa68e0605216ee21631b26cab9f823b595ea34d3deef` | MATCH |
| 37 | `shared/src/desktopMain/kotlin/com/embasic/pdfeditor/reconstructed/DesktopFileTokenLedgerStore.kt` | `2ba79a3563df1e01ad85a2c57669a638f24142ea` | `f63abe30ecde1b996d41216f34b0a0efb8983fbe57d498264bccc5e5976c6726` | MATCH |
| 39 | `shared/src/desktopTest/kotlin/com/embasic/pdfeditor/reconstructed/DesktopFileTokenLedgerStoreTest.kt` | `6e0e7a1404f919dc6592f53a1e60a51ca5cd0135` | `7635c3fcb1ba78884f1571d1ee042eed0f40c5f02c62498f0bc70fd5f9ab8169` | MATCH |

## Provenance interpretation and safety
- The manifest at its writing commit was already **not a valid hash snapshot of that commit** (9 mismatches). All nine original hashes have earlier committed byte matches; the historical record is **traceable but revision-inconsistent**.
- Do not silently replace the nine hashes with later values, restore earlier files into product, or assume any of these earlier revisions should ship. Distinguish (a) historical manifest hash, (b) exact earlier committed bytes, (c) manifest-writing commit bytes, (d) pinned later snapshot, and (e) future approved PUBLIC migrated bytes.
- Exact earlier file contents are **not published**. Commit/blob identities are provenance pointers only; license, ownership, PII, secrets, third-party asset review and human authorization remain required.
- No assertion of a single atomic earlier checkpoint: that requires checking all 41 entries against candidate Git tree(s), not merely locating one earlier revision per file.
- No PUBLIC starter/policy archive, recovery manifest, or full product Gradle checkout was validated. Historical starter 142/142 and policy 17/17 are not PUBLIC PASS.

## Actually executed scoped tests (this run)
- Nine raw-base64 historical SHA-256 comparisons: **9/9 MATCH**; two standard SHA-256 vectors: **2/2 PASS**.
- Local cross-check of nine indices against the V1068 41-entry JSON audit: **PASS** (metadata consistency only).
- Isolated Python checkout fixture tests **10/10 PASS**, migration preflight **14/14 PASS**, `py_compile` **PASS**.
- Isolated Kotlin/JVM editor PoC compile **PASS**, smoke **45/45 PASS**. These are **not** product Build/Unit/Integration/Security PASS.
- Actual executable `git ls-remote` PUBLIC: **FAIL** (DNS: `github.com` unresolved); trusted complete PUBLIC checkout **NOT RUN**. GitHub connector API reads are not a trusted full checkout.

## Product release gates
Build **NOT RUN**; Unit **NOT RUN**; Integration **NOT RUN**; Android **NOT RUN**; Windows **NOT RUN**; Ubuntu **NOT RUN**; Security **NOT RUN**; Dependency Verification **NOT RUN**; License/SBOM/NOTICE **NOT RUN**; Packaging **NOT RUN**; Signing/Rollback **NOT RUN**. **0/11 PASS**. PUBLIC Reconstruction **NOT RUN**.

## P0 next steps
1. Trusted full PUBLIC checkout on a Git-capable Codex/local host; capture `git fsck --full --strict`, non-shallow, clean HEAD/origin/main, remote URL, tool output.
2. With PRIVATE history READ-ONLY, evaluate whether **any single historical Git tree** satisfies the 41-entry manifest; if not, record per-entry mixed-revision provenance. Resolve the ten later divergences separately. Do not treat the nine earlier matches as source approval.
3. Human rights/privacy/license/secret review of product + recovered-source source graph (including Android source sets and manifest) before any allowlisted PUBLIC migration. Then V477–latest regressions, checksum convergence, strict dependency verification/resolved license/SBOM/NOTICE, real Gradle/platform gates.
4. ADR-005 immutable `commonMain` workspace remains an isolated Kotlin PoC pending real product baseline. PDF Arranger GPL-3.0 code/implementation/runtime dependency not used; desktop PDFBox structural and Android PdfRenderer viewer remain baselines; Poppler/pikepdf and unapproved Android structural engines remain excluded.

GitHub Actions blackout ended 2026-10-05 00:00 TRT; no Actions dispatched. PUBLIC commit messages require `[skip ci]`, no force push. PRIVATE READ-ONLY. **PRODUCTION NOT FINAL.**
