from pathlib import Path

import pytest

from textstats import format_report
from textstats.__main__ import main


def test_main_prints_report_for_file_and_returns_zero(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    text = "the cat the a cat the"
    path = tmp_path / "in.txt"
    path.write_text(text, encoding="utf-8")

    assert main([str(path)]) == 0
    assert capsys.readouterr().out == format_report(text) + "\n"


def test_main_top_limits_number_of_top_words(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "in.txt"
    path.write_text("d c c b b b a a a a", encoding="utf-8")

    assert main([str(path), "--top", "2"]) == 0
    assert capsys.readouterr().out.endswith("top words:\n  a: 4\n  b: 3\n")
