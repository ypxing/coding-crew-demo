import builtins
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

import textstats.__main__ as cli_module
from textstats import format_report
from textstats.__main__ import main


def test_python_m_textstats_prints_report_for_file(tmp_path: Path) -> None:
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


def test_top_option_limits_top_words(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("the cat the a cat the", encoding="utf-8")

    assert main([str(path), "--top", "2"]) == 0
    assert capsys.readouterr().out == format_report("the cat the a cat the", n=2) + "\n"


def test_default_lists_three_top_words(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("a b c d e", encoding="utf-8")

    assert main([str(path)]) == 0
    top_lines = [line for line in capsys.readouterr().out.splitlines() if line.startswith("  ")]
    assert top_lines == ["  a: 1", "  b: 1", "  c: 1"]


def test_file_is_decoded_as_utf8(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    text = "café naïve ümlaut"
    path = tmp_path / "sample.txt"
    path.write_bytes(text.encode("utf-8"))
    real_open: Callable[..., Any] = builtins.open

    def ascii_locale_open(
        file: Any, mode: str = "r", *args: Any, encoding: str | None = None, **kwargs: Any
    ) -> Any:
        # Stands in for a non-UTF-8 locale: open() without an encoding decodes as ASCII.
        return real_open(file, mode, *args, encoding=encoding or "ascii", **kwargs)

    monkeypatch.setattr(cli_module, "open", ascii_locale_open, raising=False)

    assert main([str(path)]) == 0
    assert capsys.readouterr().out == format_report(text) + "\n"


def test_missing_file_reports_error_and_returns_1(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(tmp_path / "missing.txt")]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_directory_reports_error_and_returns_1(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(tmp_path)]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_invalid_utf8_reports_error_and_returns_1(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "binary.txt"
    path.write_bytes(b"\xff\xfe\xfa")

    assert main([str(path)]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_negative_top_is_rejected_by_argparse(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("a b c", encoding="utf-8")

    with pytest.raises(SystemExit) as exc:
        main([str(path), "--top", "-1"])
    assert exc.value.code == 2
    assert "usage:" in capsys.readouterr().err


def test_non_integer_top_is_rejected_by_argparse(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("a b c", encoding="utf-8")

    with pytest.raises(SystemExit) as exc:
        main([str(path), "--top", "abc"])
    assert exc.value.code == 2
    assert "usage:" in capsys.readouterr().err
