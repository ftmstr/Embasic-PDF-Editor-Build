# V1127 — Checkout cleanliness status-producer fail-open: test-first correction

**2026-11-19 ~20:xx Europe/Istanbul · PUBLIC ONLY · PRODUCTION NOT FINAL.**

## Canonical source and real trusted checkout first

- Verified canonical PUBLIC `ftmstr/Embasic-PDF-Editor-Build` `main`, starting HEAD `8752d4ced0dfce17bcaab3b8ca6e8f7fe562b6bb` (V1126); `docs/STATUS.md`, complete 99-entry tree, GitHub Actions **0 runs** and both native Drive V1126 Rapor/Codex read-back. Historical PRIVATE `ftmstr/uygulama-baslangic-sablonu` **STRICT READ-ONLY**.
- Actual `git ls-remote --exit-code` against exact canonical PUBLIC HTTPS **FAIL exit128**; separate real `git clone --no-tags --no-single-branch --branch main` **FAIL exit128** on DNS `github.com`. Logs SHA256 respectively `137c4578bf8e71fd67eb06ef89ac907a19bffabaf9eedd374c1b717d550f41e2` and `ab246d6e077612983ce3bc851acf866b36ed9c55addcb4af65537b19417672e9`; no `.git` checkout. GitHub connector only supports existing-job reruns, not creating a new manual `workflow_dispatch` and existing run count remains zero. **No hosted run started**.
- Therefore actual full trusted non-shallow clone, `git fsck`, exact remote/HEAD/origin/main/event SHA, clean pre/post clone, V477–latest public full regression chain and actual `Gradle` build/task discovery **NOT RUN**. GitHub contents API hashes are not a real checkout.

## Concrete defect in two PUBLIC trusted-checkout launchers

The V1125 manual-only `.github/workflows/p0-trusted-public-checkout.yml` and standalone `tools/p0_public_checkout_once.sh` both executed a clean-tree gate through shell command substitution inside `test -z "$(git status --porcelain=v1 --untracked-files=all)"` or `[[ -z "$(git status ...)" ]]`. When `git status` itself fails and prints no stdout, the outer string test succeeds despite the producer error. This creates a **false clean-tree classification**, both before and after test execution. The previously fixed V1125 index-producer check remains untouched.

- New original `tests/test_v1127_checkout_status_failclosed.py` first run against exact prior PUBLIC workflow blob `e4257c3c2bedc2ac2255a3e4b4d145b1da17c23a` and standalone runner blob `a08e32fe899d978e8b57ee5c3804dd6d4104486c`: **RED: 8 test methods, 12 assertion failures, exit1**.
- Minimum code fix: in both launchers, before and after tests, run the producer as a **standalone command** and capture its entire output outside the checkout, then require the output file to be empty:
```bash
git status --porcelain=v1 --untracked-files=all > "$ROOT/status-pre.txt"
test ! -s "$ROOT/status-pre.txt"
```
For standalone runner, use `$OUT/status-pre.txt` and `[[ ! -s ... ]]`; repeated for `status-post.txt`. Existing `set -Eeuo pipefail` now aborts on a producer error *before* any empty-tree decision. No source migration, secrets, remote writes, CI triggers, third-party dependencies or user data were added.
- **GREEN: 8/8 new independent local Python tests PASS exit0**, including two sources/two locations, clean/dirty, zero-output and partial-output failing producer. Extracted hosted workflow Bash script `bash -n` PASS; standalone Bash `bash -n` PASS.
- Relevant existing tests rerun because both launchers changed: manual workflow policy **9/9 PASS**, previous V1125 Git index regression **7/7 PASS**, standalone runner contract **11/11 PASS**, all local. Total **35/35 scoped local tests PASS**, not product Unit/Security/Integration. V1126 8+34+14 tests **not rerun**.
- Exact PUBLIC source Git blob readback **3/3 match local tested bytes**:
  - workflow `bf13702c804463cc56a1a503b1a2f30a162fc952` SHA256 `14565357a0395c1a2f84f42b2d3440546edb92cfd31ebcd8f7e0e1c0976c8f08`;
  - runner `6478cd04821a1d70b1442db69567b16082a8bf56` SHA256 `a3a993a9055d250d2e62a68fab46833841988ea5a38d4bafa3abc32f4bcd740b`;
  - new regression test `e2845505b0556be307be6692ea12cba6b8111347` SHA256 `9ae23e46e7635a8538d7a4a84f3dc0ffd701d8058dbe47067f77c18d5c8b49e1`.
- Test file upload bridge initially altered quote/question-mark bytes, detected by blob mismatch and corrected in separate **`[skip ci]` commits**; **only final exact matching bytes** are counted as published test source. No additional test PASS was claimed for encoding repair.

## Explicit unresolved release gates

This only hardens PUBLIC checkout verification; **neither launcher has completed a real GitHub-hosted/full checkout**. The host lacks `gradle`, `adb`, `sdkmanager`, `aapt2`, `apksigner`, `pwsh` and native Windows access. Real Android/Windows/Ubuntu product builds and runtime tests are **NOT RUN**.

- ADR-006 product Gradle/KMP/AGP toolchain **PROPOSED**; no rights-cleared product wrapper, task/variant, resolved graphs or device test run.
- ADR-007 JUnit 4 `junit:junit:4.13.2` **EPL-1.0 BLOCKED_TEST_ONLY_EXCEPTION_REVIEW**. Production APK and test APK distinct physical/source graph/hash/SPDX/SBOM/THIRD_PARTY_NOTICES and independently approved tool/signer pin acceptance **NOT RUN**. The V1121 platform-only synthetic PDF `PdfRenderer` instrumentation remains **UNBUILT / device NOT RUN**.
- Historical 51 Kotlin source candidates rights/ownership/PII/secrets/fonts/assets/transitive SPDX/provenance **BLOCKED**. PRIVATE STRICT READ-ONLY; no migrations. ADR-005 isolated Kotlin PoC only. Desktop PDFBox structural / Android PdfRenderer viewer baseline unchanged; PDF Arranger GPL-3.0 implementation and Poppler/pikepdf excluded.
- **All 11 production gates NOT RUN (0/11 PASS)**: Build, Unit, Integration, Android, Windows, Ubuntu, Security, Dependency Verification, License/SBOM/NOTICE, Packaging, Signing/Rollback. PUBLIC Reconstruction **NOT RUN**. 0% means *verified production release gates*, **not development completion**.

## Next authorized P0 and conditional scenario

Obtain a **real** trusted non-shallow PUBLIC clone, or one justified manual-only hosted workflow run on a networked authorized host, and capture exact event SHA/origin/main/remote/HEAD, `git fsck --full --strict --no-reflogs`, clean pre/post plus actual status-producer command exits, log/artifact SHA. Then source rights clearance, ADR-006/007 decisions, exact Gradle tasks and strict resolved production/test APK transitive SPDX/NOTICE/SBOM, actual independent signer/SDK pins and nonempty `PdfRenderer` emulator/device tests, full V477–latest and actual three-platform install/upgrade/uninstall/security/signing/rollback.

Conditional planning **12–24 weeks only AFTER** trusted full checkout, rights and all Android/Windows/Ubuntu test laboratories are ready. If hypothetically ready 2026-11-19, range **2027-02-11 to 2027-05-06**; prerequisites are not ready and no committed FINAL date exists.

All PUBLIC commits **`[skip ci]`**, no force push, no unnecessary Actions. PRIVATE **STRICT READ-ONLY**. **PRODUCTION NOT FINAL**.
