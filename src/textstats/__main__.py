"""Command-line entry point: ``python -m textstats FILE [--top N]``."""

import argparse
import sys

from textstats.report import format_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="textstats", description="Summarise a text file.")
    parser.add_argument("file", help="UTF-8 text file to summarise")
    parser.add_argument("--top", type=int, default=3, help="number of top words to list")
    args = parser.parse_args(argv)
    if args.top < 0:
        parser.error("--top must be zero or a positive integer")

    try:
        with open(args.file, encoding="utf-8") as handle:
            text = handle.read()
    except (OSError, UnicodeDecodeError) as exc:
        reason = exc.strerror or str(exc) if isinstance(exc, OSError) else str(exc)
        print(f"textstats: error: {reason}", file=sys.stderr)
        return 1
    print(format_report(text, n=args.top))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
