import locale
import subprocess
import sys
from pathlib import Path

import pytest
from pytest import CaptureFixture

from textstats import format_report
from textstats.__main__ import main


def test_main_prints_report_for_utf8_file(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("the cat the a cat the", encoding="utf-8")

    code = main([str(path)])

    assert code == 0
    assert capsys.readouterr().out == format_report("the cat the a cat the") + "\n"


def test_main_top_option_limits_top_words(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("the cat the a cat the", encoding="utf-8")

    code = main([str(path), "--top", "2"])

    assert code == 0
    assert capsys.readouterr().out == format_report("the cat the a cat the", n=2) + "\n"


def test_main_defaults_to_three_top_words(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("a b c d d d e e", encoding="utf-8")

    main([str(path)])

    top_lines = capsys.readouterr().out.splitlines()[4:]
    assert top_lines == ["  d: 3", "  e: 2", "  a: 1"]


def test_python_m_textstats_runs_as_subprocess(tmp_path: Path) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("the cat the a cat the", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == format_report("the cat the a cat the") + "\n"


def test_main_missing_file_reports_error_and_returns_1(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    code = main([str(tmp_path / "missing.txt")])

    captured = capsys.readouterr()
    assert code == 1
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_main_directory_reports_error_and_returns_1(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    code = main([str(tmp_path)])

    captured = capsys.readouterr()
    assert code == 1
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_main_invalid_utf8_reports_error_and_returns_1(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    path = tmp_path / "binary.txt"
    path.write_bytes(b"\xff\xfe\xfa")

    code = main([str(path)])

    captured = capsys.readouterr()
    assert code == 1
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_main_non_integer_top_is_usage_error(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("a b", encoding="utf-8")

    with pytest.raises(SystemExit) as exc_info:
        main([str(path), "--top", "abc"])

    assert exc_info.value.code == 2
    assert "usage: textstats" in capsys.readouterr().err


def test_main_negative_top_is_usage_error_before_reading_file(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main([str(tmp_path / "missing.txt"), "--top", "-1"])

    assert exc_info.value.code == 2
    assert "usage: textstats" in capsys.readouterr().err


def test_main_decodes_file_as_utf8_regardless_of_locale(
    tmp_path: Path, capsys: CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(locale, "getpreferredencoding", lambda do_setlocale=True: "ascii")
    path = tmp_path / "sample.txt"
    path.write_text("café naïve", encoding="utf-8")

    code = main([str(path)])

    assert code == 0
    assert capsys.readouterr().out == format_report("café naïve") + "\n"
