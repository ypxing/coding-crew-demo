"""Plain-text rendering of the text statistics."""

from textstats.stats import char_count, top_words, word_count


def report(text: str, *, top: int = 3) -> str:
    """Return a plain-text report of ``text``'s stats, ending with one newline."""
    lines = [
        f"words: {word_count(text)}",
        f"characters: {char_count(text, include_spaces=True)}",
        f"characters (no spaces): {char_count(text, include_spaces=False)}",
        "top words:",
    ]
    ranked = top_words(text, top)
    width = max((len(word) for word, _ in ranked), default=0)
    lines.extend(f"  {word.ljust(width)}  {count}" for word, count in ranked)
    if not ranked:
        lines.append("  (none)")
    return "\n".join(lines) + "\n"
