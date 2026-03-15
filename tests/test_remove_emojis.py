"""Tests for remove_emojis()."""

from davat import remove_emojis


def test_emoji_removed():
    assert remove_emojis("hello 😀 world") == "hello  world"


def test_sad_emoticon():
    assert remove_emojis("sad :(") == "sad "


def test_happy_emoticon():
    assert remove_emojis("happy :)") == "happy "


def test_neutral_emoticon():
    assert remove_emojis("meh :|") == "meh "


def test_spaced_emoticon():
    assert remove_emojis("oh : (") == "oh "


def test_no_emojis():
    assert remove_emojis("plain text") == "plain text"


def test_cat_emoji():
    assert "🐈" not in remove_emojis("cat 🐈‍")


def test_multiple_emojis():
    result = remove_emojis("😀😂🎉 text")
    assert "😀" not in result
    assert "😂" not in result
    assert "text" in result


def test_emoji_between_persian():
    result = remove_emojis("سلام 👋 دنیا")
    assert "👋" not in result
    assert "سلام" in result
    assert "دنیا" in result


def test_empty_string():
    assert remove_emojis("") == ""


def test_only_emojis():
    result = remove_emojis("😀😂")
    assert result.strip() == ""
