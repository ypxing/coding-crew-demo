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
