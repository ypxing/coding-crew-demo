import os
import subprocess
import sys
from pathlib import Path

import pytest

from textstats.__main__ import main


def test_python_m_textstats_prints_report_for_file(tmp_path: Path) -> None:
    source = tmp_path / "sample.txt"
    source.write_text("the cat the a cat the", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(source)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == (
        "words: 6\n"
        "characters: 21\n"
        "characters (no spaces): 16\n"
        "top words:\n"
        "  the: 3\n"
        "  cat: 2\n"
        "  a: 1\n"
    )


def test_main_top_limits_top_words(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    source = tmp_path / "sample.txt"
    source.write_text("the cat the a cat the", encoding="utf-8")

    assert main([str(source), "--top", "2"]) == 0
    assert capsys.readouterr().out == (
        "words: 6\n"
        "characters: 21\n"
        "characters (no spaces): 16\n"
        "top words:\n"
        "  the: 3\n"
        "  cat: 2\n"
    )


def test_main_lists_three_top_words_by_default(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "sample.txt"
    source.write_text("the cat the a cat the dog", encoding="utf-8")

    assert main([str(source)]) == 0
    assert capsys.readouterr().out == (
        "words: 7\n"
        "characters: 25\n"
        "characters (no spaces): 19\n"
        "top words:\n"
        "  the: 3\n"
        "  cat: 2\n"
        "  a: 1\n"
    )


def test_python_m_textstats_reads_utf8_under_c_locale(tmp_path: Path) -> None:
    source = tmp_path / "accents.txt"
    source.write_bytes("café naïve".encode())
    env = {**os.environ, "LC_ALL": "C", "LANG": "C", "PYTHONUTF8": "0", "PYTHONCOERCECLOCALE": "0"}

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(source)],
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout == (
        "words: 3\n"
        "characters: 10\n"
        "characters (no spaces): 9\n"
        "top words:\n"
        "  caf: 1\n"
        "  na: 1\n"
        "  ve: 1\n"
    )


def test_main_missing_file_reports_error_and_returns_1(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    missing = tmp_path / "missing.txt"

    assert main([str(missing)]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_main_directory_reports_error_and_returns_1(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(tmp_path)]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")
