import pytest

import textstats
from textstats import format_report


def test_format_report_is_exported() -> None:
    assert "format_report" in textstats.__all__


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


def test_format_report_empty_text() -> None:
    assert format_report("") == (
        "words: 0\ncharacters: 0\ncharacters (no spaces): 0\ntop words:\n  (none)"
    )


def test_format_report_n_zero_shows_none() -> None:
    assert format_report("a b", n=0).endswith("top words:\n  (none)")


def test_format_report_limits_top_words_and_breaks_ties_alphabetically() -> None:
    assert format_report("z y x z", n=2).endswith("top words:\n  z: 2\n  x: 1")


def test_format_report_rejects_negative_n() -> None:
    with pytest.raises(ValueError):
        format_report("a", n=-1)
