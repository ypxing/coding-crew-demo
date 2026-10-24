from pathlib import Path

import pytest

from textstats import format_report
from textstats.__main__ import main


def test_main_prints_report_for_utf8_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    source = tmp_path / "doc.txt"
    source.write_text("the cat the a cat the", encoding="utf-8")

    assert main([str(source)]) == 0
    assert capsys.readouterr().out == format_report("the cat the a cat the") + "\n"


def test_main_top_limits_top_words(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    source = tmp_path / "doc.txt"
    source.write_text("the cat the a cat the", encoding="utf-8")

    assert main([str(source), "--top", "2"]) == 0
    assert capsys.readouterr().out == format_report("the cat the a cat the", n=2) + "\n"


def test_main_defaults_to_three_top_words(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "doc.txt"
    source.write_text("one two three four four", encoding="utf-8")

    assert main([str(source)]) == 0
    top_lines = capsys.readouterr().out.splitlines()[4:]
    assert top_lines == ["  four: 2", "  one: 1", "  three: 1"]
