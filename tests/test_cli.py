from pathlib import Path

import pytest

from textstats import format_report
from textstats.__main__ import main


def test_main_prints_report_for_utf8_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("the cat the a cat the", encoding="utf-8")

    code = main([str(path)])

    out = capsys.readouterr().out
    assert code == 0
    assert out == format_report("the cat the a cat the") + "\n"
