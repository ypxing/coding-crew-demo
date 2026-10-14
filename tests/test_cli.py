from pathlib import Path

import pytest

from textstats import format_report
from textstats.__main__ import main


def test_main_prints_report_for_file_and_returns_zero(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    text = "the cat the a cat the dog"
    path = tmp_path / "input.txt"
    path.write_text(text, encoding="utf-8")

    assert main([str(path)]) == 0

    captured = capsys.readouterr()
    assert captured.out == format_report(text) + "\n"
    assert captured.err == ""


def test_main_top_limits_report_to_n_words(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    text = "the cat the a cat the dog"
    path = tmp_path / "input.txt"
    path.write_text(text, encoding="utf-8")

    assert main([str(path), "--top", "2"]) == 0

    out = capsys.readouterr().out
    assert out == format_report(text, n=2) + "\n"
    assert out.endswith("top words:\n  the: 3\n  cat: 2\n")
