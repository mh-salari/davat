"""Tests for remove_hashtags()."""

from davat import remove_hashtags


def test_keep_text_default():
    assert remove_hashtags("#سلام") == " سلام"


def test_keep_text_true():
    assert remove_hashtags("#hello #world", keep_text=True) == " hello  world"


def test_keep_text_false():
    assert remove_hashtags("text #tag more", keep_text=False) == "text  more"


def test_remove_entire_hashtag():
    assert remove_hashtags("#حذف_شود نه_این", keep_text=False) == " نه_این"


def test_no_hashtags():
    assert remove_hashtags("no tags") == "no tags"


def test_multiple_hashtags_keep():
    result = remove_hashtags("#یک #دو #سه")
    assert "#" not in result
    assert "یک" in result
    assert "سه" in result


def test_multiple_hashtags_remove():
    result = remove_hashtags("#one #two keep", keep_text=False)
    assert "one" not in result
    assert "two" not in result
    assert "keep" in result


def test_empty_string():
    assert remove_hashtags("") == ""


def test_hashtag_with_underscore():
    result = remove_hashtags("#هشتگ_ها", keep_text=True)
    assert "هشتگ" in result
    assert "#" not in result
