from pathlib import Path

import pytest

from textstats import report
from textstats.cli import main


def test_main_prints_report_for_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "in.txt"
    path.write_text("b a b c a b", encoding="utf-8")
    assert main([str(path)]) == 0
    assert capsys.readouterr().out == report("b a b c a b")
