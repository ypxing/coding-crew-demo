"""Command-line entry point: ``python -m textstats FILE [--top N]``."""

import argparse
import sys

from textstats.report import format_report


def main(argv: list[str] | None = None) -> int:
    """Print the report for FILE and return the process exit code."""
    parser = argparse.ArgumentParser(prog="textstats", description="Print a text report for FILE.")
    parser.add_argument("file", help="UTF-8 text file to summarise")
    parser.add_argument("--top", type=int, default=3, help="number of top words to list")
    args = parser.parse_args(argv)
    if args.top < 0:
        parser.error(f"--top must be non-negative, got {args.top}")

    try:
        with open(args.file, encoding="utf-8") as handle:
            text = handle.read()
    except (OSError, UnicodeDecodeError) as exc:
        reason = (exc.strerror if isinstance(exc, OSError) else None) or str(exc)
        print(f"textstats: error: {reason}", file=sys.stderr)
        return 1
    print(format_report(text, n=args.top))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
