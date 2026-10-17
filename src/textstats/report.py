"""Plain-text summary of a text, built on ``textstats.stats``."""

from textstats.stats import char_count, top_words, word_count


def format_report(text: str, n: int = 3) -> str:
    """Return a labeled-lines summary: word count, character counts and the top ``n`` words."""
    lines = [
        f"words: {word_count(text)}",
        f"characters: {char_count(text)}",
        f"characters (no spaces): {char_count(text, include_spaces=False)}",
        "top words:",
    ]
    ranked = top_words(text, n)
    if not ranked:
        lines.append("  (none)")
    else:
        lines.extend(f"  {word}: {count}" for word, count in ranked)
    return "\n".join(lines)
