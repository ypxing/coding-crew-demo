import os
import subprocess
import sys
from pathlib import Path

import pytest

from textstats import format_report
from textstats.__main__ import main


def test_main_prints_report_for_utf8_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("the cat the a cat the", encoding="utf-8")

    code = main([str(path)])

    out = capsys.readouterr().out
    assert code == 0
    assert out == format_report("the cat the a cat the") + "\n"


def test_main_top_option_limits_top_words(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("the cat the a cat the", encoding="utf-8")

    code = main([str(path), "--top", "2"])

    out = capsys.readouterr().out
    assert code == 0
    assert out == format_report("the cat the a cat the", n=2) + "\n"


def test_main_defaults_to_three_top_words(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("d c b a", encoding="utf-8")

    main([str(path)])

    out = capsys.readouterr().out
    assert out.endswith("top words:\n  a: 1\n  b: 1\n  c: 1\n")


def test_module_runs_as_subprocess(tmp_path: Path) -> None:
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


def test_file_is_read_as_utf8_regardless_of_locale(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "accented.txt"
    path.write_bytes("café café".encode("utf-8"))
    env = {**os.environ, "LC_ALL": "C", "LANG": "C", "PYTHONUTF8": "0", "PYTHONCOERCECLOCALE": "0"}

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(path)],
        capture_output=True,
        env=env,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == (format_report("café café") + "\n").encode("utf-8")
