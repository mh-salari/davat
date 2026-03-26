"""Tests for remove_markdown()."""

from davat import remove_markdown


def test_bold():
    assert remove_markdown("this is **bold** text") == "this is bold text"


def test_italic_underscore():
    assert remove_markdown("this is __italic__ text") == "this is italic text"


def test_strikethrough():
    assert remove_markdown("this is ~~deleted~~ text") == "this is deleted text"


def test_inline_code():
    assert remove_markdown("use `code` here") == "use code here"


def test_link_keeps_url():
    assert remove_markdown("[click here](https://example.com)") == "click here https://example.com"


def test_link_with_persian_keeps_url():
    assert remove_markdown("[اینجا کلیک کنید](https://example.com)") == "اینجا کلیک کنید https://example.com"


def test_leftover_stars():
    assert remove_markdown("*partial") == "partial"


def test_leftover_underscores():
    assert remove_markdown("some_thing") == "some thing"


def test_underscores_in_url_preserved():
    text = "photo: [عطا داداشی](https://farsnews.ir/ata_dadashi/12345)"
    result = remove_markdown(text)
    assert "ata_dadashi" in result
    assert result == "photo: عطا داداشی https://farsnews.ir/ata_dadashi/12345"


def test_bare_url_underscores_preserved():
    text = "see https://example.com/some_path/file_name for details"
    result = remove_markdown(text)
    assert "some_path" in result
    assert "file_name" in result


def test_pipe_in_url_preserved():
    text = "check https://example.com/search?a|b for results"
    result = remove_markdown(text)
    assert "a|b" in result


def test_pipe_outside_url_replaced():
    text = "col1 | col2 | col3"
    result = remove_markdown(text)
    assert "|" not in result


def test_combined():
    text = "**bold** and ~~strike~~ and [link](http://x.com)"
    assert remove_markdown(text) == "bold and strike and link http://x.com"


def test_nested_bold_in_text():
    text = "normal **bold part** normal"
    assert remove_markdown(text) == "normal bold part normal"


def test_multiple_bold():
    text = "**one** and **two**"
    assert remove_markdown(text) == "one and two"


def test_code_with_special_chars():
    assert remove_markdown("run `pip install davat`") == "run pip install davat"


def test_empty_string():
    assert remove_markdown("") == ""


def test_no_markdown():
    assert remove_markdown("plain text سلام") == "plain text سلام"


def test_telegram_style_message():
    text = "**Breaking:** New update from [channel](https://t.me/channel) is ~~old~~ fresh"
    result = remove_markdown(text)
    assert result == "Breaking: New update from channel https://t.me/channel is old fresh"


def test_empty_link_url():
    assert remove_markdown("[text]()") == "text"
