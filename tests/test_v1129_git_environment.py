"""P0 V1129: inherited Git variables must not disable verified HTTPS checkout.

Tests source-bound sanitized environment *construction*, not real remote TLS or
GitHub Actions. No PRIVATE repository, APKs, secrets or external connections.
"""
import ast
import os
from pathlib import Path
import re
import subprocess
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
DANGEROUS = {
    'GIT_SSL_NO_VERIFY': '1',
    'GIT_CONFIG_PARAMETERS': "'http.sslVerify=false'",
    'GIT_DIR': '/tmp/injected-directory',
    'GIT_WORK_TREE': '/tmp/injected-work-tree',
    'GIT_CONFIG_KEY_0': 'http.sslVerify',
    'GIT_CONFIG_VALUE_0': 'false',
    'GIT_CONFIG_COUNT': '1',
}
SHELL_SOURCES = (
    ROOT / 'tools/p0_public_checkout_once.sh',
    ROOT / '.github/workflows/p0-trusted-public-checkout.yml',
)


def actual_python_git_env():
    source = (ROOT / 'tools/p0_public_checkout.py').read_text('utf-8')
    fn = next(n for n in ast.parse(source).body
              if isinstance(n, ast.FunctionDef) and n.name == 'git_env')
    ns = {'os': os}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), '<canonical-git_env>', 'exec'), ns)
    return ns['git_env']


def bash_sanitizer(source: str) -> str:
    # Extract the canonical pre-clone environment reset, not a synthetic replacement.
    match = re.search(r'^\s*for git_key in "\$\{!GIT_@\}"; do\s*\n'
                      r'(?P<body>(?:.*\n){1,5}?)\s*done\s*\n'
                      r'(?P<export>\s*export GIT_TERMINAL_PROMPT=0[^\n]*)',
                      source, re.MULTILINE)
    if match is None:
        raise AssertionError('Missing pre-clone Git environment sanitizer')
    return 'for git_key in "${!GIT_@}"; do\n' + match['body'] + 'done\n' + match['export'].strip() + '\n'


class TrustedCheckoutEnvironment(unittest.TestCase):
    def test_python_drops_inherited_tls_override_and_config(self):
        with patch.dict(os.environ, DANGEROUS):
            clean = actual_python_git_env()()
        for key in DANGEROUS:
            if key == 'GIT_CONFIG_COUNT':
                self.assertEqual(clean[key], '0')
            else:
                self.assertFalse(key in clean, f'inherited Git setting survived: {key}')

    def test_python_retains_only_safe_explicit_git_settings(self):
        with patch.dict(os.environ, DANGEROUS):
            clean = actual_python_git_env()()
        self.assertEqual(clean['GIT_TERMINAL_PROMPT'], '0')
        self.assertEqual(clean['GIT_CONFIG_NOSYSTEM'], '1')
        self.assertEqual(clean['GIT_LFS_SKIP_SMUDGE'], '1')

    def test_both_bash_paths_remove_tls_override_before_git_clone(self):
        for path in SHELL_SOURCES:
            with self.subTest(source=path.name):
                source = path.read_text('utf-8')
                sanitizer = bash_sanitizer(source)
                # Actual variable reset is required before first git network invocation.
                self.assertLess(source.index('for git_key in "${!GIT_@}"'), source.index('git clone'))
                cmd = 'set -Eeuo pipefail\n' + sanitizer + '''
[[ -z ${GIT_SSL_NO_VERIFY+x} ]]
[[ -z ${GIT_CONFIG_PARAMETERS+x} ]]
[[ -z ${GIT_DIR+x} ]]
[[ -z ${GIT_WORK_TREE+x} ]]
[[ "$GIT_CONFIG_COUNT" == 0 ]]
[[ "$GIT_TERMINAL_PROMPT" == 0 ]]
'''
                env = dict(os.environ, **DANGEROUS)
                result = subprocess.run(['bash', '-c', cmd], env=env, capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_both_bash_paths_keep_public_source_fixed(self):
        for path in SHELL_SOURCES:
            with self.subTest(source=path.name):
                source = path.read_text('utf-8')
                self.assertIn('ftmstr/Embasic-PDF-Editor-Build', source)
                self.assertNotIn('GIT_SSL_NO_VERIFY=1', source)


if __name__ == '__main__':
    unittest.main()
