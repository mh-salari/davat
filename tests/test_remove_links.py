"""Tests for remove_links()."""

from davat import remove_links


def test_http_link():
    assert remove_links("visit https://example.com please") == "visit  please"


def test_https_with_path():
    assert remove_links("see https://example.com/path/to/page end") == "see  end"


def test_www_link():
    assert remove_links("visit www.example.com please") == "visit  please"


def test_no_link():
    assert remove_links("no links here") == "no links here"


def test_multiple_links():
    text = "first https://a.com second https://b.com third"
    result = remove_links(text)
    assert "https" not in result
    assert "first" in result
    assert "third" in result


def test_preserves_persian_digits():
    text = "شماره ۱۲۳ و https://test.org"
    result = remove_links(text)
    assert "۱۲۳" in result
    assert "test" not in result


def test_preserves_arabic_digits():
    text = "عدد ٥٠ و https://example.com"
    result = remove_links(text)
    assert "٥٠" in result
    assert "example" not in result


def test_link_at_start():
    assert remove_links("https://example.com text after").strip().startswith("text")


def test_link_at_end():
    result = remove_links("text before https://example.com")
    assert "text before" in result
    assert "example" not in result


def test_empty_string():
    assert remove_links("") == ""


def test_localhost_link():
    result = remove_links("visit http://localhost:8888 done")
    assert "localhost" not in result


def test_linkedin_long_url():
    url = (
        "https://www.linkedin.com/posts/mh-salari_hi-eye-tracking-community-"
        "ive-released-activity-7416789052915408896-WL8F"
        "?utm_source=share&utm_medium=member_desktop"
        "&rcm=ACoAADcn9I8Bp5KBu2zH0jT8y9ODSZ-KCtyXocU"
    )
    result = remove_links(f"سلام {url} دنیا")
    assert "linkedin" not in result
    assert "سلام" in result
    assert "دنیا" in result


def test_url_with_numbers():
    result = remove_links("see https://example.com/page/12345 end")
    assert "12345" not in result
    assert "see" in result


def test_markdown_style_url_no_backtracking():
    """Regression: markdown-style URLs must not cause catastrophic backtracking."""
    text = "[dnws.ir/003QwU](https://web.splus.ir/dnws.ir/003QwU)"
    result = remove_links(text)
    assert "https" not in result
    assert "splus" not in result
