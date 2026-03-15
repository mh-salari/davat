"""Tests for remove_ellipsis()."""

from davat import remove_ellipsis


def test_ellipsis_removed():
    assert remove_ellipsis("و …") == "و "


def test_ellipsis_at_end():
    assert remove_ellipsis("ادامه دارد…") == "ادامه دارد"


def test_no_ellipsis():
    assert remove_ellipsis("سلام") == "سلام"


def test_multiple_ellipsis():
    assert remove_ellipsis("یک… دو… سه") == "یک دو سه"


def test_empty_string():
    assert remove_ellipsis("") == ""


def test_three_dots_not_affected():
    # Regular dots are NOT ellipsis character
    assert remove_ellipsis("...") == "..."
