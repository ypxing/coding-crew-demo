import subprocess
import sys
from pathlib import Path

import pytest

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


def test_file_is_decoded_as_utf8(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    text = "café naïve ümlaut"
    path = tmp_path / "sample.txt"
    path.write_bytes(text.encode("utf-8"))

    assert main([str(path)]) == 0
    assert capsys.readouterr().out == format_report(text) + "\n"
