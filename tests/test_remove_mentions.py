"""Tests for remove_mentions()."""

from davat import remove_mentions


def test_simple_mention():
    assert remove_mentions("hello @user world") == "hello  world"


def test_multiple_mentions():
    assert remove_mentions("@a @b text") == "  text"


def test_no_mention():
    assert remove_mentions("no mentions") == "no mentions"


def test_mention_with_numbers():
    assert remove_mentions("@user123 test") == " test"


def test_mention_at_end():
    assert remove_mentions("text @user") == "text "


def test_mention_with_underscore():
    assert remove_mentions("hello @mh_salari bye") == "hello  bye"


def test_persian_text_around_mention():
    assert remove_mentions("سلام @user خوبی") == "سلام  خوبی"


def test_empty_string():
    assert remove_mentions("") == ""


def test_only_mention():
    assert remove_mentions("@onlythis") == ""
