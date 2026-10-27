"""Plain-text summary of a document's word and character statistics."""

from textstats.stats import char_count, top_words, word_count


def format_report(text: str, n: int = 3) -> str:
    """Return a labeled-lines summary of ``text`` listing at most ``n`` top words."""
    lines = [
        f"words: {word_count(text)}",
        f"characters: {char_count(text)}",
        f"characters (no spaces): {char_count(text, include_spaces=False)}",
        "top words:",
    ]
    ranked = top_words(text, n)
    if ranked:
        lines.extend(f"  {word}: {count}" for word, count in ranked)
    else:
        lines.append("  (none)")
    return "\n".join(lines)
