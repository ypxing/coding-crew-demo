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
    path = tmp_path / "doc.txt"
    path.write_text("the cat the a cat the", encoding="utf-8")

    assert main([str(path)]) == 0
    assert capsys.readouterr().out == format_report("the cat the a cat the") + "\n"


def test_main_top_limits_top_words(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "doc.txt"
    path.write_text("the cat the a cat the", encoding="utf-8")

    assert main([str(path), "--top", "2"]) == 0
    assert capsys.readouterr().out == format_report("the cat the a cat the", n=2) + "\n"


def test_main_defaults_to_three_top_words(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "doc.txt"
    path.write_text("a a b b c c d", encoding="utf-8")

    assert main([str(path)]) == 0
    assert capsys.readouterr().out == format_report("a a b b c c d", n=3) + "\n"


def test_python_m_textstats_runs_the_cli(tmp_path: Path) -> None:
    path = tmp_path / "doc.txt"
    path.write_text("the cat the a cat the", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == format_report("the cat the a cat the") + "\n"


def test_main_decodes_file_as_utf8_under_non_utf8_locale(tmp_path: Path) -> None:
    path = tmp_path / "doc.txt"
    path.write_bytes("café the".encode())
    # ASCII locale with UTF-8 mode off: open() without encoding="utf-8" would fail here.
    # PYTHONIOENCODING keeps the child's stdout printable so only decoding is under test.
    env = {
        **os.environ,
        "LC_ALL": "C",
        "LANG": "C",
        "PYTHONCOERCECLOCALE": "0",
        "PYTHONUTF8": "0",
        "PYTHONIOENCODING": "utf-8",
    }

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(path)],
        capture_output=True,
        check=False,
        env=env,
    )

    assert result.returncode == 0
    assert result.stdout == (format_report("café the") + "\n").encode("utf-8")


def test_main_reports_missing_file_as_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(tmp_path / "missing.txt")]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")
    assert "Traceback" not in captured.err


def test_main_reports_directory_as_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(tmp_path)]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")
    assert "Traceback" not in captured.err


def test_main_reports_non_utf8_file_as_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "doc.txt"
    path.write_bytes(b"\xff\xfe\xfa")

    assert main([str(path)]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")
    assert "Traceback" not in captured.err


def test_main_rejects_negative_top_before_reading_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main([str(tmp_path / "missing.txt"), "--top", "-1"])

    assert exc_info.value.code == 2
    assert "usage: textstats" in capsys.readouterr().err


def test_main_rejects_non_integer_top(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "doc.txt"
    path.write_text("the cat the a cat the", encoding="utf-8")

    with pytest.raises(SystemExit) as exc_info:
        main([str(path), "--top", "abc"])

    assert exc_info.value.code == 2
    assert "usage: textstats" in capsys.readouterr().err
