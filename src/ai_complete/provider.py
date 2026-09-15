from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass

import httpx

from .config import Config
from .context import CompletionContext
from .prompt import make_messages


@dataclass(frozen=True)
class Completion:
    line: str
    description: str


class ProviderError(RuntimeError):
    pass


def _parse_completion(content: str, original: str) -> Completion:
    content = content.strip()
    if not content:
        return Completion(original, "")
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        if content.startswith("```") and content.endswith("```"):
            lines = content.splitlines()
            fenced_content = "\n".join(lines[1:-1]).strip()
            try:
                data = json.loads(fenced_content)
            except json.JSONDecodeError as exc:
                raise ProviderError("模型返回的补全不是有效 JSON") from exc
        else:
            decoder = json.JSONDecoder()
            for index, character in enumerate(content):
                if character == "{":
                    try:
                        data, _ = decoder.raw_decode(content[index:])
                        break
                    except json.JSONDecodeError:
                        continue
            else:
                if "\n" not in content and "\r" not in content:
                    return Completion(content, "")
                raise ProviderError("模型返回的补全不是有效 JSON")
    try:
        line = data["line"]
        description = data.get("description", "")
    except (KeyError, TypeError) as exc:
        raise ProviderError("模型返回缺少 line 字段") from exc
    if not isinstance(line, str) or "\n" in line or "\r" in line:
        raise ProviderError("模型返回了无效的多行或非字符串命令")
    if not line.strip():
        return Completion(original, "")
    return Completion(line, str(description))


def complete(config: Config, context: CompletionContext) -> Completion:
    payload = {
        "model": config.model,
        "temperature": 0.1,
        "max_tokens": 160,
        "messages": make_messages(context),
    }
    headers = {"Authorization": f"Bearer {config.api_key}", "Content-Type": "application/json"}
    try:
        with httpx.Client(timeout=config.timeout) as client:
            response = client.post(
                f"{config.base_url}/chat/completions",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            if os.environ.get("AI_COMPLETE_DEBUG") == "1":
                print(f"ai-complete debug: model={data.get('model')!r}", file=sys.stderr)
                print(f"ai-complete debug: content={content!r}", file=sys.stderr)
            if not content or not content.strip():
                fallback_payload = {
                    "model": config.model,
                    "temperature": 0.1,
                    "max_tokens": 80,
                    "messages": [
                        {
                            "role": "system",
                            "content": "只返回补全后的完整单行终端命令，不要解释，不要 Markdown。",
                        },
                        {
                            "role": "user",
                            "content": (
                                f"Shell: {context.shell}\n"
                                f"当前命令行: {context.line}\n"
                                f"光标位置: {context.cursor}\n"
                                "请补全当前命令行。"
                            ),
                        },
                    ],
                }
                fallback_response = client.post(
                    f"{config.base_url}/chat/completions",
                    json=fallback_payload,
                    headers=headers,
                )
                fallback_response.raise_for_status()
                fallback_data = fallback_response.json()
                content = fallback_data["choices"][0]["message"]["content"]
                if os.environ.get("AI_COMPLETE_DEBUG") == "1":
                    print(
                        f"ai-complete debug: fallback_model={fallback_data.get('model')!r}",
                        file=sys.stderr,
                    )
                    print(f"ai-complete debug: fallback_content={content!r}", file=sys.stderr)
    except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError) as exc:
        raise ProviderError(f"模型请求失败: {exc}") from exc
    return _parse_completion(content, context.line)
