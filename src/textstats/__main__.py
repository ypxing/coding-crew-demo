import argparse

from textstats.report import format_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="textstats")
    parser.add_argument("file")
    args = parser.parse_args(argv)
    with open(args.file, encoding="utf-8") as fh:
        text = fh.read()
    print(format_report(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
