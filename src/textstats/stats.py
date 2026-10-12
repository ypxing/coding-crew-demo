"""Word and character statistics over plain text."""

import re
from collections import Counter

_WORD = re.compile(r"[A-Za-z0-9']+")


def words(text: str) -> list[str]:
    """Return the words in ``text``, lowercased, in order."""
    return [w.lower() for w in _WORD.findall(text)]


def word_count(text: str) -> int:
    """Return the number of words in ``text``."""
    return len(words(text))


def char_count(text: str, *, include_spaces: bool = True) -> int:
    """Return the number of characters in ``text``, optionally ignoring whitespace."""
    if include_spaces:
        return len(text)
    return sum(1 for c in text if not c.isspace())


def top_words(text: str, n: int = 3) -> list[tuple[str, int]]:
    """Return the ``n`` most frequent words with their counts, ties broken alphabetically."""
    if n < 0:
        raise ValueError("n must be non-negative")
    counts = Counter(words(text))
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:n]


def unique_word_count(text: str) -> int:
    """Return the number of distinct words in ``text``."""
    return len(set(words(text)))
