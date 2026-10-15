"""Small text statistics: counts and frequent words."""

from textstats.report import report
from textstats.stats import char_count, top_words, word_count, words

__all__ = ["char_count", "report", "top_words", "word_count", "words"]
