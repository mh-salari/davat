"""Tests for convert_digits()."""

import pytest

from davat import convert_digits


def test_english_to_persian():
    assert convert_digits("0123456789", to="fa") == "۰۱۲۳۴۵۶۷۸۹"


def test_arabic_to_persian():
    assert convert_digits("٠١٢٣٤٥٦٧٨٩", to="fa") == "۰۱۲۳۴۵۶۷۸۹"


def test_persian_to_english():
    assert convert_digits("۰۱۲۳۴۵۶۷۸۹", to="en") == "0123456789"


def test_arabic_to_english():
    assert convert_digits("٠١٢٣٤٥٦٧٨٩", to="en") == "0123456789"


def test_percent_to_persian():
    assert convert_digits("50%", to="fa") == "۵۰٪"


def test_percent_to_english():
    assert convert_digits("۵۰٪", to="en") == "50%"


def test_mixed_text_preserved():
    assert convert_digits("test 123 سلام", to="fa") == "test ۱۲۳ سلام"


def test_no_digits_unchanged():
    assert convert_digits("سلام دنیا", to="fa") == "سلام دنیا"


def test_invalid_target_raises():
    with pytest.raises(ValueError, match="Unsupported"):
        convert_digits("123", to="xx")


def test_roundtrip_en_fa_en():
    original = "price: 1,234.56"
    assert convert_digits(convert_digits(original, to="fa"), to="en") == original


def test_roundtrip_en_ar_en():
    original = "test 9876"
    result = convert_digits(convert_digits(original, to="ar"), to="en")
    assert result == original


def test_empty_string():
    assert convert_digits("", to="fa") == ""
    assert convert_digits("", to="en") == ""


def test_only_digits():
    assert convert_digits("999", to="fa") == "۹۹۹"


def test_mixed_arabic_english_to_persian():
    assert convert_digits("٣ and 7", to="fa") == "۳ and ۷"
