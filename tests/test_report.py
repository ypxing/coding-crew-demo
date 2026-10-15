import textstats


def test_report_is_exported() -> None:
    assert "report" in textstats.__all__
