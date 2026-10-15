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


def test_crlf_bytes_give_same_report_from_file_and_stdin(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    data = b"a b\r\nc\r\n"
    path = tmp_path / "crlf.txt"
    path.write_bytes(data)
    assert main([str(path)]) == 0
    from_file = capsys.readouterr().out
    feed_stdin(monkeypatch, data)
    assert main([]) == 0
    from_stdin = capsys.readouterr().out
    assert from_file == from_stdin
    assert "characters: 8\n" in from_file


def test_negative_top_is_a_usage_error(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        main(["--top", "-1"])
    assert exc.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "--top" in captured.err


@pytest.mark.parametrize("name", ["missing.txt", "."])
def test_unreadable_file_is_a_usage_error(
    name: str, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exc:
        main([str(tmp_path / name)])
    assert exc.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "error:" in captured.err
    assert "Traceback" not in captured.err


@pytest.mark.parametrize("source", ["file", "stdin"])
def test_invalid_utf8_is_a_usage_error(
    source: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    data = b"\xff\xfe"
    if source == "file":
        path = tmp_path / "bad.txt"
        path.write_bytes(data)
        argv = [str(path)]
    else:
        feed_stdin(monkeypatch, data)
        argv = []
    with pytest.raises(SystemExit) as exc:
        main(argv)
    assert exc.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "UTF-8" in captured.err
