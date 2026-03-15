# Davat (دوات)

[![PyPI version](https://img.shields.io/pypi/v/davat)](https://pypi.org/project/davat/)
[![Downloads](https://static.pepy.tech/badge/davat)](https://pepy.tech/project/davat)
[![License](https://img.shields.io/pypi/l/davat)](https://github.com/mh-salari/davat/blob/main/LICENSE)

A Python library for normalizing and cleaning Persian text. Composable, single-purpose functions that can be used individually or combined via a pipeline.

## Installation

```bash
pip install davat
```

## Quick start

```python
from davat import clean

text = """
متنی برای برسی تابع تمیز کردن متن
که #هشتگ_ها را خیلی عاااااللللییییی!!!! تبدیل به متن عادی می‌کند!
منشن‌ها @mh_salari و لینک‌ها www.mh-salari.ir را حذف می‌کند.
حروف غیر فارسی  a b c d و اموجی‌ها :( 🐈‍ را حذف می‌کند
علائم دستوری/نگارشی ?!٫ را حذف نمی‌کند
و ...
http://localhost:8888
"""

print(clean(text))
```

`clean()` applies the default Persian pipeline (`PERSIAN_STEPS`): remove links, mentions, hashtags, emojis, normalize Persian text, fix repeated punctuation, strip non-Persian characters, and collapse extra spaces.

## Normalize Persian text

```python
from davat import normalize_persian

>>> normalize_persian("بِسْمِ اللَّهِ الرَّحْمنِ الرَّحِيمِ")
'بسم الله الرحمن الرحیم'

>>> normalize_persian("این یك متن تست است که حروف عربي ، کشیـــــده \n'اعداد 12345' و... دارد     که می خواهیم آن را نرمالایز کنیم .")
"این یک متن تست است که حروف عربی، کشیده\n«اعداد ۱۲۳۴۵» و …  دارد  که می‌خواهیم آن را نرمالایز کنیم."
```

`normalize_persian()` handles: whitespace normalization, diacritic removal, keshide removal, Arabic-to-Persian character mapping, digit conversion, quotation normalization, ZWNJ fixes for common affixes (می/نمی, ها/های, تر/ترین, etc.), punctuation spacing, and repeated character collapse.

By default, exaggerated text like `عاااللللییییی` is collapsed to `عالی` (3+ repeated characters → single).

### Dictionary-aware repeated character collapse

Set `use_dictionary=True` to enable dictionary-aware collapse using a bundled 453K Persian word list. This preserves legitimate doubled letters in words like الله, موسسه, تردد:

```python
# Default (no dictionary): simple collapse, 3+ → single
>>> normalize_persian("اللله")
'اله'                     # loses the legitimate لل

# With dictionary: preserves legitimate doubles
>>> normalize_persian("اللله", use_dictionary=True)
'الله'                    # dictionary knows الله has لل

>>> normalize_persian("موسسسسسه", use_dictionary=True)
'موسسه'                   # dictionary knows موسسه has سس

>>> normalize_persian("تردددد", use_dictionary=True)
'تردد'                    # dictionary knows تردد has دد
```

**Tradeoff:** The dictionary lookup means some informal/slang words may not collapse to what you'd expect. For example, `نهههه` collapses to `نهه` (not `نه`) because `نهه` is a valid word in the dictionary. Similarly, `ههههههه` becomes `هه` because `هه` is a real word. This is the price of preserving legitimate doubles like الله, موسسه, تردد, محقق, etc. In practice, this is the better tradeoff since breaking real words (الله → اله) is worse than keeping an extra letter in slang text.

## Individual functions

Every function takes a string and returns a string. Use them independently:

```python
from davat import (
    convert_digits,
    remove_links,
    remove_mentions,
    remove_hashtags,
    remove_emojis,
    remove_markdown,
    normalize_persian,
    remove_punctuations,
    fix_multiple_punctuations,
    remove_ellipsis,
    strip_characters,
    remove_extra_spaces,
)

>>> remove_links("سلام https://example.com دنیا")
'سلام  دنیا'

>>> remove_mentions("سلام @user دنیا")
'سلام  دنیا'

>>> remove_hashtags("#سلام دنیا")
' سلام دنیا'

>>> remove_hashtags("#سلام دنیا", keep_text=False)
' دنیا'

>>> remove_emojis("سلام 😀 دنیا")
'سلام  دنیا'

>>> remove_markdown("**bold** and [link](http://x.com)")
'bold and link'

>>> convert_digits("123", to="fa")
'۱۲۳'

>>> convert_digits("۱۲۳", to="en")
'123'

>>> strip_characters("hello سلام world", keep="fa")
' سلام '

>>> strip_characters("hello سلام world", keep=["fa", "en"])
'hello سلام world'
```

## Custom pipelines

Build your own pipeline with `clean()` and `steps`:

```python
from functools import partial
from davat import clean, remove_links, remove_emojis, strip_characters, remove_extra_spaces

# Multilingual: keep Persian, English, and Arabic
steps = [
    remove_links,
    remove_emojis,
    partial(strip_characters, keep=["fa", "en", "ar"]),
    remove_extra_spaces,
]

>>> clean("hello سلام مرحبا https://x.com 😀 שלום", steps=steps)
'hello سلام مرحبا'
```

### Preset pipelines

```python
from davat import PERSIAN_STEPS, MINIMAL_STEPS

# PERSIAN_STEPS (default): full Persian cleaning pipeline
# MINIMAL_STEPS: just remove links, emojis, and extra spaces

>>> clean("سلام https://x.com 😀 hello", steps=MINIMAL_STEPS)
'سلام  hello'  # minimal doesn't strip non-Persian
```

## Thanks to

- [Persian-Words-Database](https://github.com/shahind/Persian-Words-Database) for the Persian word list
- [Persian poems corpus](https://github.com/amnghd/Persian_poems_corpus)
- [Hazm](https://github.com/sobhe/hazm)
- [Parsivar](https://github.com/ICTRC/Parsivar)
