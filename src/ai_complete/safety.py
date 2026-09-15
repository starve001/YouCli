from __future__ import annotations

import re


_DANGEROUS = re.compile(
    r"(?:^|[;&|]\s*)(?:sudo\s+)?(?:"
    r"rm\s+(?:-[^\s]*r[^\s]*\s+)?(?:-[^\s]*\s+)?(?:/|~|\$HOME)"
    r"|mkfs(?:\s|$)|shutdown(?:\s|$)|reboot(?:\s|$)|dd\s+if="
    r"|chmod\s+-R\s+777|curl[^\n|]*\|\s*(?:ba)?sh|wget[^\n|]*\|\s*(?:ba)?sh"
    r")",
    re.IGNORECASE,
)


def is_safe_candidate(original: str, candidate: str) -> bool:
    if "\n" in candidate or "\r" in candidate or "\x00" in candidate:
        return False
    if not candidate.startswith(original[: min(len(original), 1)]):
        return False
    return _DANGEROUS.search(candidate) is None
