import pytest

import textstats
from textstats import char_count, top_words, word_count, words


def test_words_lowercases_and_strips_punctuation() -> None:
    assert words("Hello, world! It's here.") == ["hello", "world", "it's", "here"]


def test_word_count_empty() -> None:
    assert word_count("") == 0


def test_word_count() -> None:
    assert word_count("one two  three\nfour") == 4


def test_char_count_with_and_without_spaces() -> None:
    assert char_count("a b\tc") == 5
    assert char_count("a b\tc", include_spaces=False) == 3


def test_top_words_orders_by_count_then_alphabetically() -> None:
    assert top_words("b a b c a b", n=2) == [("b", 3), ("a", 2)]
    assert top_words("z y x", n=2) == [("x", 1), ("y", 1)]


def test_top_words_rejects_negative_n() -> None:
    with pytest.raises(ValueError):
        top_words("a", n=-1)


def test_unique_word_count_counts_distinct_lowercased_words() -> None:
    assert textstats.unique_word_count("The cat the CAT a") == 3


def test_unique_word_count_empty() -> None:
    assert textstats.unique_word_count("") == 0


def test_unique_word_count_is_exported() -> None:
    assert "unique_word_count" in textstats.__all__


def test_lexical_density_is_unique_over_total() -> None:
    assert textstats.lexical_density("the cat the cat") == 0.5


def test_lexical_density_without_words_is_zero() -> None:
    assert textstats.lexical_density("") == 0.0
    assert textstats.lexical_density("!!") == 0.0


def test_lexical_density_is_exported() -> None:
    assert "lexical_density" in textstats.__all__
