"""Plain-text summary of word and character statistics."""

from textstats.stats import char_count, top_words, word_count


def format_report(text: str, n: int = 3) -> str:
    """Return a labeled-lines summary of ``text``."""
    top = top_words(text, n)
    lines = [
        f"words: {word_count(text)}",
        f"characters: {char_count(text)}",
        f"characters (no spaces): {char_count(text, include_spaces=False)}",
        "top words:",
    ]
    if not top:
        lines.append("  (none)")
    lines.extend(f"  {word}: {count}" for word, count in top)
    return "\n".join(lines)
