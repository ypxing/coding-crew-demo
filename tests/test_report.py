import pytest

from textstats import format_report


def test_format_report_summarises_text() -> None:
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


def test_format_report_shows_none_when_no_top_words() -> None:
    assert format_report("") == "\n".join(
        ["words: 0", "characters: 0", "characters (no spaces): 0", "top words:", "  (none)"]
    )
    assert format_report("a b", n=0).endswith("top words:\n  (none)")


def test_format_report_limits_top_words_with_ties_alphabetical() -> None:
    assert format_report("b a b c a b", n=2).splitlines()[-2:] == ["  b: 3", "  a: 2"]


def test_format_report_rejects_negative_n() -> None:
    with pytest.raises(ValueError):
        format_report("a", n=-1)
