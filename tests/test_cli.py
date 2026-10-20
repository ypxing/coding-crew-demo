from pathlib import Path

import pytest

from textstats import format_report


def test_main_prints_report_for_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    from textstats.__main__ import main

    text = "the cat the a cat the"
    sample = tmp_path / "sample.txt"
    sample.write_text(text, encoding="utf-8")

    assert main([str(sample)]) == 0
    assert capsys.readouterr().out == format_report(text) + "\n"
