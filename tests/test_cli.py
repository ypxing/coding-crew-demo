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
