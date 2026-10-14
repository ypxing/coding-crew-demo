from pathlib import Path

import pytest

from textstats import format_report
from textstats.__main__ import main


def test_main_prints_report_for_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    contents = "the cat the a cat the dog"
    path = tmp_path / "input.txt"
    path.write_text(contents, encoding="utf-8")

    assert main([str(path)]) == 0
    assert capsys.readouterr().out == format_report(contents) + "\n"
