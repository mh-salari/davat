Davat(دوات)
====

A very simple python library for normalizing and cleaning Persian text.

+ Text Normalizing
+ Text Cleaning
+ Python 3.x support


## Usage

```python3
>>> import davat

>>> sample_text = "بِسْمِ اللَّهِ الرَّحْمنِ الرَّحِيمِ"

>>> davat.normalize(sample_text)
'بسم الله الرحمن الرحیم'

>>> sample_text = """این یك متن تست است که حروف عربي ، کشیـــــده 
'اعداد 12345' و... دارد     که می خواهیم آن را نرمالایز کنیم ."""

>>> print(davat.normalize(sample_text))
این یک متن تست است که حروف عربی، کشیده
«اعداد ۱۲۳۴۵» و …  دارد  که می‌خواهیم آن را نرمالایز کنیم.

>>> sample_text = """
... متنی برای برسی تابع تمیز کردن متن
... که #هشتگ_ها را خیلی عاااااللللییییی!!!! تبدیل به متن عادی می‌کند!
... منشن‌ها @mh_salari و لینک‌ها www.mh-salari.ir را حذف می‌کند.
... حروف غیر فارسی  a b c d و اموجی‌ها :( 🐈‍ را حذف می‌کند
... علائم دستوری/نگارشی ?!٫ را حذف نمی‌کند
... و ...
... http://localhost:8888
... """


>>> # davat.clean(
... #     text: str,
... #     remove_links=True,
... #     remove_mentions=True,
... #     remove_hashtags=False,
... #     remove_hashtag=True,
... #     remove_underline=True,
... #     remove_emojis=True,
... #     normalize_persian=True,
... #     remove_punctuations=False,
... #     fix_multiple_punctuations=True,
... #     remove_3dots=False,
... #     remove_non_persian_letters=True,
... #     remove_extraspaces=True,
... #)
... 


>>> text = davat.clean(sample_text)
>>> print(text)
متنی برای برسی تابع تمیز کردن متن 
 که هشتگ‌ها را خیلی عااللیی! تبدیل به متن عادی می‌کند! 
 منشن‌ها و لینک‌ها را حذف می‌کند. 
 حروف غیر فارسی و اموجی‌ها را حذف می‌کند 
 علائم دستوری/نگارشی؟!، را حذف نمی‌کند 
 و …

```


## Installation
The latest stable version of Davat can be installed through `pip`:

	pip install davat


## Thanks to:
+ [Persian poems corpus](https://github.com/amnghd/Persian_poems_corpus/blob/master/pers_alphab.py)
+ [Hazm](https://github.com/sobhe/hazm/blob/master/hazm/Normalizer.py)
+ [parsivar](https://github.com/ICTRC/Parsivar/blob/master/parsivar/normalizer.py)
