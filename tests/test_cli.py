import os
import subprocess
import sys
from pathlib import Path

import pytest

from textstats import format_report
from textstats.__main__ import main


def test_main_prints_report_for_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    contents = "the cat the a cat the dog"
    path = tmp_path / "input.txt"
    path.write_text(contents, encoding="utf-8")

    assert main([str(path)]) == 0
    assert capsys.readouterr().out == format_report(contents) + "\n"


def test_main_top_limits_top_words(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "input.txt"
    path.write_text("d c b a d c b d c d", encoding="utf-8")

    assert main([str(path), "--top", "2"]) == 0
    assert capsys.readouterr().out.endswith("top words:\n  d: 4\n  c: 3\n")


def test_main_lists_three_top_words_by_default(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "input.txt"
    path.write_text("d c b a d c b d c d", encoding="utf-8")

    assert main([str(path)]) == 0
    assert capsys.readouterr().out.endswith("top words:\n  d: 4\n  c: 3\n  b: 2\n")


def test_python_m_textstats_prints_report(tmp_path: Path) -> None:
    contents = "the cat the a cat the dog"
    path = tmp_path / "input.txt"
    path.write_text(contents, encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    assert result.returncode == 0
    assert result.stdout == format_report(contents) + "\n"


def test_python_m_textstats_reads_utf8_under_ascii_locale(tmp_path: Path) -> None:
    contents = "café naïve café — déjà vu"
    path = tmp_path / "input.txt"
    path.write_text(contents, encoding="utf-8")
    # A C locale with coercion and UTF-8 mode off makes the default text encoding ASCII.
    env = {
        **os.environ,
        "LC_ALL": "C",
        "LANG": "C",
        "PYTHONCOERCECLOCALE": "0",
        "PYTHONUTF8": "0",
        "PYTHONIOENCODING": "utf-8",
    }

    result = subprocess.run(
        [sys.executable, "-X", "utf8=0", "-m", "textstats", str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout == format_report(contents) + "\n"


def test_main_reports_missing_file_as_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(tmp_path / "missing.txt")]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")
    assert "Traceback" not in captured.err
