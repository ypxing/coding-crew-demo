import subprocess
import sys
from pathlib import Path

import pytest

from textstats.__main__ import main
from textstats.report import format_report


def test_main_prints_report_for_utf8_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("the cat the a cat the", encoding="utf-8")

    exit_code = main([str(path)])

    assert exit_code == 0
    assert capsys.readouterr().out == format_report("the cat the a cat the") + "\n"


def test_main_top_option_limits_top_words(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("the cat the a cat the", encoding="utf-8")

    exit_code = main([str(path), "--top", "2"])

    assert exit_code == 0
    assert capsys.readouterr().out == format_report("the cat the a cat the", n=2) + "\n"


def test_main_lists_three_top_words_by_default(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("d c b a", encoding="utf-8")

    exit_code = main([str(path)])

    assert exit_code == 0
    assert capsys.readouterr().out.endswith("top words:\n  a: 1\n  b: 1\n  c: 1\n")


def test_python_m_textstats_prints_report(tmp_path: Path) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("the cat the a cat the", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == format_report("the cat the a cat the") + "\n"
