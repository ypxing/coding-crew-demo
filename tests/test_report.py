from textstats import format_report


def test_format_report_summarises_words_characters_and_top_words() -> None:
    expected = (
        "words: 6\n"
        "characters: 21\n"
        "characters (no spaces): 16\n"
        "top words:\n"
        "  the: 3\n"
        "  cat: 2\n"
        "  a: 1"
    )
    assert format_report("the cat the a cat the") == expected
