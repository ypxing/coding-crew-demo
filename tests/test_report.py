import pytest

from textstats import format_report


def test_format_report_normal_text() -> None:
    assert format_report("the cat the a cat the") == (
        "words: 6\n"
        "characters: 21\n"
        "characters (no spaces): 16\n"
        "top words:\n"
        "  the: 3\n"
        "  cat: 2\n"
        "  a: 1"
    )


def test_format_report_limits_top_words_to_n() -> None:
    assert format_report("the cat the a cat the", n=2).endswith("top words:\n  the: 3\n  cat: 2")


def test_format_report_breaks_ties_alphabetically() -> None:
    assert format_report("b a", n=2).endswith("top words:\n  a: 1\n  b: 1")


def test_format_report_empty_text() -> None:
    assert format_report("") == (
        "words: 0\ncharacters: 0\ncharacters (no spaces): 0\ntop words:\n  (none)"
    )


def test_format_report_zero_top_words_shows_none() -> None:
    assert format_report("a b", n=0).endswith("top words:\n  (none)")


def test_format_report_negative_n_raises() -> None:
    with pytest.raises(ValueError):
        format_report("a", n=-1)


def test_format_report_is_exported_from_package() -> None:
    import textstats

    assert "format_report" in textstats.__all__
