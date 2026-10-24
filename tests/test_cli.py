import os
import subprocess
import sys
from pathlib import Path

import pytest

from textstats import format_report
from textstats.__main__ import main


def test_main_prints_report_for_utf8_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "doc.txt"
    source.write_text("the cat the a cat the", encoding="utf-8")

    assert main([str(source)]) == 0
    assert capsys.readouterr().out == format_report("the cat the a cat the") + "\n"


def test_main_top_limits_top_words(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    source = tmp_path / "doc.txt"
    source.write_text("the cat the a cat the", encoding="utf-8")

    assert main([str(source), "--top", "2"]) == 0
    assert capsys.readouterr().out == format_report("the cat the a cat the", n=2) + "\n"


def test_main_defaults_to_three_top_words(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "doc.txt"
    source.write_text("one two three four four", encoding="utf-8")

    assert main([str(source)]) == 0
    top_lines = capsys.readouterr().out.splitlines()[4:]
    assert top_lines == ["  four: 2", "  one: 1", "  three: 1"]


def _run_cli_under_c_locale(path: Path) -> subprocess.CompletedProcess[str]:
    env = {**os.environ, "LC_ALL": "C", "LANG": "C", "PYTHONUTF8": "0", "PYTHONCOERCECLOCALE": "0"}
    return subprocess.run(
        [sys.executable, "-m", "textstats", str(path)],
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )


def test_python_m_textstats_prints_report(tmp_path: Path) -> None:
    source = tmp_path / "doc.txt"
    source.write_text("the cat the a cat the", encoding="utf-8")

    result = _run_cli_under_c_locale(source)

    assert result.returncode == 0
    assert result.stdout == format_report("the cat the a cat the") + "\n"


def test_main_reads_utf8_regardless_of_locale(tmp_path: Path) -> None:
    text = "café naïve café"
    source = tmp_path / "doc.txt"
    source.write_bytes(text.encode("utf-8"))

    result = _run_cli_under_c_locale(source)

    assert result.returncode == 0
    assert result.stdout == format_report(text) + "\n"
