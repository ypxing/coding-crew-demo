"""Command-line entry point: ``python -m textstats FILE [--top N]``."""

from textstats.report import format_report


def main(argv: list[str] | None = None) -> int:
    path = (argv or [])[0]
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    print(format_report(text))
    return 0
