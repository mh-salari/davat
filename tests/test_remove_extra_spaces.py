"""Tests for remove_extra_spaces()."""

from davat import remove_extra_spaces


def test_multiple_spaces():
    assert remove_extra_spaces("سلام   دنیا") == "سلام دنیا"


def test_leading_trailing():
    assert remove_extra_spaces("  سلام  ") == "سلام"


def test_single_spaces_unchanged():
    assert remove_extra_spaces("سلام دنیا") == "سلام دنیا"


def test_tabs_not_affected():
    # Only regular spaces are collapsed, not tabs
    result = remove_extra_spaces("سلام\tدنیا")
    assert "\t" in result


def test_many_spaces():
    assert remove_extra_spaces("a          b") == "a b"


def test_empty_string():
    assert remove_extra_spaces("") == ""


def test_only_spaces():
    assert remove_extra_spaces("     ") == ""


def test_single_word():
    assert remove_extra_spaces("  سلام  ") == "سلام"
