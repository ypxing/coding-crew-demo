import subprocess
import sys
from pathlib import Path

import pytest

from textstats.__main__ import main
from textstats.report import format_report


def test_main_prints_report_and_returns_zero(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("the cat the a cat the", encoding="utf-8")

    assert main([str(path)]) == 0
    assert capsys.readouterr().out == format_report("the cat the a cat the") + "\n"


def test_top_option_limits_top_words(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("b a b c a b", encoding="utf-8")

    assert main([str(path), "--top", "2"]) == 0
    assert capsys.readouterr().out == (
        "words: 6\n"
        "characters: 11\n"
        "characters (no spaces): 6\n"
        "top words:\n"
        "  b: 3\n"
        "  a: 2\n"
    )


def test_default_lists_three_top_words(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("d c b a d c b d", encoding="utf-8")

    assert main([str(path)]) == 0
    assert capsys.readouterr().out == (
        "words: 8\n"
        "characters: 15\n"
        "characters (no spaces): 8\n"
        "top words:\n"
        "  d: 3\n"
        "  b: 2\n"
        "  c: 2\n"
    )


def test_file_is_read_as_utf8(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "accents.txt"
    path.write_text("café café", encoding="utf-8")

    assert main([str(path)]) == 0
    assert "characters: 9\n" in capsys.readouterr().out


def test_missing_file_prints_error_and_returns_one(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(tmp_path / "missing.txt")]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_directory_prints_error_and_returns_one(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(tmp_path)]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_non_utf8_file_prints_error_and_returns_one(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "binary.txt"
    path.write_bytes(b"\xff\xfe\xfa")

    assert main([str(path)]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_negative_top_is_rejected_before_file_is_read(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    missing = tmp_path / "missing.txt"

    with pytest.raises(SystemExit) as excinfo:
        main([str(missing), "--top", "-1"])
    assert excinfo.value.code == 2
    assert "usage: textstats" in capsys.readouterr().err


def test_non_integer_top_is_rejected(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("a b", encoding="utf-8")

    with pytest.raises(SystemExit) as excinfo:
        main([str(path), "--top", "abc"])
    assert excinfo.value.code == 2
    assert "usage: textstats" in capsys.readouterr().err


def test_python_m_textstats_prints_report_for_file(tmp_path: Path) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("the cat the a cat the", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == format_report("the cat the a cat the") + "\n"
