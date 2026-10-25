import locale
import subprocess
import sys
from pathlib import Path

import pytest

from textstats import format_report
from textstats.__main__ import main


def test_main_prints_report_for_utf8_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    text = "the cat the a cat the"
    path = tmp_path / "doc.txt"
    path.write_text(text, encoding="utf-8")

    assert main([str(path)]) == 0

    assert capsys.readouterr().out == format_report(text) + "\n"


def test_main_top_option_limits_top_words(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    text = "the cat the a cat the"
    path = tmp_path / "doc.txt"
    path.write_text(text, encoding="utf-8")

    assert main([str(path), "--top", "2"]) == 0

    assert capsys.readouterr().out == format_report(text, n=2) + "\n"


def test_main_defaults_to_three_top_words(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    text = "d c b a d c b"
    path = tmp_path / "doc.txt"
    path.write_text(text, encoding="utf-8")

    assert main([str(path)]) == 0

    lines = capsys.readouterr().out.splitlines()
    assert lines[-3:] == ["  b: 2", "  c: 2", "  d: 2"]


def test_module_runs_as_subprocess(tmp_path: Path) -> None:
    path = tmp_path / "doc.txt"
    path.write_text("the cat the a cat the", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == format_report("the cat the a cat the") + "\n"


def test_main_reads_file_as_utf8_regardless_of_locale(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(locale, "getpreferredencoding", lambda do_setlocale=True: "ascii")
    path = tmp_path / "doc.txt"
    path.write_text("café café", encoding="utf-8")

    assert main([str(path)]) == 0

    assert "characters: 9" in capsys.readouterr().out.splitlines()
