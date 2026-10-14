"""Command-line entry point: ``python -m textstats FILE [--top N]``."""

import argparse
from pathlib import Path

from textstats.report import format_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="textstats")
    parser.add_argument("file", metavar="FILE")
    parser.add_argument("--top", metavar="N", type=int, default=3)
    args = parser.parse_args(argv)
    text = Path(args.file).read_text()
    print(format_report(text, n=args.top))
    return 0
