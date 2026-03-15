"""Tests for fix_multiple_punctuations()."""

from davat import fix_multiple_punctuations


def test_multiple_persian_commas():
    assert fix_multiple_punctuations("سلام،،،") == "سلام،"


def test_multiple_persian_question():
    assert fix_multiple_punctuations("چرا؟؟؟") == "چرا؟"


def test_multiple_english_question():
    assert fix_multiple_punctuations("why???") == "why?"


def test_multiple_dots():
    assert fix_multiple_punctuations("آره...") == "آره."


def test_multiple_exclamation():
    assert fix_multiple_punctuations("عالی!!!!") == "عالی!"


def test_single_punctuation_unchanged():
    assert fix_multiple_punctuations("سلام!") == "سلام!"


def test_mixed_punctuation():
    result = fix_multiple_punctuations("واقعا؟؟؟ بله!!! آره...")
    assert "؟؟" not in result
    assert "!!" not in result
    assert ".." not in result


def test_empty_string():
    assert fix_multiple_punctuations("") == ""


def test_no_punctuation():
    assert fix_multiple_punctuations("سلام دنیا") == "سلام دنیا"


def test_two_dots():
    assert fix_multiple_punctuations("..") == "."
