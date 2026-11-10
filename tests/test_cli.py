from pathlib import Path

import pytest

from textstats.__main__ import main
from textstats.report import format_report


def test_main_prints_report_for_utf8_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("the cat the a cat the", encoding="utf-8")

    exit_code = main([str(path)])

    assert exit_code == 0
    assert capsys.readouterr().out == format_report("the cat the a cat the") + "\n"
