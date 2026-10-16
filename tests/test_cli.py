import subprocess
import sys
from pathlib import Path

import pytest

from textstats import format_report
from textstats.__main__ import main


def test_main_prints_report_for_utf8_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "in.txt"
    path.write_text("the cat the a cat the", encoding="utf-8")

    assert main([str(path)]) == 0

    assert capsys.readouterr().out == format_report("the cat the a cat the") + "\n"


def test_main_top_option_limits_top_words(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "in.txt"
    path.write_text("the cat the a cat the", encoding="utf-8")

    assert main([str(path), "--top", "2"]) == 0

    assert capsys.readouterr().out == format_report("the cat the a cat the", n=2) + "\n"


def test_main_missing_file_reports_error_and_returns_1(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(tmp_path / "nope.txt")]) == 1

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


def test_main_invalid_utf8_reports_error_and_returns_1(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "bad.bin"
    path.write_bytes(b"\xff\xfe\xfa")

    assert main([str(path)]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_main_negative_top_is_usage_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "in.txt"
    path.write_text("a b", encoding="utf-8")

    with pytest.raises(SystemExit) as exc:
        main([str(path), "--top", "-1"])

    assert exc.value.code == 2
    assert "usage" in capsys.readouterr().err


def test_main_non_integer_top_is_usage_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "in.txt"
    path.write_text("a b", encoding="utf-8")

    with pytest.raises(SystemExit) as exc:
        main([str(path), "--top", "abc"])

    assert exc.value.code == 2
    assert "usage" in capsys.readouterr().err


def test_python_m_textstats_runs_report(tmp_path: Path) -> None:
    path = tmp_path / "in.txt"
    path.write_text("the cat the a cat the", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == format_report("the cat the a cat the") + "\n"
