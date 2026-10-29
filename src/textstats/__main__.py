"""Command-line entry point: ``python -m textstats FILE [--top N]``."""

from textstats.report import format_report


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else []
    with open(args[0], encoding="utf-8") as handle:
        text = handle.read()
    print(format_report(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
