"""Command-line entry point: ``python -m textstats FILE [--top N]``."""

from pathlib import Path

from textstats.report import format_report


def main(argv: list[str] | None = None) -> int:
    path = Path(argv[0]) if argv else Path()
    text = path.read_text(encoding="utf-8")
    print(format_report(text))
    return 0
