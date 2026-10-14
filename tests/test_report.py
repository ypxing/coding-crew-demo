import textstats


def test_format_report_is_exported() -> None:
    assert "format_report" in textstats.__all__
    assert callable(getattr(textstats, "format_report", None))
