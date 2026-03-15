"""Tests for clean() pipeline."""

from functools import partial

from davat import (
    MINIMAL_STEPS,
    PERSIAN_STEPS,
    clean,
    remove_emojis,
    remove_extra_spaces,
    remove_links,
    remove_mentions,
    strip_characters,
)

# --- Default pipeline ---


def test_default_removes_links():
    result = clean("سلام https://example.com دنیا")
    assert "https" not in result
    assert "سلام" in result


def test_default_removes_mentions():
    result = clean("سلام @user دنیا")
    assert "@user" not in result


def test_default_removes_hashtag_symbol():
    result = clean("سلام #تست")
    assert "#" not in result
    assert "تست" in result


def test_default_removes_emojis():
    result = clean("سلام 😀 دنیا")
    assert "😀" not in result


def test_default_normalizes_persian():
    result = clean("كتاب عربي")
    assert "کتاب" in result
    assert "عربی" in result


def test_default_strips_non_persian():
    result = clean("hello سلام world")
    assert "hello" not in result
    assert "سلام" in result


def test_default_cleans_spaces():
    result = clean("سلام     دنیا")
    assert "     " not in result


def test_default_collapses_punctuation():
    result = clean("سلام!!!! دنیا")
    assert "!!!!" not in result


# --- README example ---


def test_readme_example():
    text = """
متنی برای برسی تابع تمیز کردن متن
که #هشتگ_ها را خیلی عاااااللللییییی!!!! تبدیل به متن عادی می‌کند!
منشن‌ها @mh_salari و لینک‌ها www.mh-salari.ir را حذف می‌کند.
حروف غیر فارسی  a b c d و اموجی‌ها :( 🐈‍ را حذف می‌کند
علائم دستوری/نگارشی ?!٫ را حذف نمی‌کند
و ...
http://localhost:8888
"""
    result = clean(text)
    assert isinstance(result, str)
    assert len(result) > 0
    assert "@mh_salari" not in result
    assert "http" not in result
    assert "🐈" not in result
    assert "a b c d" not in result


# --- Custom steps ---


def test_custom_steps():
    result = clean("hello 😀 world", steps=[remove_emojis, remove_extra_spaces])
    assert result == "hello world"


def test_minimal_steps():
    result = clean("سلام https://x.com 😀 hello", steps=MINIMAL_STEPS)
    assert "https" not in result
    assert "😀" not in result
    assert "hello" in result  # minimal doesn't strip non-persian


def test_custom_multilingual():
    steps = [
        remove_links,
        remove_mentions,
        remove_emojis,
        partial(strip_characters, keep=["fa", "en", "ar"]),
        remove_extra_spaces,
    ]
    text = "hello سلام مرحبا https://example.com @user 😀 שלום"
    result = clean(text, steps=steps)
    assert "hello" in result
    assert "سلام" in result
    assert "https" not in result
    assert "@user" not in result
    assert "😀" not in result


# --- Edge cases ---


def test_empty_string():
    assert clean("") == ""


def test_only_whitespace():
    assert clean("   ") == ""


def test_only_emojis():
    result = clean("😀😂🎉")
    assert result.strip() == ""


def test_steps_order_matters():
    # With normalize first, digits get converted
    from davat import normalize_persian

    result1 = clean("test 123", steps=[normalize_persian, remove_extra_spaces])
    assert "۱۲۳" in result1


def test_none_steps_uses_default():
    result = clean("سلام https://example.com", steps=None)
    assert "https" not in result


def test_persian_steps_is_a_list():
    assert isinstance(PERSIAN_STEPS, list)
    assert len(PERSIAN_STEPS) > 0


def test_minimal_steps_is_a_list():
    assert isinstance(MINIMAL_STEPS, list)
    assert len(MINIMAL_STEPS) > 0
