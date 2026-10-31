import os
import subprocess
import sys
from pathlib import Path

import pytest

from textstats import format_report
from textstats.__main__ import main


def test_main_prints_report_for_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    text = "the cat the a cat the"
    path = tmp_path / "sample.txt"
    path.write_text(text, encoding="utf-8")

    assert main([str(path)]) == 0

    assert capsys.readouterr().out == format_report(text) + "\n"


def test_main_top_option_limits_top_words(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    text = "the cat the a cat the"
    path = tmp_path / "sample.txt"
    path.write_text(text, encoding="utf-8")

    assert main([str(path), "--top", "2"]) == 0

    assert capsys.readouterr().out == format_report(text, n=2) + "\n"


def test_main_lists_three_top_words_by_default(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("d c b a", encoding="utf-8")

    assert main([str(path)]) == 0

    assert capsys.readouterr().out.endswith("top words:\n  a: 1\n  b: 1\n  c: 1\n")


def test_main_reads_file_as_utf8(tmp_path: Path) -> None:
    path = tmp_path / "accents.txt"
    path.write_bytes("café naïve café\n".encode())
    # Run under a non-UTF-8 locale so a missing encoding="utf-8" cannot pass by luck.
    env = {
        **os.environ,
        "LC_ALL": "C",
        "PYTHONUTF8": "0",
        "PYTHONCOERCECLOCALE": "0",
    }

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(path)],
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )

    assert result.returncode == 0
    assert result.stdout == (
        "words: 4\n"
        "characters: 16\n"
        "characters (no spaces): 13\n"
        "top words:\n"
        "  caf: 2\n"
        "  na: 1\n"
        "  ve: 1\n"
    )


def test_module_runs_as_script(tmp_path: Path) -> None:
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


def test_main_reports_missing_file_on_stderr(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    missing = tmp_path / "missing.txt"

    assert main([str(missing)]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_main_reports_directory_on_stderr(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(tmp_path)]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_main_reports_invalid_utf8_on_stderr(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "binary.txt"
    path.write_bytes(b"\xff\xfe\xfa")

    assert main([str(path)]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_main_rejects_negative_top_before_reading(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    missing = tmp_path / "missing.txt"

    with pytest.raises(SystemExit) as excinfo:
        main([str(missing), "--top", "-1"])

    assert excinfo.value.code == 2
    assert "usage:" in capsys.readouterr().err


def test_main_rejects_non_integer_top(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("the cat", encoding="utf-8")

    with pytest.raises(SystemExit) as excinfo:
        main([str(path), "--top", "abc"])

    assert excinfo.value.code == 2
    assert "usage:" in capsys.readouterr().err
