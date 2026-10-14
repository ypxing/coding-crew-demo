import os
import subprocess
import sys
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


def test_main_lists_three_top_words_by_default(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "in.txt"
    path.write_text("d c c b b b a a a a", encoding="utf-8")

    assert main([str(path)]) == 0
    assert capsys.readouterr().out.endswith("top words:\n  a: 4\n  b: 3\n  c: 2\n")


def test_python_m_textstats_prints_report(tmp_path: Path) -> None:
    text = "the cat the a cat the"
    path = tmp_path / "in.txt"
    path.write_text(text, encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == format_report(text) + "\n"


def test_file_is_decoded_as_utf8_regardless_of_locale(tmp_path: Path) -> None:
    path = tmp_path / "in.txt"
    path.write_text("café", encoding="utf-8")
    # Force an ASCII locale encoding: disable C-locale coercion and UTF-8 mode.
    env = {**os.environ, "LC_ALL": "C", "PYTHONCOERCECLOCALE": "0", "PYTHONUTF8": "0"}

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "characters: 4\n" in result.stdout


def test_missing_file_reports_error_and_returns_one(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(tmp_path / "missing.txt")]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")
    assert "Traceback" not in captured.err


def test_directory_path_reports_error_and_returns_one(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(tmp_path)]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")
