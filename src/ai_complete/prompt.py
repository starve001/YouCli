from __future__ import annotations

import json

from .context import CompletionContext


SYSTEM_PROMPT = """你是跨平台终端命令补全引擎。
根据 Shell、当前目录、Git 分支和光标位置，补全用户当前命令行。
只输出 JSON，不要 Markdown、解释或额外文本，格式必须是：
{"line":"完整替换后的命令行","description":"一句简短中文说明"}
规则：
1. 只修改输入缓冲区，不执行命令。
2. 保留用户已经输入的内容；不确定时原样返回。
3. 不主动生成 rm -rf、磁盘格式化、权限破坏、反弹 Shell 或其他明显危险命令。
4. line 必须是单行字符串。"""


def make_messages(context: CompletionContext) -> list[dict[str, str]]:
    payload = {
        "shell": context.shell,
        "line": context.line,
        "cursor": context.cursor,
        "prefix": context.line[: context.cursor],
        "suffix": context.line[context.cursor :],
        "cwd": context.cwd,
        "git_branch": context.git_branch,
    }
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
    ]
