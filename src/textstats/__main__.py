"""Command-line entry point: ``python -m textstats FILE [--top N]``."""

import argparse
import sys
from pathlib import Path

from textstats.report import format_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="textstats")
    parser.add_argument("FILE")
    parser.add_argument("--top", type=int, default=3)
    args = parser.parse_args(argv)
    try:
        text = Path(args.FILE).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"textstats: error: {exc}", file=sys.stderr)
        return 1
    print(format_report(text, n=args.top))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
