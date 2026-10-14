"""Command-line entry point: ``python -m textstats FILE [--top N]``."""

import argparse
from pathlib import Path

from textstats.report import format_report


def main(argv: list[str] | None = None) -> int:
    """Print the report for FILE and return the process exit code."""
    parser = argparse.ArgumentParser(prog="textstats", description="Summarise a text file.")
    parser.add_argument("file", metavar="FILE", help="UTF-8 text file to summarise")
    args = parser.parse_args(argv)
    text = Path(args.file).read_text(encoding="utf-8")
    print(format_report(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
