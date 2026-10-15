import textstats
from textstats import report


def test_report_is_exported() -> None:
    assert "report" in textstats.__all__


def test_report_exact_format() -> None:
    assert report("b a b c a b", top=2) == (
        "words: 6\ncharacters: 11\ncharacters (no spaces): 6\ntop words:\n  b  3\n  a  2\n"
    )
