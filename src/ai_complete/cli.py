from __future__ import annotations

import argparse
import sys

from .config import load_config
from .context import make_context
from .provider import ProviderError, complete
from .safety import is_safe_candidate


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI-powered terminal completion")
    parser.add_argument(
        "--shell",
        default="bash",
        choices=("bash", "zsh", "powershell"),
        help="当前 Shell（支持 bash、zsh、PowerShell）",
    )
    parser.add_argument("--line", required=True, help="当前命令行")
    parser.add_argument("--cursor", type=int, required=True, help="光标位置")
    parser.add_argument("--show-description", action="store_true")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        config = load_config()
        context = make_context(args.shell, args.line, args.cursor)
        result = complete(config, context)
        if not is_safe_candidate(args.line, result.line):
            raise ProviderError(f"已拒绝模型生成的可疑命令: {result.line!r}")
    except (ValueError, ProviderError) as exc:
        print(f"ai-complete: {exc}", file=sys.stderr)
        return 1
    print(result.line)
    if args.show_description and result.description:
        print(f"# {result.description}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
