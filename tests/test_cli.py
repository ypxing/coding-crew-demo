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


def test_main_top_limits_report_to_n_top_words(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([_write(tmp_path), "--top", "2"]) == 0
    out, _ = capsys.readouterr()
    assert out == format_report(TEXT, n=2) + "\n"
    assert out.endswith("top words:\n  the: 3\n  cat: 2\n")


def test_main_without_top_lists_up_to_three_top_words(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([_write(tmp_path)]) == 0
    out, _ = capsys.readouterr()
    assert out.endswith("top words:\n  the: 3\n  cat: 2\n  a: 1\n")
