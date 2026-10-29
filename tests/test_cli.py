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
    source = tmp_path / "sample.txt"
    source.write_text("the cat the a cat the", encoding="utf-8")

    assert main([str(source)]) == 0

    assert capsys.readouterr().out == format_report("the cat the a cat the") + "\n"


def test_main_top_option_limits_top_words(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "sample.txt"
    source.write_text("the cat the a cat the dog", encoding="utf-8")

    assert main([str(source), "--top", "2"]) == 0

    assert capsys.readouterr().out == format_report("the cat the a cat the dog", n=2) + "\n"


def test_main_lists_three_top_words_without_top_option(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "sample.txt"
    source.write_text("the cat the a cat the dog", encoding="utf-8")

    assert main([str(source)]) == 0

    assert capsys.readouterr().out == format_report("the cat the a cat the dog", n=3) + "\n"


def test_module_runs_as_script_and_prints_report(tmp_path: Path) -> None:
    source = tmp_path / "sample.txt"
    source.write_text("the cat the a cat the", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(source)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == format_report("the cat the a cat the") + "\n"


def test_main_reports_missing_file_as_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    missing = tmp_path / "missing.txt"

    assert main([str(missing)]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_main_reports_directory_as_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(tmp_path)]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_main_reports_invalid_utf8_as_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "binary.txt"
    source.write_bytes(b"\xff\xfe\xfa")

    assert main([str(source)]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_main_rejects_negative_top_before_reading_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "sample.txt"
    source.write_text("the cat", encoding="utf-8")

    with pytest.raises(SystemExit) as excinfo:
        main([str(source), "--top", "-1"])

    assert excinfo.value.code == 2
    assert "usage:" in capsys.readouterr().err


def test_main_rejects_non_integer_top(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "sample.txt"
    source.write_text("the cat", encoding="utf-8")

    with pytest.raises(SystemExit) as excinfo:
        main([str(source), "--top", "abc"])

    assert excinfo.value.code == 2


def test_module_decodes_file_as_utf8_under_ascii_locale(tmp_path: Path) -> None:
    source = tmp_path / "accents.txt"
    source.write_bytes("café naïve".encode())
    env = {
        **os.environ,
        "LC_ALL": "C",
        "PYTHONUTF8": "0",
        "PYTHONCOERCECLOCALE": "0",
    }

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(source)],
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )

    assert result.returncode == 0
    assert "characters: 10\n" in result.stdout
