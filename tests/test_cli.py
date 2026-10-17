import subprocess
import sys
from pathlib import Path

import pytest

from textstats import format_report
from textstats.__main__ import main

TEXT = "the cat the a cat the b b b c c c d"


def test_main_prints_report_and_returns_zero(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "sample.txt"
    path.write_text(TEXT, encoding="utf-8")

    assert main([str(path)]) == 0

    assert capsys.readouterr().out == format_report(TEXT) + "\n"


def test_main_top_limits_top_words(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "sample.txt"
    path.write_text(TEXT, encoding="utf-8")

    assert main([str(path), "--top", "2"]) == 0

    assert capsys.readouterr().out == format_report(TEXT, n=2) + "\n"


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


def test_main_decodes_file_as_utf8(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    text = "café naïve café — ✓"
    path = tmp_path / "unicode.txt"
    path.write_bytes(text.encode("utf-8"))

    assert main([str(path)]) == 0

    assert capsys.readouterr().out == format_report(text) + "\n"
