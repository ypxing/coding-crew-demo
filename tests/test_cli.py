import subprocess
import sys
from pathlib import Path

import pytest

from textstats import format_report
from textstats.__main__ import main


def test_main_prints_report_for_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    path = tmp_path / "doc.txt"
    path.write_text("the cat the a cat the", encoding="utf-8")

    assert main([str(path)]) == 0

    out = capsys.readouterr().out
    assert out == format_report("the cat the a cat the") + "\n"


def test_main_top_option_limits_top_words(
    tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    path = tmp_path / "doc.txt"
    path.write_text("the cat the a cat the", encoding="utf-8")

    assert main([str(path), "--top", "2"]) == 0

    out = capsys.readouterr().out
    assert out.splitlines()[4:] == ["  the: 3", "  cat: 2"]


def test_main_defaults_to_three_top_words(
    tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    path = tmp_path / "doc.txt"
    path.write_text("a b c d e", encoding="utf-8")

    assert main([str(path)]) == 0

    out = capsys.readouterr().out
    assert out.splitlines()[4:] == ["  a: 1", "  b: 1", "  c: 1"]


def test_main_reads_file_as_utf8(
    tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    path = tmp_path / "doc.txt"
    path.write_bytes("café naïve".encode())

    assert main([str(path)]) == 0

    out = capsys.readouterr().out
    assert out.splitlines()[1] == "characters: 10"


def test_module_runs_as_subprocess(tmp_path: Path) -> None:
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
