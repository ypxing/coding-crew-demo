import subprocess
import sys
from pathlib import Path

import pytest

from textstats import format_report
from textstats.__main__ import main

TEXT = "the cat the a cat the dog"


def test_main_prints_report_with_default_top_three_and_returns_zero(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "in.txt"
    path.write_text(TEXT, encoding="utf-8")

    assert main([str(path)]) == 0

    out = capsys.readouterr().out
    assert out == format_report(TEXT) + "\n"
    assert out.endswith("top words:\n  the: 3\n  cat: 2\n  a: 1\n")


def test_main_top_option_limits_top_words(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "in.txt"
    path.write_text(TEXT, encoding="utf-8")

    assert main([str(path), "--top", "2"]) == 0

    assert capsys.readouterr().out.endswith("top words:\n  the: 3\n  cat: 2\n")


def test_python_dash_m_textstats_prints_report(tmp_path: Path) -> None:
    path = tmp_path / "in.txt"
    path.write_text(TEXT, encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == format_report(TEXT) + "\n"
