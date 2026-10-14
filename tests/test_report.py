import pytest

import textstats
from textstats import format_report


def test_format_report_is_exported() -> None:
    assert "format_report" in textstats.__all__
    assert callable(getattr(textstats, "format_report", None))


def test_format_report_full_summary() -> None:
    assert format_report("the cat the a cat the") == (
        "words: 6\n"
        "characters: 21\n"
        "characters (no spaces): 16\n"
        "top words:\n"
        "  the: 3\n"
        "  cat: 2\n"
        "  a: 1"
    )


def test_format_report_empty_text_shows_none() -> None:
    assert format_report("") == (
        "words: 0\ncharacters: 0\ncharacters (no spaces): 0\ntop words:\n  (none)"
    )


def test_format_report_limits_top_words_to_n() -> None:
    assert format_report("b a b c a b", n=2) == (
        "words: 6\n"
        "characters: 11\n"
        "characters (no spaces): 6\n"
        "top words:\n"
        "  b: 3\n"
        "  a: 2"
    )


def test_format_report_breaks_ties_alphabetically() -> None:
    assert format_report("b a c b a c d", n=2) == (
        "words: 7\n"
        "characters: 13\n"
        "characters (no spaces): 7\n"
        "top words:\n"
        "  a: 2\n"
        "  b: 2"
    )


def test_format_report_zero_n_shows_none() -> None:
    assert format_report("a b", n=0) == (
        "words: 2\ncharacters: 3\ncharacters (no spaces): 2\ntop words:\n  (none)"
    )


def test_format_report_rejects_negative_n() -> None:
    with pytest.raises(ValueError):
        format_report("a", n=-1)
