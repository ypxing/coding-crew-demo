"""Plain-text summary of a text, built on ``textstats.stats``."""

from textstats.stats import char_count, top_words, word_count


def format_report(text: str, n: int = 3) -> str:
    """Return a labeled-lines summary: word and character counts, then the top ``n`` words."""
    lines = [
        f"words: {word_count(text)}",
        f"characters: {char_count(text)}",
        f"characters (no spaces): {char_count(text, include_spaces=False)}",
        "top words:",
    ]
    top = top_words(text, n)
    lines.extend(f"  {word}: {count}" for word, count in top)
    if not top:
        lines.append("  (none)")
    return "\n".join(lines)
