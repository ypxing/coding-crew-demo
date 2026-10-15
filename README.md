# textstats

A small text statistics library (word count, character count, most frequent words), with
`report(text, top=3)` rendering them as a plain-text report, and a `textstats` command that prints
that report for a file or stdin:

```bash
uv run textstats README.md --top 5   # or: cat README.md | uv run python -m textstats
```

It exists as the demo project [coding-crew](https://github.com/ypxing/coding-crew) runs a real
crew-afk sprint against before each release; coding-crew pins one commit of it.

```bash
uv run pytest && uv run ruff check . && uv run mypy .
```
