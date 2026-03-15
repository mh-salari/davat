"""Tests for remove_punctuations()."""

from davat import remove_punctuations


def test_exclamation():
    assert "!" not in remove_punctuations("سلام!")


def test_persian_question():
    assert "؟" not in remove_punctuations("آیا؟")


def test_slash_becomes_space():
    assert remove_punctuations("دستوری/نگارشی") == "دستوری نگارشی"


def test_text_preserved():
    assert remove_punctuations("سلام دنیا") == "سلام دنیا"


def test_brackets_removed():
    result = remove_punctuations("(سلام) [دنیا] {خوب}")
    assert "(" not in result
    assert "[" not in result
    assert "{" not in result


def test_mixed_punctuation():
    result = remove_punctuations("سلام! دنیا؟ خوب. آره،")
    assert "!" not in result
    assert "؟" not in result
    assert "،" not in result


def test_empty_string():
    assert remove_punctuations("") == ""


def test_only_punctuation():
    result = remove_punctuations("!?.,")
    assert result.strip() == ""


def test_persian_comma_removed():
    assert "،" not in remove_punctuations("سلام، دنیا")


def test_at_sign_removed():
    assert "@" not in remove_punctuations("test@example")


def test_hash_removed():
    assert "#" not in remove_punctuations("#تست")
