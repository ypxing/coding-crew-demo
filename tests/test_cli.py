from pathlib import Path

import pytest

from textstats import format_report
from textstats.__main__ import main

TEXT = "the cat the a cat the dog"


def _write(tmp_path: Path, text: str = TEXT) -> str:
    path = tmp_path / "input.txt"
    path.write_text(text, encoding="utf-8")
    return str(path)


def test_main_prints_report_for_file_and_returns_zero(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([_write(tmp_path)]) == 0
    out, err = capsys.readouterr()
    assert out == format_report(TEXT) + "\n"
    assert err == ""
