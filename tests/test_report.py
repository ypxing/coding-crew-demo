import textstats
from textstats import format_report


def test_format_report_labeled_lines_without_trailing_newline() -> None:
    assert format_report("the cat the a cat the") == (
        "words: 6\n"
        "characters: 21\n"
        "characters (no spaces): 16\n"
        "top words:\n"
        "  the: 3\n"
        "  cat: 2\n"
        "  a: 1"
    )
    assert "format_report" in textstats.__all__
