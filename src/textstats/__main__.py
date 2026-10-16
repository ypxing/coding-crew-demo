"""Command-line entry point: ``python -m textstats FILE [--top N]``."""

import argparse
from pathlib import Path

from textstats.report import format_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="textstats")
    parser.add_argument("FILE")
    args = parser.parse_args(argv)
    text = Path(args.FILE).read_text(encoding="utf-8")
    print(format_report(text))
    return 0
