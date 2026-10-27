#!/usr/bin/env python3
"""One-shot, fail-closed PUBLIC repository checkout gate (not a release gate).

The PRIVATE historical repository is never a target. This tool executes no
repository code and does not make any remote GitHub writes.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Sequence
from urllib.parse import urlparse

PUBLIC_URL = "https://github.com/ftmstr/Embasic-PDF-Editor-Build.git"


class CheckoutFailure(RuntimeError):
    pass


def git_env() -> dict[str, str]:
    env = dict(os.environ)
    # Ignore user/system Git config, credential helpers, and local hooks.
    env.update({
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_LFS_SKIP_SMUDGE": "1",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_CONFIG_COUNT": "0",
    })
    for key in tuple(env):
        if key.startswith("GIT_CONFIG_KEY_") or key.startswith("GIT_CONFIG_VALUE_"):
            del env[key]
    return env


def run_git(args: Sequence[str], *, cwd: Path | None = None,
            local_fixture: bool = False, timeout: int = 120) -> str:
    protocol = "always" if local_fixture else "never"
    cmd = ["git", "-c", "core.hooksPath=/dev/null", "-c", "core.fsmonitor=false",
           "-c", f"protocol.file.allow={protocol}", *args]
    try:
        result = subprocess.run(cmd, cwd=cwd, env=git_env(), capture_output=True,
                                text=True, timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckoutFailure(f"git execution failed: {type(exc).__name__}") from exc
    if result.returncode:
        # No command line, environment, or credential URLs in the error log.
        tail = (result.stderr or result.stdout).strip()[-600:]
        raise CheckoutFailure(f"git {args[0]} exit {result.returncode}: {tail}")
    return result.stdout.strip()


def verify_checkout(destination: Path, *, expected_url: str = PUBLIC_URL,
                    local_fixture: bool = False) -> dict[str, object]:
    if not destination.is_dir():
        raise CheckoutFailure("checkout directory does not exist")
    def g(*args: str) -> str:
        return run_git(args, cwd=destination, local_fixture=local_fixture)

    actual_url = g("remote", "get-url", "origin")
    if actual_url != expected_url:
        raise CheckoutFailure("origin URL mismatch; refuse noncanonical source")
    if g("rev-parse", "--is-inside-work-tree") != "true":
        raise CheckoutFailure("not a Git working tree")
    if g("rev-parse", "--is-shallow-repository") != "false":
        raise CheckoutFailure("shallow checkout is not eligible")
    if g("symbolic-ref", "--short", "HEAD") != "main":
        raise CheckoutFailure("checked-out branch is not main")
    head = g("rev-parse", "--verify", "HEAD^{commit}")
    remote_head = g("rev-parse", "--verify", "refs/remotes/origin/main^{commit}")
    if head != remote_head:
        raise CheckoutFailure("local HEAD differs from origin/main")
    if g("status", "--porcelain=v1", "--untracked-files=all"):
        raise CheckoutFailure("worktree or index is not clean")
    # Object-integrity validation is necessary but does not establish source rights.
    g("fsck", "--full", "--strict", "--no-reflogs")
    tracked = g("ls-files", "-s").splitlines()
    if any(line.startswith("160000 ") for line in tracked):
        raise CheckoutFailure("submodules require separately reviewed provenance")
    return {
        "status": "PASS",
        "scope": "git checkout integrity only; NOT product release qualification",
        "origin": actual_url,
        "branch": "main",
        "head": head,
        "origin_main": remote_head,
        "is_shallow": False,
        "worktree_clean": True,
        "git_fsck": "PASS",
        "tracked_entries": len(tracked),
        "local_fixture": local_fixture,
    }


def checkout(destination: Path, *, source_url: str = PUBLIC_URL,
             local_fixture: bool = False) -> dict[str, object]:
    if destination.exists() or destination.is_symlink():
        raise CheckoutFailure("destination exists; refusing overwrite")
    if not destination.parent.is_dir():
        raise CheckoutFailure("destination parent does not exist")
    if local_fixture:
        parsed = urlparse(source_url)
        if parsed.scheme != "file" or not parsed.path.startswith("/") or parsed.netloc:
            raise CheckoutFailure("test fixture must use an absolute local file:// URL")
    elif source_url != PUBLIC_URL:
        raise CheckoutFailure("only the canonical PUBLIC GitHub repository is allowed")
    run_git(["clone", "--no-tags", "--no-single-branch", "--branch", "main",
             "--", source_url, str(destination)], local_fixture=local_fixture)
    return verify_checkout(destination, expected_url=source_url, local_fixture=local_fixture)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--test-local-url", default=None,
                        help="Only for isolated test fixtures; requires --allow-local-fixture")
    parser.add_argument("--allow-local-fixture", action="store_true")
    args = parser.parse_args()
    if args.test_local_url is not None and not args.allow_local_fixture:
        parser.error("--test-local-url requires --allow-local-fixture")
    if args.allow_local_fixture and args.test_local_url is None:
        parser.error("--allow-local-fixture requires --test-local-url")
    try:
        result = checkout(args.destination,
                          source_url=args.test_local_url or PUBLIC_URL,
                          local_fixture=args.allow_local_fixture)
    except CheckoutFailure as exc:
        print(json.dumps({"status": "FAIL", "scope": "PUBLIC trusted checkout",
                          "error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
