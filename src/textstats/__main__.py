"""Command-line entry point: ``python -m textstats FILE [--top N]``."""

import argparse
import sys

from textstats.report import format_report


def _non_negative_int(value: str) -> int:
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid int value: {value!r}") from None
    if number < 0:
        raise argparse.ArgumentTypeError(f"must be non-negative: {value!r}")
    return number


def main(argv: list[str] | None = None) -> int:
    """Print the report for FILE and return the process exit code."""
    parser = argparse.ArgumentParser(prog="textstats")
    parser.add_argument("file")
    parser.add_argument("--top", type=_non_negative_int, default=3)
    args = parser.parse_args(argv)

    try:
        with open(args.file, encoding="utf-8") as fh:
            contents = fh.read()
    except (OSError, UnicodeDecodeError) as exc:
        print(f"textstats: error: {exc}", file=sys.stderr)
        return 1

    print(format_report(contents, args.top))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
