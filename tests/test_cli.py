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
