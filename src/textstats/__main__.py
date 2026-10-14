"""Command-line entry point: ``python -m textstats FILE [--top N]``."""

import argparse
from pathlib import Path

from textstats.report import format_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="textstats")
    parser.add_argument("file", metavar="FILE")
    parser.add_argument("--top", type=int, default=3, metavar="N", help="number of top words")
    args = parser.parse_args(argv)
    text = Path(args.file).read_text(encoding="utf-8")
    print(format_report(text, n=args.top))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
