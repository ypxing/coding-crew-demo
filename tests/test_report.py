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
