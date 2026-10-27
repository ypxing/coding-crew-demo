"""Command-line entry point: ``python -m textstats FILE [--top N]``."""

import argparse

from textstats.report import format_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="textstats", description="Print a text summary.")
    parser.add_argument("file", help="UTF-8 text file to summarise")
    parser.add_argument("--top", type=int, default=3, help="number of top words to list")
    args = parser.parse_args(argv)

    with open(args.file, encoding="utf-8") as fh:
        text = fh.read()
    print(format_report(text, n=args.top))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
