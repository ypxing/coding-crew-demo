import os
import subprocess
import sys
from pathlib import Path

import pytest

from textstats import format_report
from textstats.__main__ import main


def test_main_prints_report_for_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    text = "the cat the a cat the"
    sample = tmp_path / "sample.txt"
    sample.write_text(text, encoding="utf-8")

    assert main([str(sample)]) == 0

    assert capsys.readouterr().out == format_report(text) + "\n"


def test_main_top_limits_top_words(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    sample = tmp_path / "sample.txt"
    sample.write_text("the cat the a cat the", encoding="utf-8")

    assert main([str(sample), "--top", "2"]) == 0

    out = capsys.readouterr().out
    assert out.endswith("top words:\n  the: 3\n  cat: 2\n")


def test_main_defaults_to_three_top_words(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    sample = tmp_path / "sample.txt"
    sample.write_text("d c b a", encoding="utf-8")

    assert main([str(sample)]) == 0

    out = capsys.readouterr().out
    assert out.endswith("top words:\n  a: 1\n  b: 1\n  c: 1\n")


def test_main_decodes_file_as_utf8(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    text = "café naïve"
    sample = tmp_path / "sample.txt"
    sample.write_bytes(text.encode("utf-8"))

    assert main([str(sample)]) == 0

    assert "characters: 10\n" in capsys.readouterr().out


def test_main_decodes_file_as_utf8_under_ascii_locale(tmp_path: Path) -> None:
    sample = tmp_path / "sample.txt"
    sample.write_bytes("café naïve".encode())
    env = {
        **os.environ,
        "LC_ALL": "C",
        "PYTHONUTF8": "0",
        "PYTHONCOERCECLOCALE": "0",
        "PYTHONIOENCODING": "utf-8",
    }

    code = "import sys; from textstats.__main__ import main; sys.exit(main([sys.argv[1]]))"
    result = subprocess.run(
        [sys.executable, "-c", code, str(sample)],
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "characters: 10\n" in result.stdout


def test_python_m_textstats_runs_as_subprocess(tmp_path: Path) -> None:
    text = "the cat the a cat the"
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


def test_main_reports_missing_file_as_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    missing = tmp_path / "missing.txt"

    assert main([str(missing)]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_main_reports_directory_as_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(tmp_path)]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_main_reports_non_utf8_file_as_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    sample = tmp_path / "sample.txt"
    sample.write_bytes(b"\xff\xfe\xfa")

    assert main([str(sample)]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_main_rejects_negative_top_before_reading_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    missing = tmp_path / "missing.txt"

    with pytest.raises(SystemExit) as excinfo:
        main([str(missing), "--top", "-1"])

    assert excinfo.value.code == 2
    assert "error" in capsys.readouterr().err


def test_main_rejects_non_integer_top(tmp_path: Path) -> None:
    sample = tmp_path / "sample.txt"
    sample.write_text("the cat", encoding="utf-8")

    with pytest.raises(SystemExit) as excinfo:
        main([str(sample), "--top", "abc"])

    assert excinfo.value.code == 2
