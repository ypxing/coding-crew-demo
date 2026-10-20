import subprocess
import sys
from pathlib import Path

import pytest

from textstats import format_report


def test_main_prints_report_for_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    from textstats.__main__ import main

    text = "the cat the a cat the"
    sample = tmp_path / "sample.txt"
    sample.write_text(text, encoding="utf-8")

    assert main([str(sample)]) == 0
    assert capsys.readouterr().out == format_report(text) + "\n"


def test_main_top_option_limits_top_words(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from textstats.__main__ import main

    text = "b a b c a b"
    sample = tmp_path / "sample.txt"
    sample.write_text(text, encoding="utf-8")

    assert main([str(sample), "--top", "2"]) == 0
    assert capsys.readouterr().out == format_report(text, n=2) + "\n"


def test_main_defaults_to_three_top_words(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from textstats.__main__ import main

    text = "d c c b b b a a a a"
    sample = tmp_path / "sample.txt"
    sample.write_text(text, encoding="utf-8")

    assert main([str(sample)]) == 0
    assert capsys.readouterr().out.splitlines()[4:] == ["  a: 4", "  b: 3", "  c: 2"]


def test_main_reads_utf8_regardless_of_locale(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from textstats.__main__ import main

    text = "café naïve café"
    sample = tmp_path / "sample.txt"
    sample.write_bytes(text.encode("utf-8"))

    assert main([str(sample)]) == 0
    assert capsys.readouterr().out == format_report(text) + "\n"


def test_module_run_as_subprocess_prints_report(tmp_path: Path) -> None:
    text = "the cat the"
    sample = tmp_path / "sample.txt"
    sample.write_text(text, encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(sample)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == format_report(text) + "\n"
