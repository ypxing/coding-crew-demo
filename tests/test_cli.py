import subprocess
import sys
from pathlib import Path

import pytest

from textstats import format_report
from textstats.__main__ import main


def test_main_prints_report_for_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "doc.txt"
    path.write_text("the cat the a cat the", encoding="utf-8")

    assert main([str(path)]) == 0

    assert capsys.readouterr().out == format_report("the cat the a cat the") + "\n"


def test_main_limits_top_words_with_top_option(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "doc.txt"
    path.write_text("a b c d b c d d", encoding="utf-8")

    assert main([str(path), "--top", "2"]) == 0

    assert capsys.readouterr().out == format_report("a b c d b c d d", n=2) + "\n"


def test_main_lists_three_top_words_by_default(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "doc.txt"
    path.write_text("a b c d b c d d", encoding="utf-8")

    assert main([str(path)]) == 0

    assert capsys.readouterr().out.splitlines()[-3:] == ["  d: 3", "  b: 2", "  c: 2"]


def test_main_reads_file_as_utf8(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "doc.txt"
    path.write_bytes("café café".encode())

    assert main([str(path)]) == 0

    assert capsys.readouterr().out.splitlines()[:2] == ["words: 2", "characters: 9"]


def test_python_m_textstats_runs_as_subprocess(tmp_path: Path) -> None:
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
