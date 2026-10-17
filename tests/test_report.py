import pytest

from textstats.report import format_report


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


def test_format_report_is_exported_from_package() -> None:
    import textstats

    assert textstats.format_report is format_report
    assert "format_report" in textstats.__all__


def test_format_report_limits_top_words_to_n() -> None:
    lines = format_report("the cat the a cat the", n=2).splitlines()
    assert lines[4:] == ["  the: 3", "  cat: 2"]


def test_format_report_breaks_ties_alphabetically() -> None:
    lines = format_report("zebra apple", n=2).splitlines()
    assert lines[4:] == ["  apple: 1", "  zebra: 1"]


def test_format_report_empty_text_shows_none() -> None:
    assert format_report("") == (
        "words: 0\n"
        "characters: 0\n"
        "characters (no spaces): 0\n"
        "top words:\n"
        "  (none)"
    )


def test_format_report_zero_n_shows_none() -> None:
    assert format_report("a b", n=0).splitlines()[4:] == ["  (none)"]


def test_format_report_rejects_negative_n() -> None:
    with pytest.raises(ValueError):
        format_report("a", n=-1)
