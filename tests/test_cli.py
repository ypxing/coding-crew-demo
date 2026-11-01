import builtins
import subprocess
import sys
from pathlib import Path

import pytest

from textstats.__main__ import main
from textstats.report import format_report

SAMPLE = "the cat the a cat the"


def test_main_prints_report_and_returns_zero(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "sample.txt"
    path.write_text(SAMPLE, encoding="utf-8")

    assert main([str(path)]) == 0
    assert capsys.readouterr().out == format_report(SAMPLE) + "\n"


def test_main_default_lists_three_top_words(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("a b c d e a b c d a", encoding="utf-8")

    main([str(path)])
    top_lines = capsys.readouterr().out.splitlines()[4:]
    assert top_lines == ["  a: 3", "  b: 2", "  c: 2"]


def test_main_top_option_limits_top_words(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "sample.txt"
    path.write_text(SAMPLE, encoding="utf-8")

    assert main([str(path), "--top", "2"]) == 0
    assert capsys.readouterr().out == format_report(SAMPLE, n=2) + "\n"


def test_main_reads_file_as_utf8_explicitly(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("café naïve", encoding="utf-8")
    seen: dict[str, object] = {}
    real_open = builtins.open

    def spy(file: object, *args: object, **kwargs: object) -> object:
        seen.update(kwargs)
        return real_open(file, *args, **kwargs)  # type: ignore[call-overload]

    monkeypatch.setattr(builtins, "open", spy)
    main([str(path)])
    assert seen.get("encoding") == "utf-8"


def test_module_prints_report_for_file(tmp_path: Path) -> None:
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
