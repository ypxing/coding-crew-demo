"""Command-line entry point: ``python -m textstats FILE``."""

import argparse

from textstats.report import format_report


def main(argv: list[str] | None = None) -> int:
    """Print the report for the file named in ``argv`` and return the exit code."""
    parser = argparse.ArgumentParser(prog="textstats")
    parser.add_argument("file", metavar="FILE")
    args = parser.parse_args(argv)
    with open(args.file, encoding="utf-8") as f:
        text = f.read()
    print(format_report(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
