"""Tests for strip_characters()."""

from davat import strip_characters


def test_keep_persian_only():
    result = strip_characters("hello سلام 123", keep="fa")
    assert "hello" not in result
    assert "سلام" in result


def test_keep_english_only():
    result = strip_characters("hello سلام world", keep="en")
    assert "hello" in result
    assert "world" in result
    assert "سلام" not in result


def test_keep_persian_and_english():
    result = strip_characters("hello سلام שלום", keep=["fa", "en"])
    assert "hello" in result
    assert "سلام" in result
    assert "שלום" not in result


def test_keep_all_four():
    result = strip_characters("hello سلام שלום مرحبا", keep=["fa", "en", "he", "ar"])
    assert "hello" in result
    assert "سلام" in result
    assert "שלום" in result


def test_keep_persian_preserves_digits():
    result = strip_characters("عدد ۱۲۳", keep="fa")
    assert "۱۲۳" in result


def test_keep_english_preserves_digits():
    result = strip_characters("num 123", keep="en")
    assert "123" in result


def test_common_punctuation_preserved():
    result = strip_characters("سلام! دنیا؟", keep="fa")
    assert "!" in result
    assert "؟" in result


def test_newlines_preserved():
    result = strip_characters("سلام\nدنیا", keep="fa")
    assert "\n" in result


def test_spaces_preserved():
    result = strip_characters("سلام دنیا", keep="fa")
    assert " " in result


def test_empty_string():
    assert strip_characters("") == ""


def test_string_keep_param():
    result = strip_characters("hello سلام", keep="fa")
    assert "سلام" in result


def test_list_keep_param():
    result = strip_characters("hello سلام", keep=["fa"])
    assert "سلام" in result


def test_zwnj_preserved():
    result = strip_characters("می\u200cخواهم", keep="fa")
    assert "\u200c" in result
