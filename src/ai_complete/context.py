from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CompletionContext:
    shell: str
    line: str
    cursor: int
    cwd: str
    git_branch: Optional[str]


def current_git_branch(cwd: str) -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", "-C", cwd, "branch", "--show-current"],
            capture_output=True,
            text=True,
            timeout=1,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    branch = result.stdout.strip()
    return branch or None


def make_context(shell: str, line: str, cursor: int) -> CompletionContext:
    return CompletionContext(
        shell=shell,
        line=line,
        cursor=max(0, min(cursor, len(line))),
        cwd=os.getcwd(),
        git_branch=current_git_branch(os.getcwd()),
    )
