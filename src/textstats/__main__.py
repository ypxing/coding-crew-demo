"""Command-line entry point: ``python -m textstats FILE [--top N]``."""

import argparse
import sys
from pathlib import Path

from textstats.report import format_report


def main(argv: list[str] | None = None) -> int:
    """Print the report for FILE and return the process exit code."""
    parser = argparse.ArgumentParser(prog="textstats", description="Summarise a text file.")
    parser.add_argument("file", metavar="FILE", help="UTF-8 text file to summarise")
    parser.add_argument(
        "--top", type=int, default=3, metavar="N", help="number of top words (default: 3)"
    )
    args = parser.parse_args(argv)
    try:
        text = Path(args.file).read_text(encoding="utf-8")
    except OSError as exc:
        print(f"textstats: error: {exc}", file=sys.stderr)
        return 1
    print(format_report(text, n=args.top))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
