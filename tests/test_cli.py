import io
from pathlib import Path

import pytest

from textstats import report
from textstats.cli import main


def feed_stdin(monkeypatch: pytest.MonkeyPatch, data: bytes) -> None:
    # A TextIOWrapper so the CLI can read the raw bytes from ``sys.stdin.buffer``.
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(data)))


def test_main_prints_report_for_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "in.txt"
    path.write_text("b a b c a b", encoding="utf-8")
    assert main([str(path)]) == 0
    assert capsys.readouterr().out == report("b a b c a b")


def test_main_passes_top_to_report(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "in.txt"
    path.write_text("b a b c a b", encoding="utf-8")
    assert main([str(path), "--top", "1"]) == 0
    assert capsys.readouterr().out == report("b a b c a b", top=1)


@pytest.mark.parametrize("argv", [[], ["-"]])
def test_main_reads_stdin_without_file_or_with_dash(
    argv: list[str], monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    feed_stdin(monkeypatch, "café café x".encode())
    assert main(argv) == 0
    assert capsys.readouterr().out == report("café café x")
