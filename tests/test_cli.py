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


def test_python_m_textstats_prints_report_and_exits_zero(tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "textstats", _write(tmp_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert result.stdout == format_report(TEXT) + "\n"


def test_python_m_textstats_decodes_utf8_under_ascii_locale(tmp_path: Path) -> None:
    text = "café naïve café"
    # C locale with coercion and UTF-8 mode off makes the default encoding ASCII.
    env = {
        **os.environ,
        "LC_ALL": "C",
        "PYTHONCOERCECLOCALE": "0",
        "PYTHONUTF8": "0",
        "PYTHONIOENCODING": "utf-8",
    }
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


def test_main_missing_file_reports_error_and_returns_one(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(tmp_path / "missing.txt")]) == 1
    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith("textstats: error:")
    assert "Traceback" not in err


def test_main_directory_reports_error_and_returns_one(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(tmp_path)]) == 1
    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith("textstats: error:")


def test_main_invalid_utf8_reports_error_and_returns_one(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "binary.txt"
    path.write_bytes(b"\xff\xfe\xfa")
    assert main([str(path)]) == 1
    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith("textstats: error:")
