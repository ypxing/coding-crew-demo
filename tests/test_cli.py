import os
import subprocess
import sys
from pathlib import Path

import pytest

from textstats import format_report
from textstats.__main__ import main

TEXT = "the cat the a cat the dog"


def _write(tmp_path: Path, text: str = TEXT) -> str:
    path = tmp_path / "input.txt"
    path.write_text(text, encoding="utf-8")
    return str(path)


def test_main_prints_report_and_returns_zero(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([_write(tmp_path)]) == 0
    assert capsys.readouterr().out == format_report(TEXT) + "\n"


def test_main_top_limits_top_words(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([_write(tmp_path), "--top", "2"]) == 0
    out = capsys.readouterr().out
    assert out == format_report(TEXT, n=2) + "\n"
    assert out.endswith("top words:\n  the: 3\n  cat: 2\n")


def test_main_defaults_to_three_top_words(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([_write(tmp_path)]) == 0
    top_section = capsys.readouterr().out.split("top words:\n")[1]
    assert top_section == "  the: 3\n  cat: 2\n  a: 1\n"


def test_python_dash_m_textstats_prints_report(tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "textstats", _write(tmp_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert result.stdout == format_report(TEXT) + "\n"


def test_file_is_decoded_as_utf8_under_ascii_locale(tmp_path: Path) -> None:
    text = "café naïve café"
    env = {**os.environ, "LC_ALL": "C", "PYTHONUTF8": "0", "PYTHONCOERCECLOCALE": "0"}
    result = subprocess.run(
        [sys.executable, "-m", "textstats", _write(tmp_path, text)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout == format_report(text) + "\n"


def test_missing_file_reports_error_and_returns_one(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(tmp_path / "missing.txt")]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error: ")
    assert "Traceback" not in captured.err
