"""Command-line entry point: ``textstats [FILE] [--top N]``."""

import argparse
import sys

from textstats.report import report


def _read(file: str) -> str:
    # UTF-8 with no newline translation, so a file and the same bytes on stdin report alike.
    if file == "-":
        return sys.stdin.buffer.read().decode("utf-8")
    with open(file, encoding="utf-8", newline="") as f:
        return f.read()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="textstats", description="Print a plain-text stats report for FILE or stdin."
    )
    parser.add_argument("file", nargs="?", default="-", metavar="FILE", help="'-' or absent: stdin")
    parser.add_argument("--top", type=int, default=3, help="number of top words (default: 3)")
    args = parser.parse_args(argv)
    if args.top < 0:
        parser.error(f"--top must be 0 or more, got {args.top}")
    source = "stdin" if args.file == "-" else args.file
    try:
        text = _read(args.file)
    except OSError as exc:
        parser.error(f"cannot read {source}: {exc.strerror}")
    except UnicodeDecodeError:
        parser.error(f"{source} is not valid UTF-8")
    sys.stdout.write(report(text, top=args.top))
    return 0
