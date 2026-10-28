# V1074 — Evidence-scoped PUBLIC PowerShell progress dashboard

Date: 2026-10-28 09:14 TRT. **PRODUCTION NOT FINAL.**

## Canonical authority and intake

- PUBLIC writing target: `ftmstr/Embasic-PDF-Editor-Build`; V1074 initial HEAD `fd77404577b30501019925bf3ce585a9ae47c643`, STATUS V1073 at this check. All changes on main only with `[skip ci]`; no force push.
- PRIVATE `ftmstr/uygulama-baslangic-sablonu` remains strictly **READ-ONLY**, and its historical PASS results are not PUBLIC product PASS.
- GitHub Actions read-only GET: zero runs. The manual checkout workflow is prepared but has **not** been dispatched.
- Executable container Git probe: `git ls-remote ...` -> **FAIL**, DNS `Could not resolve host: github.com`, exit 128. Therefore trusted complete PUBLIC checkout is **NOT RUN**.

## Actually executed engineering tests

Rather than extending the verifier again, the V1074 effort revalidated the PUBLIC Git blob identities for eight specific files using the GitHub tree, previously uploaded evidence ZIPs, and local `git hash-object --stdin`. All **8/8 exact Git blob SHA** comparisons matched current PUBLIC HEAD; the recovered files are a limited local extract, **not** a full Git checkout.

- PUBLIC-scoped `unittest discover`: initial environment configuration **FAIL** due to missing `PYTHONPATH`. After setting `PYTHONPATH` to the local `tools` directory, **31/31 PASS**, exit 0. 10 local Git-checkout tests, 14 migration-preflight tests, 7 manual-workflow policy tests. This is **not** product Unit or Security acceptance.
- Kotlin `kotlinc` compilation exit 0; standalone workspace smoke **45/45 PASS** exit 0 on the eight-Git-blob-matched snapshot. **Not** product Gradle/KMP acceptance.
- New PowerShell dashboard independent Python data/contract tests **12/12 PASS** exit 0. Windows PowerShell 5.1 / PowerShell 7 runtime **NOT RUN** (not installed on this host); do not mark it as a runtime PASS.
- `py_compile` for the two PUBLIC tooling sources: PASS.

## PowerShell dashboard and evidence provenance

The prepared script `Embasic-PDF-Progress.ps1`, companion `release-gates.json`, static tests, scope-limited public source extract, logs, provenance hashes and usage README are stored as a ZIP in the project's authorized Google Drive folder:

https://drive.google.com/file/d/1a9tQtu28vhfuzSm9epxYZPumli-vj1u7/view

Package SHA-256: `aa655378904871313440c1cdf2cca80f72a393fe91938ed928ea239e256a7632`.

The script is read-only and performs an optional **GET-only** PUBLIC HEAD check. It refuses noncanonical repositories, malformed gate lists, invalid statuses, or an estimate not labeled `SCENARIO_ONLY_NOT_COMMITMENT`. On a newer remote main it marks the snapshot **STALE** rather than promoting any PASS result. Only actually verified production gates contribute to the displayed percent. The artifact ZIP is delivered in Drive; **its files are not asserted to be published as GitHub source files**.

## Measured progress and ETA

- Eleven production release gates: **0/11 PASS = 0% verified release-gate coverage**. This metric does not indicate 0% engineering work completed; overall engineering percent is not evidentially measurable from the existing logs.
- Production gates: Build, Unit, Integration, Android, Windows, Ubuntu, Security, Dependency Verification, License/SBOM/NOTICE, Packaging, Signing/Rollback: all **NOT RUN**. PUBLIC reconstruction **NOT RUN**.
- Conditional planning **scenario only**: **12–24 weeks after** trusted full checkout, source rights/secret clearance, and actual cross-platform test environments are ready. If all these prerequisites hypothetically held on 2026-10-28, calendar range would be **2027-01-20 to 2027-04-14**. They do **not** hold now. Consequently there is **no committed defensible FINAL date**. The estimate is not based on observed release-gate execution velocity.

## Priority and architecture

P0: trusted complete PUBLIC checkout, V477-to-latest verifier regressions, secret/license/provenance-gated source migration with byte-exact versus reconstructed/new provenance separation, PUBLIC reconstruction checksum convergence, strict resolved Gradle verification and License/SBOM/NOTICE, real desktop/Android/Ubuntu build/runtime/security/installer/signing/rollback gates. The prepared manual GitHub-hosted checkout should be run only in an authorized environment, collecting run/event SHA/fsck/exit logs.

ADR-005 shared immutable Kotlin workspace remains a standalone PoC; no product commonMain integration. No GPL-3.0 PDF Arranger source copied; PDFBox remains desktop structural baseline, Android PdfRenderer viewer baseline; no Poppler/pikepdf, no Android structural engine selection without PoC/ADR/license/ABI/stress proof.

**PRODUCTION NOT FINAL.** Historical private recovery 41/41 SHA evidence is not PUBLIC reconstruction PASS.
