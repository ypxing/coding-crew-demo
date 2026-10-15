import pytest

import textstats
from textstats import report


def test_report_is_exported() -> None:
    assert "report" in textstats.__all__


def test_report_exact_format() -> None:
    assert report("b a b c a b", top=2) == (
        "words: 6\ncharacters: 11\ncharacters (no spaces): 6\ntop words:\n  b  3\n  a  2\n"
    )


def test_report_defaults_to_top_three_in_top_words_order() -> None:
    rows = report("d c c b b b a a a a e e").splitlines()[4:]
    assert rows == ["  a  4", "  b  3", "  c  2"]


def test_report_pads_words_to_longest_shown() -> None:
    rows = report("aaa b b", top=2).splitlines()[4:]
    assert rows == ["  b    2", "  aaa  1"]


def test_report_without_words_shows_none() -> None:
    empty = report("")
    assert empty.startswith("words: 0\ncharacters: 0\ncharacters (no spaces): 0\n")
    assert empty.endswith("top words:\n  (none)\n")
    assert report("x", top=0).endswith("top words:\n  (none)\n")


def test_report_rejects_negative_top() -> None:
    with pytest.raises(ValueError):
        report("a", top=-1)
