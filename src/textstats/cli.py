"""Command-line entry point: ``textstats [FILE] [--top N]``."""

import argparse
import sys

from textstats.report import report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="textstats")
    parser.add_argument("file", nargs="?", default="-")
    parser.add_argument("--top", type=int, default=3)
    args = parser.parse_args(argv)
    if args.top < 0:
        parser.error(f"--top must be 0 or more, got {args.top}")
    if args.file == "-":
        text = sys.stdin.buffer.read().decode("utf-8")
    else:
        with open(args.file, encoding="utf-8", newline="") as f:
            text = f.read()
    sys.stdout.write(report(text, top=args.top))
    return 0
