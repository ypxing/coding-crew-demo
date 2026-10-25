import pytest

import textstats
from textstats import format_report


def test_format_report_is_exported() -> None:
    assert "format_report" in textstats.__all__


def test_format_report_empty_text() -> None:
    assert format_report("") == (
        "words: 0\ncharacters: 0\ncharacters (no spaces): 0\ntop words:\n  (none)"
    )


def test_format_report_limits_top_words_to_n() -> None:
    assert format_report("b a b c a b", n=2).splitlines()[-2:] == ["  b: 3", "  a: 2"]


def test_format_report_ties_are_alphabetical() -> None:
    assert format_report("z y x", n=2).splitlines()[-2:] == ["  x: 1", "  y: 1"]


def test_format_report_zero_top_words_shows_none() -> None:
    assert format_report("a b", n=0).splitlines()[-1] == "  (none)"


def test_format_report_rejects_negative_n() -> None:
    with pytest.raises(ValueError):
        format_report("a", n=-1)


def test_format_report_labeled_lines() -> None:
    assert format_report("the cat the a cat the") == (
        "words: 6\n"
        "characters: 21\n"
        "characters (no spaces): 16\n"
        "top words:\n"
        "  the: 3\n"
        "  cat: 2\n"
        "  a: 1"
    )
