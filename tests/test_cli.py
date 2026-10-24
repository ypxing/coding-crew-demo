import os
import subprocess
import sys
from pathlib import Path

import pytest

from textstats import format_report
from textstats.__main__ import main


def test_main_prints_report_for_utf8_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
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


def _run_cli_under_c_locale(path: Path) -> subprocess.CompletedProcess[str]:
    env = {**os.environ, "LC_ALL": "C", "LANG": "C", "PYTHONUTF8": "0", "PYTHONCOERCECLOCALE": "0"}
    return subprocess.run(
        [sys.executable, "-m", "textstats", str(path)],
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )


def test_python_m_textstats_prints_report(tmp_path: Path) -> None:
    source = tmp_path / "doc.txt"
    source.write_text("the cat the a cat the", encoding="utf-8")

    result = _run_cli_under_c_locale(source)

    assert result.returncode == 0
    assert result.stdout == format_report("the cat the a cat the") + "\n"


def test_main_reads_utf8_regardless_of_locale(tmp_path: Path) -> None:
    text = "café naïve café"
    source = tmp_path / "doc.txt"
    source.write_bytes(text.encode("utf-8"))

    result = _run_cli_under_c_locale(source)

    assert result.returncode == 0
    assert result.stdout == format_report(text) + "\n"


def test_main_missing_file_reports_error_and_returns_1(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(tmp_path / "missing.txt")]) == 1

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


def test_main_non_utf8_file_reports_error_and_returns_1(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "doc.bin"
    source.write_bytes(b"\xff\xfe\xfa")

    assert main([str(source)]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_main_rejects_negative_top_before_reading_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as excinfo:
        main([str(tmp_path / "missing.txt"), "--top", "-1"])

    assert excinfo.value.code == 2
    assert "usage" in capsys.readouterr().err.lower()


def test_main_rejects_non_integer_top(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "doc.txt"
    source.write_text("the cat", encoding="utf-8")

    with pytest.raises(SystemExit) as excinfo:
        main([str(source), "--top", "abc"])

    assert excinfo.value.code == 2
