from pathlib import Path

import pytest

from textstats import format_report
from textstats.__main__ import main


def test_main_prints_report_and_returns_zero(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    text = "the cat the a cat the"
    path = tmp_path / "sample.txt"
    path.write_text(text, encoding="utf-8")

    assert main([str(path)]) == 0

    captured = capsys.readouterr()
    assert captured.out == format_report(text) + "\n"
    assert captured.err == ""


def test_main_top_limits_top_words(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("b a b c a b", encoding="utf-8")

    assert main([str(path), "--top", "2"]) == 0

    top_section = capsys.readouterr().out.split("top words:\n", 1)[1]
    assert top_section == "  b: 3\n  a: 2\n"


def test_main_defaults_to_three_top_words(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("d d d d c c c b b a", encoding="utf-8")

    assert main([str(path)]) == 0

    top_section = capsys.readouterr().out.split("top words:\n", 1)[1]
    assert top_section == "  d: 4\n  c: 3\n  b: 2\n"
