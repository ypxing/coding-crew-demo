import os
import subprocess
import sys
from pathlib import Path

import pytest

from textstats import format_report
from textstats.__main__ import main


def test_main_prints_report_for_file_and_returns_zero(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    text = "the cat the a cat the dog"
    path = tmp_path / "input.txt"
    path.write_text(text, encoding="utf-8")

    assert main([str(path)]) == 0

    captured = capsys.readouterr()
    assert captured.out == format_report(text) + "\n"
    assert captured.err == ""


def test_main_top_limits_report_to_n_words(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    text = "the cat the a cat the dog"
    path = tmp_path / "input.txt"
    path.write_text(text, encoding="utf-8")

    assert main([str(path), "--top", "2"]) == 0

    out = capsys.readouterr().out
    assert out == format_report(text, n=2) + "\n"
    assert out.endswith("top words:\n  the: 3\n  cat: 2\n")


def test_main_without_top_lists_three_words(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "input.txt"
    path.write_text("d c c b b b a a a a", encoding="utf-8")

    assert main([str(path)]) == 0

    out = capsys.readouterr().out
    assert out.endswith("top words:\n  a: 4\n  b: 3\n  c: 2\n")


def test_python_m_textstats_prints_report(tmp_path: Path) -> None:
    text = "the cat the a cat the dog"
    path = tmp_path / "input.txt"
    path.write_text(text, encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    assert result.returncode == 0
    assert result.stdout == format_report(text) + "\n"


def test_python_m_textstats_decodes_utf8_regardless_of_locale(tmp_path: Path) -> None:
    text = "naïve café — déjà vu"
    path = tmp_path / "input.txt"
    path.write_text(text, encoding="utf-8")
    # An ASCII locale with coercion and UTF-8 mode off makes the default encoding non-UTF-8.
    env = {
        **os.environ,
        "LC_ALL": "C",
        "PYTHONCOERCECLOCALE": "0",
        "PYTHONUTF8": "0",
        "PYTHONIOENCODING": "utf-8",
    }

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout == format_report(text) + "\n"
