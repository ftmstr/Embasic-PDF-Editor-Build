#!/usr/bin/env bash
# Embasic PDF Editor - one-shot PUBLIC checkout and scoped evidence runner.
# No pushes, workflows, PRIVATE access, Gradle release claims, or source migration.
set -Eeuo pipefail
umask 077
PUBLIC_REPO='ftmstr/Embasic-PDF-Editor-Build'
PUBLIC_URL='https://github.com/ftmstr/Embasic-PDF-Editor-Build.git'
if [[ $# -ne 2 || "$1" != '--output' ]]; then
    printf 'Usage: %s --output /new/empty/evidence-directory\n' "$0" >&2
    exit 64
fi
OUT="$2"
if [[ "$OUT" != /* || -e "$OUT" || -L "$OUT" ]]; then
    echo 'Output must be a new absolute path, not an existing file/symlink.' >&2
    exit 64
fi
if [[ ! -d "$(dirname "$OUT")" ]]; then
    echo 'Parent directory must already exist.' >&2
    exit 64
fi
mkdir -m 700 -- "$OUT"
LOG="$OUT/runner.log"
: > "$LOG"
exec 3>&1 4>&2
exec >"$LOG" 2>&1
STAGE='START'
HEAD_SHA=''
REMOTE_SHA=''
VERIFIER='NOT RUN'
KOTLIN='NOT RUN'
STARTED="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
complete() {
    local status="$?"
    trap - EXIT
    set +e
    export RUN_OUT="$OUT" RUN_STATUS="$status" RUN_STAGE="$STAGE" RUN_HEAD="$HEAD_SHA" RUN_REMOTE="$REMOTE_SHA" RUN_VERIFIER="$VERIFIER" RUN_KOTLIN="$KOTLIN" RUN_STARTED="$STARTED" RUN_REPO="$PUBLIC_REPO"
    python3 - <<'PY'
import datetime, hashlib, json, os
from pathlib import Path
root=Path(os.environ['RUN_OUT'])
log=root/'runner.log'
result={
 'scope':'canonical PUBLIC checkout + scoped tooling/Poc tests; NOT product release qualification',
 'repository':os.environ['RUN_REPO'],
 'started_utc':os.environ['RUN_STARTED'],
 'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'exit_code':int(os.environ['RUN_STATUS']),
 'status':'PASS' if os.environ['RUN_STATUS']=='0' else 'FAIL',
 'failed_or_completed_stage':os.environ['RUN_STAGE'],
 'head':os.environ['RUN_HEAD'] or None,
 'remote_main':os.environ['RUN_REMOTE'] or None,
 'public_tooling_tests':os.environ['RUN_VERIFIER'],
 'isolated_kotlin_smoke':os.environ['RUN_KOTLIN'],
 'production_release_gates':'NOT RUN',
 'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest(),
}
(root/'checkout-evidence.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf-8')
PY
    sha256sum "$LOG" "$OUT/checkout-evidence.json" > "$OUT/SHA256SUMS.txt"
    cat "$LOG" >&3
    printf '\nEvidence: %s/checkout-evidence.json  Exit: %s\n' "$OUT" "$status" >&3
    exit "$status"
}
trap complete EXIT
printf 'PUBLIC_ONLY=%s\nSTARTED=%s\n' "$PUBLIC_REPO" "$STARTED"
export GIT_TERMINAL_PROMPT=0 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_LFS_SKIP_SMUDGE=1
STAGE='PREREQUISITES'
command -v git
command -v python3
git --version
python3 --version
uname -srm
STAGE='CLONE'
git -c protocol.file.allow=never clone --no-tags --no-single-branch --branch main -- "$PUBLIC_URL" "$OUT/public-checkout"
cd "$OUT/public-checkout"
STAGE='CHECKOUT_VERIFY'
[[ "$(git remote get-url origin)" == "$PUBLIC_URL" ]]
[[ "$(git branch --show-current)" == 'main' ]]
[[ "$(git rev-parse --is-shallow-repository)" == 'false' ]]
[[ -z "$(git status --porcelain=v1 --untracked-files=all)" ]]
HEAD_SHA="$(git rev-parse --verify HEAD^{commit})"
[[ "$HEAD_SHA" =~ ^[0-9a-f]{40}$ ]]
[[ "$HEAD_SHA" == "$(git rev-parse refs/remotes/origin/main)" ]]
REMOTE_SHA="$(git ls-remote --exit-code origin refs/heads/main | cut -f1)"
[[ "$HEAD_SHA" == "$REMOTE_SHA" ]]
if [[ -n "${EMBASIC_EXPECTED_PUBLIC_SHA:-}" && "$HEAD_SHA" != "$EMBASIC_EXPECTED_PUBLIC_SHA" ]]; then
    printf 'Expected PUBLIC HEAD drift: %s != %s\n' "$HEAD_SHA" "$EMBASIC_EXPECTED_PUBLIC_SHA"
    exit 65
fi
if git ls-files --stage | grep -q '^160000 '; then
    echo 'Unexpected gitlink: blocked' >&2
    exit 65
fi
git fsck --full --strict --no-reflogs
[[ -f docs/STATUS.md ]]
grep -q 'PRODUCTION NOT FINAL' docs/STATUS.md
STAGE='PYTHON_TOOLING'
export PYTHONPATH="$PWD/tools"
export PYTHONPYCACHEPREFIX="$OUT/python-cache"
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 -m compileall -q tools tests
VERIFIER='PASS (see actual test counts in log; not product Unit)'
STAGE='KOTLIN_POC'
SOURCE='prototypes/common-editor-workspace/src/commonMain/kotlin/org/embasic/pdfeditor/workspace/EditorWorkspace.kt'
TESTS='prototypes/common-editor-workspace/src/commonTest/kotlin/org/embasic/pdfeditor/workspace/EditorWorkspaceSmoke.kt'
if command -v kotlinc >/dev/null 2>&1 && command -v java >/dev/null 2>&1; then
    kotlinc -J-Xmx512m "$SOURCE" "$TESTS" -include-runtime -d "$OUT/editor-workspace-smoke.jar"
    java -Xmx512m -jar "$OUT/editor-workspace-smoke.jar"
    KOTLIN='PASS (isolated Kotlin/JVM PoC; not Gradle/KMP)'
else
    KOTLIN='NOT RUN (kotlinc/java unavailable)'
fi
STAGE='POST_TEST_CLEAN'
[[ -z "$(git status --porcelain=v1 --untracked-files=all)" ]]
git fsck --full --strict --no-reflogs
printf 'PUBLIC_HEAD=%s\nREMOTE_MAIN=%s\nSCOPED_TESTS=%s\nPRODUCT_GATES=NOT RUN\nPRODUCTION NOT FINAL\n' "$HEAD_SHA" "$REMOTE_SHA" "$VERIFIER"
STAGE='SUCCESS_SCOPED_ONLY'
