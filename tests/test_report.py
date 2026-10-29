import pytest

import textstats
from textstats import format_report


def test_format_report_summarises_words_characters_and_top_words() -> None:
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


def test_format_report_shows_none_for_empty_text() -> None:
    assert format_report("") == (
        "words: 0\ncharacters: 0\ncharacters (no spaces): 0\ntop words:\n  (none)"
    )


def test_format_report_shows_none_when_n_is_zero() -> None:
    assert format_report("a b", n=0).endswith("top words:\n  (none)")


def test_format_report_limits_top_words_to_n_in_count_then_alphabetical_order() -> None:
    report = format_report("b a b c a b", n=2)
    assert report.endswith("top words:\n  b: 3\n  a: 2")


def test_format_report_rejects_negative_n() -> None:
    with pytest.raises(ValueError):
        format_report("a", n=-1)


def test_format_report_is_exported_from_package() -> None:
    assert "format_report" in textstats.__all__
    assert textstats.format_report is format_report
