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


def test_main_missing_file_reports_error_and_returns_1(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from textstats.__main__ import main

    assert main([str(tmp_path / "missing.txt")]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")
    assert "Traceback" not in captured.err


def test_main_directory_reports_error_and_returns_1(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from textstats.__main__ import main

    assert main([str(tmp_path)]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_main_invalid_utf8_reports_error_and_returns_1(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from textstats.__main__ import main

    sample = tmp_path / "bad.txt"
    sample.write_bytes(b"\xff\xfe\xfa")

    assert main([str(sample)]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("textstats: error:")


def test_main_negative_top_is_usage_error_before_reading_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from textstats.__main__ import main

    # The file is missing: if it were read first, main would return 1 instead.
    with pytest.raises(SystemExit) as excinfo:
        main([str(tmp_path / "missing.txt"), "--top", "-1"])

    assert excinfo.value.code == 2
    assert "usage:" in capsys.readouterr().err


def test_main_non_integer_top_is_usage_error(tmp_path: Path) -> None:
    from textstats.__main__ import main

    sample = tmp_path / "sample.txt"
    sample.write_text("the cat", encoding="utf-8")

    with pytest.raises(SystemExit) as excinfo:
        main([str(sample), "--top", "abc"])

    assert excinfo.value.code == 2
