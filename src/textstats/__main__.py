"""Command-line entry point: ``python -m textstats FILE``."""

import argparse
import sys

from textstats.report import format_report


def main(argv: list[str] | None = None) -> int:
    """Print the report for the file named in ``argv`` and return the exit code."""
    parser = argparse.ArgumentParser(prog="textstats")
    parser.add_argument("file", metavar="FILE")
    parser.add_argument("--top", metavar="N", type=int, default=3)
    args = parser.parse_args(argv)
    try:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    except OSError as exc:
        print(f"textstats: error: {exc}", file=sys.stderr)
        return 1
    print(format_report(text, n=args.top))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
