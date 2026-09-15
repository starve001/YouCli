from __future__ import annotations

import os
import stat
from dataclasses import dataclass
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 fallback
    import tomli as tomllib


@dataclass(frozen=True)
class Config:
    base_url: str
    model: str
    api_key: str
    timeout: float = 15.0


def config_path() -> Path:
    override = os.environ.get("AI_COMPLETE_CONFIG")
    if override:
        return Path(override).expanduser()
    return Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "ai-complete" / "config.toml"


def load_config() -> Config:
    path = config_path()
    values: dict[str, object] = {}
    if path.is_file():
        with path.open("rb") as file:
            values = tomllib.load(file)
        mode = stat.S_IMODE(path.stat().st_mode)
        if os.name != "nt" and mode & 0o077:
            raise ValueError(f"配置文件权限过宽，请执行: chmod 600 {path}")

    api_key = os.environ.get("AI_COMPLETE_API_KEY", str(values.get("api_key", "")))
    base_url = os.environ.get(
        "AI_COMPLETE_BASE_URL",
        str(values.get("base_url", "https://api.openai.com/v1")),
    )
    model = os.environ.get("AI_COMPLETE_MODEL", str(values.get("model", "gpt-4o-mini")))
    try:
        timeout = float(os.environ.get("AI_COMPLETE_TIMEOUT", values.get("timeout", 15.0)))
    except (TypeError, ValueError) as exc:
        raise ValueError("AI_COMPLETE_TIMEOUT 或配置文件中的 timeout 必须是数字") from exc
    if timeout <= 0:
        raise ValueError("timeout 必须大于 0")
    if not api_key:
        raise ValueError("未配置 API Key，请设置 AI_COMPLETE_API_KEY 或创建配置文件")
    return Config(base_url=base_url.rstrip("/"), model=model, api_key=api_key, timeout=timeout)
