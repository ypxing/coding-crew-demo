import subprocess
import sys
from pathlib import Path

import pytest

from textstats import format_report
from textstats.__main__ import main


def test_main_prints_report_for_utf8_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    text = "the cat the a cat the"
    path = tmp_path / "sample.txt"
    path.write_text(text, encoding="utf-8")

    assert main([str(path)]) == 0
    assert capsys.readouterr().out == format_report(text) + "\n"


def test_main_top_limits_top_words(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    text = "the cat the a cat the"
    path = tmp_path / "sample.txt"
    path.write_text(text, encoding="utf-8")

    assert main([str(path), "--top", "2"]) == 0
    assert capsys.readouterr().out == format_report(text, n=2) + "\n"


def test_main_defaults_to_three_top_words(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    text = "a b c d d d c c b b b a a a a"
    path = tmp_path / "sample.txt"
    path.write_text(text, encoding="utf-8")

    assert main([str(path)]) == 0
    assert capsys.readouterr().out == format_report(text, n=3) + "\n"


def test_main_reads_utf8_regardless_of_locale(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    text = "café naïve résumé café"
    path = tmp_path / "sample.txt"
    path.write_bytes(text.encode("utf-8"))

    assert main([str(path)]) == 0
    assert capsys.readouterr().out == format_report(text) + "\n"


def test_module_runs_as_script(tmp_path: Path) -> None:
    text = "the cat the a cat the"
    path = tmp_path / "sample.txt"
    path.write_text(text, encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == format_report(text) + "\n"


def test_main_missing_file_reports_error_and_returns_1(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    missing = tmp_path / "missing.txt"

    assert main([str(missing)]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")
    assert "Traceback" not in captured.err


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
    path = tmp_path / "binary.txt"
    path.write_bytes(b"\xff\xfe\xfa")

    assert main([str(path)]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_main_negative_top_is_rejected_before_reading_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    missing = tmp_path / "missing.txt"

    with pytest.raises(SystemExit) as excinfo:
        main([str(missing), "--top", "-1"])

    assert excinfo.value.code == 2
    assert "error:" in capsys.readouterr().err


def test_main_non_integer_top_is_rejected(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("the cat", encoding="utf-8")

    with pytest.raises(SystemExit) as excinfo:
        main([str(path), "--top", "abc"])

    assert excinfo.value.code == 2
    assert "error:" in capsys.readouterr().err
