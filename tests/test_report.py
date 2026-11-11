import pytest

import textstats
from textstats import format_report


def test_format_report_summarises_text() -> None:
    expected = (
        "words: 6\n"
        "characters: 21\n"
        "characters (no spaces): 16\n"
        "top words:\n"
        "  the: 3\n"
        "  cat: 2\n"
        "  a: 1"
    )
    assert format_report("the cat the a cat the") == expected


def test_format_report_empty_text_shows_none() -> None:
    expected = (
        "words: 0\n"
        "characters: 0\n"
        "characters (no spaces): 0\n"
        "top words:\n"
        "  (none)"
    )
    assert format_report("") == expected


def test_format_report_zero_top_words_shows_none() -> None:
    assert format_report("a b", n=0).endswith("top words:\n  (none)")


def test_format_report_limits_top_words_with_ties_alphabetical() -> None:
    assert format_report("d c b a", n=2).endswith("top words:\n  a: 1\n  b: 1")


def test_format_report_rejects_negative_n() -> None:
    with pytest.raises(ValueError):
        format_report("a", n=-1)


def test_format_report_is_exported_from_package() -> None:
    assert "format_report" in textstats.__all__
