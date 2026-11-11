import subprocess
import sys
from pathlib import Path

import pytest

from textstats.__main__ import main


def test_main_prints_report_for_utf8_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "doc.txt"
    path.write_text("the cat the a cat the dog", encoding="utf-8")

    assert main([str(path)]) == 0

    assert capsys.readouterr().out == (
        "words: 7\n"
        "characters: 25\n"
        "characters (no spaces): 19\n"
        "top words:\n"
        "  the: 3\n"
        "  cat: 2\n"
        "  a: 1\n"
    )


def test_main_top_limits_top_words(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "doc.txt"
    path.write_text("the cat the a cat the dog", encoding="utf-8")

    assert main([str(path), "--top", "2"]) == 0

    assert capsys.readouterr().out == (
        "words: 7\n"
        "characters: 25\n"
        "characters (no spaces): 19\n"
        "top words:\n"
        "  the: 3\n"
        "  cat: 2\n"
    )


def test_main_reports_missing_file_on_stderr_and_returns_1(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    missing = tmp_path / "missing.txt"

    assert main([str(missing)]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error: ")


def test_main_reports_directory_on_stderr_and_returns_1(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(tmp_path)]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error: ")


def test_main_reports_non_utf8_file_on_stderr_and_returns_1(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "doc.txt"
    path.write_bytes(b"\xff\xfe\xfa")

    assert main([str(path)]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error: ")


def test_main_rejects_negative_top_before_reading_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    missing = tmp_path / "missing.txt"

    with pytest.raises(SystemExit) as excinfo:
        main([str(missing), "--top", "-1"])

    assert excinfo.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "usage: textstats" in captured.err


def test_main_rejects_non_integer_top(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "doc.txt"
    path.write_text("the cat", encoding="utf-8")

    with pytest.raises(SystemExit) as excinfo:
        main([str(path), "--top", "abc"])

    assert excinfo.value.code == 2
    assert capsys.readouterr().out == ""


def test_python_m_textstats_prints_report_and_exits_zero(tmp_path: Path) -> None:
    path = tmp_path / "doc.txt"
    path.write_text("the cat the a cat the dog", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == (
        "words: 7\n"
        "characters: 25\n"
        "characters (no spaces): 19\n"
        "top words:\n"
        "  the: 3\n"
        "  cat: 2\n"
        "  a: 1\n"
    )


def test_main_reads_file_as_utf8_regardless_of_locale(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "doc.txt"
    path.write_text("café café", encoding="utf-8")

    assert main([str(path)]) == 0

    assert capsys.readouterr().out == (
        "words: 2\n"
        "characters: 9\n"
        "characters (no spaces): 8\n"
        "top words:\n"
        "  caf: 2\n"
    )
