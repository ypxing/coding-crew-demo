import subprocess
import sys
from pathlib import Path

import pytest

from textstats import format_report
from textstats.__main__ import main


def test_main_prints_report_for_utf8_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "sample.txt"
    source.write_text("the cat the a cat the", encoding="utf-8")

    assert main([str(source)]) == 0

    assert capsys.readouterr().out == format_report("the cat the a cat the") + "\n"


def test_main_top_option_limits_top_words(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "sample.txt"
    source.write_text("the cat the a cat the dog", encoding="utf-8")

    assert main([str(source), "--top", "2"]) == 0

    assert capsys.readouterr().out == format_report("the cat the a cat the dog", n=2) + "\n"


def test_main_lists_three_top_words_without_top_option(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "sample.txt"
    source.write_text("the cat the a cat the dog", encoding="utf-8")

    assert main([str(source)]) == 0

    assert capsys.readouterr().out == format_report("the cat the a cat the dog", n=3) + "\n"


def test_module_runs_as_script_and_prints_report(tmp_path: Path) -> None:
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


def test_main_decodes_file_as_utf8(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    source = tmp_path / "accents.txt"
    source.write_bytes("café naïve".encode())

    assert main([str(source)]) == 0

    assert "characters: 10\n" in capsys.readouterr().out
