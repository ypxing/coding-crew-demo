# textstats

A small text statistics library (word count, character count, most frequent words), plus
`format_report(text, n=3)`, which summarises all three as labeled lines.

It exists as the demo project [coding-crew](https://github.com/ypxing/coding-crew) runs a real
crew-afk sprint against before each release; coding-crew pins one commit of it.

```bash
uv run pytest && uv run ruff check . && uv run mypy .
```
