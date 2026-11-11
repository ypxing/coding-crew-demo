import pytest

import textstats
from textstats import format_report


def test_format_report_lists_counts_and_top_words() -> None:
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


def test_format_report_shows_none_when_no_top_words() -> None:
    assert format_report("") == (
        "words: 0\ncharacters: 0\ncharacters (no spaces): 0\ntop words:\n  (none)"
    )
    assert format_report("a b", n=0).endswith("top words:\n  (none)")


def test_format_report_limits_top_words_by_count_then_alphabetically() -> None:
    assert format_report("b a b c a b", n=2).endswith("top words:\n  b: 3\n  a: 2")


def test_format_report_rejects_negative_n() -> None:
    with pytest.raises(ValueError):
        format_report("a", n=-1)


def test_format_report_is_exported_from_package() -> None:
    assert "format_report" in textstats.__all__
