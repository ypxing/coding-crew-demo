import textstats
from textstats import format_report


def test_format_report_sample_text() -> None:
    expected = "\n".join(
        [
            "words: 6",
            "characters: 21",
            "characters (no spaces): 16",
            "top words:",
            "  the: 3",
            "  cat: 2",
            "  a: 1",
        ]
    )
    assert format_report("the cat the a cat the") == expected


def test_format_report_is_exported() -> None:
    assert "format_report" in textstats.__all__


def test_format_report_empty_text_has_no_top_words() -> None:
    assert format_report("") == "\n".join(
        ["words: 0", "characters: 0", "characters (no spaces): 0", "top words:", "  (none)"]
    )
