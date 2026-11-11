import os
import subprocess
import sys
from pathlib import Path

import pytest

from textstats import format_report
from textstats.__main__ import main


def test_module_run_prints_report_and_exits_zero(tmp_path: Path) -> None:
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


def test_main_top_limits_listed_words(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    source = tmp_path / "sample.txt"
    source.write_text("the cat the a cat the", encoding="utf-8")

    assert main([str(source), "--top", "2"]) == 0

    assert capsys.readouterr().out == format_report("the cat the a cat the", n=2) + "\n"


def test_main_lists_three_top_words_by_default(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "sample.txt"
    source.write_text("d d c c b b a", encoding="utf-8")

    assert main([str(source)]) == 0

    assert capsys.readouterr().out.split("\n")[4:7] == ["  b: 2", "  c: 2", "  d: 2"]


def test_module_run_reads_utf8_under_ascii_locale(tmp_path: Path) -> None:
    source = tmp_path / "sample.txt"
    source.write_text("café café", encoding="utf-8")
    env = {"PATH": os.environ["PATH"], "LC_ALL": "C", "PYTHONCOERCECLOCALE": "0", "PYTHONUTF8": "0"}

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(source)],
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )

    assert result.returncode == 0
    assert "characters: 9\n" in result.stdout
