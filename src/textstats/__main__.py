"""Command-line entry point: ``python -m textstats FILE [--top N]``."""

import argparse
import sys

from textstats.report import format_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="textstats", description="Summarise a text file.")
    parser.add_argument("file", help="UTF-8 text file to summarise")
    parser.add_argument("--top", type=int, default=3, help="number of top words to show")
    args = parser.parse_args(argv)

    try:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    except (OSError, UnicodeDecodeError) as exc:
        reason = getattr(exc, "strerror", None) or str(exc)
        print(f"textstats: error: {reason}", file=sys.stderr)
        return 1
    print(format_report(text, n=args.top))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
