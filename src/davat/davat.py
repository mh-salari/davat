"""Persian text normalization and cleaning library.

Provides composable text processing functions that can be used individually
or combined via the clean() pipeline.
"""

import re
from functools import lru_cache
from pathlib import Path

import emoji

# --- Digit mapping constants ---
# fmt: off
ENGLISH_TO_PERSIAN_DIGITS: dict[str, str] = {
    "0": "۰", "1": "۱", "2": "۲", "3": "۳", "4": "۴",
    "5": "۵", "6": "۶", "7": "۷", "8": "۸", "9": "۹",
}

ARABIC_TO_PERSIAN_DIGITS: dict[str, str] = {
    "٠": "۰", "١": "۱", "٢": "۲", "٣": "۳", "٤": "۴",
    "٥": "۵", "٦": "۶", "٧": "۷", "٨": "۸", "٩": "۹",
}

PERSIAN_TO_ENGLISH_DIGITS: dict[str, str] = {v: k for k, v in ENGLISH_TO_PERSIAN_DIGITS.items()}
ARABIC_TO_ENGLISH_DIGITS: dict[str, str] = {k: PERSIAN_TO_ENGLISH_DIGITS[v] for k, v in ARABIC_TO_PERSIAN_DIGITS.items()}
# fmt: on


def convert_digits(text: str, to: str = "fa") -> str:
    """Convert digits in text to the target script.

    Args:
        text: Input text containing digits to convert.
        to: Target script - "fa" (Persian), "en" (English), or "ar" (Arabic).

    Returns:
        Text with digits converted to the target script.

    """
    if to == "fa":
        mapping = {**ENGLISH_TO_PERSIAN_DIGITS, **ARABIC_TO_PERSIAN_DIGITS, "%": "٪"}
    elif to == "en":
        mapping = {**PERSIAN_TO_ENGLISH_DIGITS, **ARABIC_TO_ENGLISH_DIGITS, "٪": "%"}
    elif to == "ar":
        # Persian→Arabic is just the reverse of Arabic→Persian
        persian_to_arabic = {v: k for k, v in ARABIC_TO_PERSIAN_DIGITS.items()}
        mapping = {**{v: k for k, v in ARABIC_TO_ENGLISH_DIGITS.items()}, **persian_to_arabic}
    else:
        raise ValueError(f"Unsupported target script: {to!r}. Use 'fa', 'en', or 'ar'.")

    pattern = re.compile("|".join(re.escape(k) for k in mapping))
    return pattern.sub(lambda m: mapping[m.group()], text)


_URL_PATTERN = re.compile(
    r"(?:https?://|www\.)[^\s<>\"'\])]+"
    r"|\b[a-z0-9.\-]+\.(?:com|org|net|io|ir|me|co|info|dev|app|ly)/[^\s<>\"'\])]*",
    re.IGNORECASE,
)


def remove_links(text: str) -> str:
    """Remove URLs from text.

    Converts digits to English temporarily for URL matching, then removes
    the matched spans from the original text (preserving original digits).

    Args:
        text: Input text potentially containing URLs.

    Returns:
        Text with all URLs removed.

    """
    temp = convert_digits(text, to="en")
    # Find match positions in converted text, remove same spans from original
    result = []
    last_end = 0
    for m in _URL_PATTERN.finditer(temp):
        result.append(text[last_end : m.start()])
        last_end = m.end()
    result.append(text[last_end:])
    return "".join(result)


def remove_mentions(text: str) -> str:
    """Remove @mentions from text.

    Removes any word starting with @ (e.g. @username).

    Args:
        text: Input text potentially containing mentions.

    Returns:
        Text with all @mentions removed.

    """
    return re.sub(r"@\S+", "", text)


def remove_hashtags(text: str, keep_text: bool = True) -> str:
    """Remove hashtags from text.

    Args:
        text: Input text potentially containing hashtags.
        keep_text: If True, only strip the # symbol but keep the word.
            If False, remove the entire #word.

    Returns:
        Text with hashtags processed.

    """
    if keep_text:
        return text.replace("#", " ")
    return re.sub(r"#\S+", "", text)


_TEXT_EMOTICONS = [":(", ":)", ": (", ": )", ":|", ": |"]

# Geometric symbols used as bullets/decorators in messaging apps (not in emoji library)
_GEOMETRIC_BULLETS = "●•○◦◉◎■□▪▫▬▮▯▲△▴▵▸▹►▻▼▽▾▿◀◁◂◃◄◅◆◇◈◊"


def remove_emojis(text: str) -> str:
    """Remove emoji characters, text emoticons, and geometric bullet symbols.

    Args:
        text: Input text potentially containing emojis or emoticons.

    Returns:
        Text with all emojis, text emoticons, and bullet symbols removed.

    """
    text = emoji.replace_emoji(text, replace="")
    for emoticon in _TEXT_EMOTICONS:
        text = text.replace(emoticon, "")
    for ch in _GEOMETRIC_BULLETS:
        text = text.replace(ch, "")
    return text


def remove_markdown(text: str) -> str:
    """Remove markdown formatting, keeping the inner text.

    Strips **bold**, __italic__, ~~strikethrough~~, `code`,
    and [link text](url) (keeps link text, removes url).

    Args:
        text: Input text potentially containing markdown formatting.

    Returns:
        Text with markdown syntax removed but content preserved.

    """
    # [link text](url) → link text (also handles empty url from prior link removal)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    # **bold** or __italic__
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"__(.+?)__", r"\1", text)
    # ~~strikethrough~~
    text = re.sub(r"~~(.+?)~~", r"\1", text)
    # `inline code`
    text = re.sub(r"`(.+?)`", r"\1", text)
    # leftover * and _ from partial formatting
    text = text.replace("*", "").replace("_", " ")
    # leftover ~~ and | (separators/decorators in messaging apps)
    text = text.replace("~~", "")
    text = text.replace("|", " ")
    return text


# --- Word list for dictionary-aware repeated character collapse ---

_DATA_DIR = Path(__file__).parent / "data"

_PERSIAN_LETTER_CHARS = r"ئآابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیچ"
_REPEATED_CHARS_PATTERN = re.compile(r"([" + _PERSIAN_LETTER_CHARS + r"])\1{2,}")


@lru_cache(maxsize=1)
def _load_word_set() -> frozenset[str]:
    """Lazy-load the Persian word list (only on first call)."""
    words_file = _DATA_DIR / "words.txt"
    with words_file.open(encoding="utf-8") as f:
        return frozenset(line.strip() for line in f if line.strip())


def _collapse_repeated_in_word(token: str, use_dictionary: bool = False) -> str:
    """Collapse 3+ repeated chars in a single token.

    When use_dictionary is True, checks a Persian word list to preserve
    legitimate doubled letters (e.g. الله, موسسه, تردد).
    When False, simply collapses 3+ to single.
    """
    if not _REPEATED_CHARS_PATTERN.search(token):
        return token
    if use_dictionary:
        core = re.sub(r"[^" + _PERSIAN_LETTER_CHARS + r"]", "", token)
        core_to_2 = _REPEATED_CHARS_PATTERN.sub(r"\1\1", core)
        if core_to_2 in _load_word_set():
            return _REPEATED_CHARS_PATTERN.sub(r"\1\1", token)
    return _REPEATED_CHARS_PATTERN.sub(r"\1", token)


def _collapse_repeated_chars(text: str, use_dictionary: bool = False) -> str:
    """Collapse 3+ repeated Persian characters.

    When use_dictionary is True, preserves legitimate doubles using a word list.
    """
    return re.sub(r"\S+", lambda m: _collapse_repeated_in_word(m.group(), use_dictionary), text)


# --- Persian normalization constants ---

_SPACE_CHARS = re.compile(r"[\xad\ufeff\u200e\u200d\u200b\x7f\u202a\u2003\xa0\u206e\u200c\x9d]")

_DIACRITICS = re.compile(r"[\u064b-\u0652]")

# fmt: off
_ARABIC_TO_PERSIAN_CHARS = [
    (r"ء", "ئ"),
    (r"ﺁ|آ", "آ"),
    (r"ٲ|ٱ|إ|ﺍ|أ", "ا"),
    (r"ﺐ|ﺏ|ﺑ", "ب"),
    (r"ﭖ|ﭗ|ﭙ|ﺒ|ﭘ", "پ"),
    (r"ﭡ|ٺ|ٹ|ﭞ|ٿ|ټ|ﺕ|ﺗ|ﺖ|ﺘ", "ت"),
    (r"ﺙ|ﺛ", "ث"),
    (r"ﺝ|ڃ|ﺠ|ﺟ", "ج"),
    (r"ڃ|ﭽ|ﭼ", "چ"),
    (r"ﺢ|ﺤ|څ|ځ|ﺣ", "ح"),
    (r"ﺥ|ﺦ|ﺨ|ﺧ", "خ"),
    (r"ڏ|ډ|ﺪ|ﺩ", "د"),
    (r"ﺫ|ﺬ|ﻧ", "ذ"),
    (r"ڙ|ڗ|ڒ|ڑ|ڕ|ﺭ|ﺮ", "ر"),
    (r"ﺰ|ﺯ", "ز"),
    (r"ﮊ", "ژ"),
    (r"ݭ|ݜ|ﺱ|ﺲ|ښ|ﺴ|ﺳ", "س"),
    (r"ﺵ|ﺶ|ﺸ|ﺷ", "ش"),
    (r"ﺺ|ﺼ|ﺻ", "ص"),
    (r"ﺽ|ﺾ|ﺿ|ﻀ", "ض"),
    (r"ﻁ|ﻂ|ﻃ|ﻄ", "ط"),
    (r"ﻆ|ﻇ|ﻈ", "ظ"),
    (r"ڠ|ﻉ|ﻊ|ﻋ", "ع"),
    (r"ﻎ|ۼ|ﻍ|ﻐ|ﻏ", "غ"),
    (r"ﻒ|ﻑ|ﻔ|ﻓ", "ف"),
    (r"ﻕ|ڤ|ﻖ|ﻗ", "ق"),
    (r"ڭ|ﻚ|ﮎ|ﻜ|ﮏ|ګ|ﻛ|ﮑ|ﮐ|ڪ|ك", "ک"),
    (r"ﮚ|ﮒ|ﮓ|ﮕ|ﮔ", "گ"),
    (r"ﻝ|ﻞ|ﻠ|ڵ", "ل"),
    (r"ﻡ|ﻤ|ﻢ|ﻣ", "م"),
    (r"ڼ|ﻦ|ﻥ|ﻨ", "ن"),
    (r"ވ|ﯙ|ۈ|ۋ|ﺆ|ۊ|ۇ|ۏ|ۅ|ۉ|ﻭ|ﻮ|ؤ", "و"),
    (r"ﺔ|ﻬ|ھ|ﻩ|ﻫ|ﻪ|ۀ|ە|ة|ہ", "ه"),
    (r"ﭛ|ﻯ|ۍ|ﻰ|ﻱ|ﻲ|ں|ﻳ|ﻴ|ﯼ|ې|ﯽ|ﯾ|ﯿ|ێ|ے|ى|ي", "ی"),
    (r"¬", "\u200c"),  # half-space (zwnj)
    (r"•|·|●|·|・|∙|｡|ⴰ", "."),
    (r",|٬|٫|‚|，", "،"),
    (r"ʕ|\?", "؟"),
    (r"[ًٌٍَُِ]", ""),
]
# fmt: on

_PUNCT_AFTER = r"\.:!،؛؟»\]\)\}"
_PUNCT_BEFORE = r"«\[\(\{"


def normalize_persian(text: str, use_dictionary: bool = False) -> str:
    """Normalize Persian text.

    Performs: whitespace normalization, keshide/diacritic removal,
    Arabic-to-Persian character mapping, digit conversion (English/Arabic to
    Persian), quotation normalization to guillemets, ZWNJ fixes for common
    Persian affixes (می/نمی, ها/های, تر/ترین, etc.), and repeated character
    collapse.

    Args:
        text: Input Persian text to normalize.
        use_dictionary: If True, use a bundled 453K Persian word list to
            preserve legitimate doubled letters (e.g. الله, موسسه, تردد)
            when collapsing repeated characters. Default is False (simple
            collapse: 3+ repeated → single).

    Returns:
        Normalized Persian text.

    """
    # Normalize whitespace characters
    text = _SPACE_CHARS.sub(" ", text)

    # Remove keshide and carriage return
    text = re.sub(r"[ـ\r]", "", text)

    # Remove diacritics (harakat)
    text = _DIACRITICS.sub("", text)

    # Arabic → Persian character normalization
    for pattern, replacement in _ARABIC_TO_PERSIAN_CHARS:
        text = re.sub(pattern, replacement, text)

    # Convert digits to Persian
    text = convert_digits(text, to="fa")

    # Quotation normalization
    text = re.sub(r'"([^\n"]+)"', r"«\1»", text)
    text = re.sub(r"'([^\n\"]+)'", r"«\1»", text)
    text = re.sub(r'٬([^\n"]+)٬', r"«\1»", text)
    text = re.sub(r'《([^\n"]+)》', r"«\1»", text)

    # Decimal separator: digit.digit → digit٫digit
    text = re.sub(r"(\d)\.(\d)", r"\1٫\2", text)

    # Three dots → ellipsis
    text = re.sub(r" ?\.\.\.", " … ", text)

    # ZWNJ fixes for Persian affixes
    # ه ی → ه‌ی
    text = re.sub(r"([^ ]ه) ی ", "\\1\u200cی ", text)
    # می/نمی + space → می‌/نمی‌
    text = re.sub(r"(^| )(ن?می) ", "\\1\\2\u200c", text)
    # تر/ترین/گر/گری/ها/های
    text = re.sub(
        r"(?<=[^\n\d "
        + _PUNCT_AFTER
        + _PUNCT_BEFORE
        + r"]{2}) (تر(ین?)?|گری?|های?)(?=[ \n"
        + _PUNCT_AFTER
        + _PUNCT_BEFORE
        + r"]|$)",
        "\u200c\\1",
        text,
    )
    # ه + ام/ایم/اش/اند/ای/اید/ات
    text = re.sub(
        r"([^ ]ه) (ا(?:م|یم|ش|ند|ی|ید|ت))(?=[ \n" + _PUNCT_AFTER + r"]|$)",
        "\\1\u200c\\2",
        text,
    )

    # Remove space before/after quotation
    text = re.sub(r'" ([^\n"]+) "', r'"\1"', text)
    # Remove space before punctuation
    text = re.sub(r" ([" + _PUNCT_AFTER + r"])", r"\1", text)
    # Remove space after opening punctuation
    text = re.sub(r"([" + _PUNCT_BEFORE + r"]) ", r"\1", text)
    # Add space after . : !
    text = re.sub(
        r"([" + _PUNCT_AFTER[:3] + r"])([^ " + _PUNCT_AFTER + r"\w\d\\/۰۱۲۳۴۵۶۷۸۹])",
        r"\1 \2",
        text,
    )
    # Add space after other punctuation
    text = re.sub(
        r"([" + _PUNCT_AFTER[3:] + r"])([^ " + _PUNCT_AFTER + r"])",
        r"\1 \2",
        text,
    )
    # Add space before opening punctuation
    text = re.sub(
        r"([^ " + _PUNCT_BEFORE + r"])([" + _PUNCT_BEFORE + r"])",
        r"\1 \2",
        text,
    )

    # Collapse 3+ repeated Persian characters
    text = _collapse_repeated_chars(text, use_dictionary=use_dictionary)

    # Fix punctuation in English contexts (undo Persian punct in URLs/numbers)
    text = re.sub(r"([a-zA-Z]+)(؟ )", r"\1?", text)
    text = re.sub(r"([0-9]+)، ([0-9]+)", r"\1,\2", text)
    text = re.sub(r"([0-9]+)٫([0-9]+)", r"\1.\2", text)
    text = re.sub(r"([۰-۹]+)، ([۰-۹]+)", r"\1٫\2", text)

    return text


_PUNCTUATIONS = set("""!()-![]{};+'",<>.?@#$%\\^&*_~|=۔؟:«»؛ـ،٫/""")


def remove_punctuations(text: str) -> str:
    """Remove punctuation characters from text.

    Replaces / with space (to preserve word boundaries), then strips
    all other punctuation characters.

    Args:
        text: Input text containing punctuation.

    Returns:
        Text with punctuation removed.

    """
    text = text.replace("/", " ")
    return "".join(ch for ch in text if ch not in _PUNCTUATIONS)


def fix_multiple_punctuations(text: str) -> str:
    """Collapse repeated punctuation marks to a single instance.

    Handles: ، ؟ ? . !

    Args:
        text: Input text with potentially repeated punctuation.

    Returns:
        Text with repeated punctuation collapsed.

    """
    text = re.sub(r"،+", "،", text)
    text = re.sub(r"؟+", "؟", text)
    text = re.sub(r"\?+", "?", text)
    text = re.sub(r"\.+", ".", text)
    text = re.sub(r"!+", "!", text)
    return text


def remove_ellipsis(text: str) -> str:
    """Remove ellipsis characters from text.

    Args:
        text: Input text potentially containing ellipsis.

    Returns:
        Text with ellipsis characters removed.

    """
    return text.replace("…", "")


# --- Character set constants for strip_characters ---

_CHAR_RANGES: dict[str, str] = {
    "fa": r"ئآابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیچ۰۱۲۳۴۵۶۷۸۹",
    "ar": r"\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF",
    "en": r"a-zA-Z0-9",
    "he": r"\u0590-\u05FF",
}

_COMMON_CHARS = (
    r"×'\"\،*﷼٫!٪()\«»ـ+÷|{}\[\]:؛\.؟/<>…\\;"
    r"\u200c"  # zwnj
    r"\u202d\u202e\u202c\u202a\u202b"  # bidi control characters
    r"\u2010\u2212"  # hyphen and minus sign
    r"_ \n"
)


def strip_characters(text: str, keep: str | list[str] = "fa") -> str:
    """Remove characters not belonging to the specified language(s).

    Args:
        text: Input text to filter.
        keep: Language code(s) to keep. Single string or list of codes.
            Supported: "fa" (Persian), "ar" (Arabic), "en" (English), "he" (Hebrew).

    Returns:
        Text with only characters from the specified language(s) and common
        punctuation/whitespace preserved.

    """
    if isinstance(keep, str):
        keep = [keep]
    char_pattern = "".join(_CHAR_RANGES[lang] for lang in keep if lang in _CHAR_RANGES)
    pattern = re.compile(r"[^" + _COMMON_CHARS + char_pattern + r"]")
    return pattern.sub("", text)


def remove_extra_spaces(text: str) -> str:
    """Collapse multiple spaces into one and strip leading/trailing whitespace.

    Args:
        text: Input text with potentially extra whitespace.

    Returns:
        Text with normalized whitespace.

    """
    return re.sub(r" +", " ", text).strip()


# --- Step presets ---
PERSIAN_STEPS = [
    remove_links,
    remove_mentions,
    remove_hashtags,
    remove_emojis,
    normalize_persian,
    fix_multiple_punctuations,
    strip_characters,
    remove_extra_spaces,
]

MINIMAL_STEPS = [
    remove_links,
    remove_emojis,
    remove_extra_spaces,
]


def clean(text: str, steps: list | None = None) -> str:
    """Run a sequence of text processing steps.

    Each step is a callable that takes a string and returns a string.
    Steps are applied in order.

    Args:
        text: Input text to clean.
        steps: List of processing functions to apply. If None, uses
            PERSIAN_STEPS (the default Persian cleaning pipeline).

    Returns:
        Cleaned text after applying all steps.

    """
    if steps is None:
        steps = PERSIAN_STEPS
    for step in steps:
        text = step(text)
    return text
