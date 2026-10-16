"""Human-readable summary of text statistics."""

from textstats.stats import char_count, top_words, word_count


def format_report(text: str, n: int = 3) -> str:
    """Return a labeled-lines summary of word, character and top-word statistics.

    Lines are joined by ``\\n`` with no trailing newline, so callers can ``print`` it.
    """
    lines = [
        f"words: {word_count(text)}",
        f"characters: {char_count(text)}",
        f"characters (no spaces): {char_count(text, include_spaces=False)}",
        "top words:",
    ]
    lines.extend(f"  {word}: {count}" for word, count in top_words(text, n))
    return "\n".join(lines)
