import os
import subprocess
import sys
from pathlib import Path

import pytest
from pytest import CaptureFixture

from textstats import format_report
from textstats.__main__ import main


def test_main_prints_report_for_utf8_file(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("the cat the a cat the", encoding="utf-8")

    code = main([str(path)])

    out = capsys.readouterr().out
    assert code == 0
    assert out == format_report("the cat the a cat the") + "\n"


def test_main_top_option_limits_top_words(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("the cat the a cat the", encoding="utf-8")

    code = main([str(path), "--top", "2"])

    out = capsys.readouterr().out
    assert code == 0
    assert out == format_report("the cat the a cat the", n=2) + "\n"


def test_main_defaults_to_three_top_words(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
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


def test_file_is_read_as_utf8_regardless_of_locale(tmp_path: Path) -> None:
    path = tmp_path / "accented.txt"
    path.write_bytes("café café".encode())
    env = {**os.environ, "LC_ALL": "C", "LANG": "C", "PYTHONUTF8": "0", "PYTHONCOERCECLOCALE": "0"}

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(path)],
        capture_output=True,
        env=env,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == (format_report("café café") + "\n").encode("utf-8")


def test_missing_file_reports_error_and_exits_1(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    code = main([str(tmp_path / "missing.txt")])

    captured = capsys.readouterr()
    assert code == 1
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_directory_reports_error_and_exits_1(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
    code = main([str(tmp_path)])

    captured = capsys.readouterr()
    assert code == 1
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_non_utf8_file_reports_error_and_exits_1(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    path = tmp_path / "binary.txt"
    path.write_bytes(b"\xff\xfe\xfa")

    code = main([str(path)])

    captured = capsys.readouterr()
    assert code == 1
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_negative_top_is_rejected_before_reading_file(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exc:
        main([str(tmp_path / "missing.txt"), "--top", "-1"])

    assert exc.value.code == 2
    assert "usage:" in capsys.readouterr().err


def test_non_integer_top_is_rejected(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("the cat", encoding="utf-8")

    with pytest.raises(SystemExit) as exc:
        main([str(path), "--top", "abc"])

    assert exc.value.code == 2
    assert "usage:" in capsys.readouterr().err
