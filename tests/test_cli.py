import subprocess
import sys
from pathlib import Path

import pytest

from textstats.__main__ import main


def test_main_prints_report_for_utf8_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "doc.txt"
    path.write_text("the cat the a cat the dog", encoding="utf-8")

    assert main([str(path)]) == 0

    assert capsys.readouterr().out == (
        "words: 7\n"
        "characters: 25\n"
        "characters (no spaces): 19\n"
        "top words:\n"
        "  the: 3\n"
        "  cat: 2\n"
        "  a: 1\n"
    )


def test_main_top_limits_top_words(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "doc.txt"
    path.write_text("the cat the a cat the dog", encoding="utf-8")

    assert main([str(path), "--top", "2"]) == 0

    assert capsys.readouterr().out == (
        "words: 7\n"
        "characters: 25\n"
        "characters (no spaces): 19\n"
        "top words:\n"
        "  the: 3\n"
        "  cat: 2\n"
    )


def test_python_m_textstats_prints_report_and_exits_zero(tmp_path: Path) -> None:
    path = tmp_path / "doc.txt"
    path.write_text("the cat the a cat the dog", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == (
        "words: 7\n"
        "characters: 25\n"
        "characters (no spaces): 19\n"
        "top words:\n"
        "  the: 3\n"
        "  cat: 2\n"
        "  a: 1\n"
    )
