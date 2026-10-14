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


def test_main_top_limits_top_words(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "input.txt"
    path.write_text("d c b a d c b d c d", encoding="utf-8")

    assert main([str(path), "--top", "2"]) == 0
    assert capsys.readouterr().out.endswith("top words:\n  d: 4\n  c: 3\n")


def test_main_lists_three_top_words_by_default(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "input.txt"
    path.write_text("d c b a d c b d c d", encoding="utf-8")

    assert main([str(path)]) == 0
    assert capsys.readouterr().out.endswith("top words:\n  d: 4\n  c: 3\n  b: 2\n")
