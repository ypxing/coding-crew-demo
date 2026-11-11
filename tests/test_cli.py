import subprocess
import sys
from pathlib import Path

from textstats import format_report


def test_module_run_prints_report_and_exits_zero(tmp_path: Path) -> None:
    source = tmp_path / "sample.txt"
    source.write_text("the cat the a cat the", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "textstats", str(source)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == format_report("the cat the a cat the") + "\n"
