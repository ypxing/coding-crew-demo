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


def test_format_report_is_exported() -> None:
    assert "format_report" in textstats.__all__
    assert textstats.format_report is format_report


def test_format_report_limits_top_words_to_n() -> None:
    expected = (
        "words: 6\n"
        "characters: 21\n"
        "characters (no spaces): 16\n"
        "top words:\n"
        "  the: 3\n"
        "  cat: 2"
    )
    assert format_report("the cat the a cat the", n=2) == expected


def test_format_report_breaks_ties_alphabetically() -> None:
    expected = (
        "words: 3\n"
        "characters: 5\n"
        "characters (no spaces): 3\n"
        "top words:\n"
        "  a: 1\n"
        "  b: 1"
    )
    assert format_report("b a c", n=2) == expected


def test_format_report_empty_text() -> None:
    expected = (
        "words: 0\n"
        "characters: 0\n"
        "characters (no spaces): 0\n"
        "top words:\n"
        "  (none)"
    )
    assert format_report("") == expected


def test_format_report_zero_top_words_shows_none() -> None:
    expected = (
        "words: 2\n"
        "characters: 3\n"
        "characters (no spaces): 2\n"
        "top words:\n"
        "  (none)"
    )
    assert format_report("a b", n=0) == expected


def test_format_report_rejects_negative_n() -> None:
    with pytest.raises(ValueError):
        format_report("a", n=-1)
