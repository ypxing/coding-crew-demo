import subprocess
import sys
from pathlib import Path

import pytest
from pytest import CaptureFixture

from textstats import format_report
from textstats.__main__ import main

SAMPLE = "the cat the a cat the b c d\n"


def test_main_prints_report_and_returns_zero(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
    path = tmp_path / "sample.txt"
    path.write_text(SAMPLE, encoding="utf-8")

    assert main([str(path)]) == 0

    out = capsys.readouterr().out
    assert out == format_report(SAMPLE) + "\n"


def test_main_top_option_limits_top_words(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
    path = tmp_path / "sample.txt"
    path.write_text(SAMPLE, encoding="utf-8")

    assert main([str(path), "--top", "2"]) == 0

    out = capsys.readouterr().out
    assert out == format_report(SAMPLE, n=2) + "\n"
    assert out.endswith("top words:\n  the: 3\n  cat: 2\n")


def test_main_defaults_to_three_top_words(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
    path = tmp_path / "sample.txt"
    path.write_text(SAMPLE, encoding="utf-8")

    assert main([str(path)]) == 0

    out = capsys.readouterr().out
    top_lines = out.split("top words:\n", 1)[1].splitlines()
    assert top_lines == ["  the: 3", "  cat: 2", "  a: 1"]


def test_main_reads_file_as_utf8(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
    text = "café naïve déjà vu\n"
    path = tmp_path / "unicode.txt"
    path.write_bytes(text.encode("utf-8"))

    assert main([str(path)]) == 0

    out = capsys.readouterr().out
    assert out == format_report(text) + "\n"


def test_python_m_textstats_runs_as_subprocess(tmp_path: Path) -> None:
    path = tmp_path / "sample.txt"
    path.write_text(SAMPLE, encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == format_report(SAMPLE) + "\n"


def test_main_missing_file_reports_error_and_returns_one(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    assert main([str(tmp_path / "missing.txt")]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_main_directory_reports_error_and_returns_one(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    assert main([str(tmp_path)]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_main_non_utf8_file_reports_error_and_returns_one(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    path = tmp_path / "binary.txt"
    path.write_bytes(b"\xff\xfe\xfa")

    assert main([str(path)]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_main_negative_top_is_usage_error(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
    path = tmp_path / "sample.txt"
    path.write_text(SAMPLE, encoding="utf-8")

    with pytest.raises(SystemExit) as excinfo:
        main([str(path), "--top", "-1"])

    assert excinfo.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "usage: textstats" in captured.err


def test_main_non_integer_top_is_usage_error(tmp_path: Path) -> None:
    path = tmp_path / "sample.txt"
    path.write_text(SAMPLE, encoding="utf-8")

    with pytest.raises(SystemExit) as excinfo:
        main([str(path), "--top", "abc"])

    assert excinfo.value.code == 2
