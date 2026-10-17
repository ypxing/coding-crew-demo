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
