"""Human-readable summary of a text's statistics."""

from textstats.stats import char_count, top_words, word_count


def format_report(text: str, n: int = 3) -> str:
    """Return a labeled-lines summary of ``text``'s word, character and top-word counts."""
    lines = [
        f"words: {word_count(text)}",
        f"characters: {char_count(text)}",
        f"characters (no spaces): {char_count(text, include_spaces=False)}",
        "top words:",
    ]
    lines += [f"  {word}: {count}" for word, count in top_words(text, n)]
    return "\n".join(lines)
