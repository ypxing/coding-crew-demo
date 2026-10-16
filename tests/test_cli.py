import subprocess
import sys
from pathlib import Path

import pytest

from textstats import format_report
from textstats.__main__ import main


def test_main_prints_report_for_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
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
    text = "a b c d e a b c a"
    path = tmp_path / "sample.txt"
    path.write_text(text, encoding="utf-8")

    assert main([str(path)]) == 0

    out = capsys.readouterr().out
    assert out.splitlines()[4:] == ["  a: 3", "  b: 2", "  c: 2"]


def test_module_runs_as_script(tmp_path: Path) -> None:
    text = "the cat the a cat the"
    path = tmp_path / "sample.txt"
    path.write_text(text, encoding="utf-8")

    proc = subprocess.run(
        [sys.executable, "-m", "textstats", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert proc.returncode == 0
    assert proc.stdout == format_report(text) + "\n"


def test_main_reads_file_as_utf8(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    text = "naïve café ☕ the the"
    path = tmp_path / "sample.txt"
    path.write_bytes(text.encode("utf-8"))

    assert main([str(path)]) == 0

    assert capsys.readouterr().out == format_report(text) + "\n"


def test_main_counts_crlf_line_endings_as_characters(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    text = "the cat\r\nthe a\r\n"
    path = tmp_path / "crlf.txt"
    path.write_bytes(text.encode("utf-8"))

    assert main([str(path)]) == 0

    assert capsys.readouterr().out == format_report(text) + "\n"
    assert format_report(text).splitlines()[1] == "characters: 16"


def test_main_missing_file_reports_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(tmp_path / "missing.txt")]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")
    assert "Traceback" not in captured.err


def test_main_directory_reports_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(tmp_path)]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_main_invalid_utf8_reports_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "bad.txt"
    path.write_bytes(b"\xff\xfe\xfa")

    assert main([str(path)]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_main_rejects_negative_top_before_reading(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    # The file does not exist: a read would exit 1, so exit 2 proves it was never read.
    with pytest.raises(SystemExit) as excinfo:
        main([str(tmp_path / "missing.txt"), "--top", "-1"])

    assert excinfo.value.code == 2
    assert "usage:" in capsys.readouterr().err


def test_main_rejects_non_integer_top(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("the cat", encoding="utf-8")

    with pytest.raises(SystemExit) as excinfo:
        main([str(path), "--top", "abc"])

    assert excinfo.value.code == 2
