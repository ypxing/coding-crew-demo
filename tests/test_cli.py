import os
import subprocess
import sys
from pathlib import Path

import pytest

from textstats import format_report
from textstats.__main__ import main

TEXT = "the cat the a cat the dog"


def test_main_prints_report_with_default_top_three_and_returns_zero(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "in.txt"
    path.write_text(TEXT, encoding="utf-8")

    assert main([str(path)]) == 0

    out = capsys.readouterr().out
    assert out == format_report(TEXT) + "\n"
    assert out.endswith("top words:\n  the: 3\n  cat: 2\n  a: 1\n")


def test_main_top_option_limits_top_words(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "in.txt"
    path.write_text(TEXT, encoding="utf-8")

    assert main([str(path), "--top", "2"]) == 0

    assert capsys.readouterr().out.endswith("top words:\n  the: 3\n  cat: 2\n")


def test_python_dash_m_textstats_prints_report(tmp_path: Path) -> None:
    path = tmp_path / "in.txt"
    path.write_text(TEXT, encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == format_report(TEXT) + "\n"


def test_file_is_decoded_as_utf8_under_a_non_utf8_locale(tmp_path: Path) -> None:
    text = "café naïve café"
    path = tmp_path / "in.txt"
    path.write_bytes(text.encode("utf-8"))
    # C locale with UTF-8 mode and locale coercion off makes the default encoding ASCII.
    env = {
        **os.environ,
        "LC_ALL": "C",
        "PYTHONUTF8": "0",
        "PYTHONCOERCECLOCALE": "0",
        "PYTHONIOENCODING": "utf-8",
    }

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(path)],
        capture_output=True,
        env=env,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout.decode("utf-8") == format_report(text) + "\n"


def test_missing_file_reports_error_on_stderr_and_returns_one(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(tmp_path / "missing.txt")]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error: ")
    assert "Traceback" not in captured.err


def test_directory_path_reports_error_on_stderr_and_returns_one(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(tmp_path)]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error: ")


def test_invalid_utf8_file_reports_error_on_stderr_and_returns_one(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "in.txt"
    path.write_bytes(b"\xff\xfe\xfa")

    assert main([str(path)]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error: ")
