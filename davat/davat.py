#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Apr 24 2020
@author: MohammadHossein Salari
Source:
      - https://github.com/amnghd/Persian_poems_corpus/blob/master/pers_alphab.py
      - https://github.com/sobhe/hazm/blob/master/hazm/Normalizer.py
      - https://github.com/ICTRC/Parsivar/blob/master/parsivar/normalizer.py
      - https://stackoverflow.com/questions/38804425/remove-urls-from-a-text-file
      - https://stackoverflow.com/questions/51784964/remove-emojis-from-multilingual-unicode-text
"""
import re
import emoji


def normalize(text: str, convert_digits=True) -> str:
    """
    Summary:


    Arguments:
        text [type:string]

    Returns:
        normalized text [type:string]
    """

    # replacing all spaces,hyphens,... with white space
    space_pattern = (
        r"[\xad\ufeff\u200e\u200d\u200b\x7f\u202a\u2003\xa0\u206e\u200c\x9d]"
    )
    space_pattern = re.compile(space_pattern)
    text = space_pattern.sub(" ", text)

    # remove keshide,
    text = re.sub(r"[ـ\r]", "", text)

    # remove Aarab
    text = re.sub(r"[\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652]", "", text)

    # replace arabic alphabets with equivalent persian alphabet
    regex_list = [
        (r"ء", r"ئ"),
        (r"ﺁ|آ", r"آ"),
        (r"ٲ|ٱ|إ|ﺍ|أ", r"ا"),
        (r"ﺐ|ﺏ|ﺑ", r"ب"),
        (r"ﭖ|ﭗ|ﭙ|ﺒ|ﭘ", r"پ"),
        (r"ﭡ|ٺ|ٹ|ﭞ|ٿ|ټ|ﺕ|ﺗ|ﺖ|ﺘ", r"ت"),
        (r"ﺙ|ﺛ", r"ث"),
        (r"ﺝ|ڃ|ﺠ|ﺟ", r"ج"),
        (r"ڃ|ﭽ|ﭼ", r"چ"),
        (r"ﺢ|ﺤ|څ|ځ|ﺣ", r"ح"),
        (r"ﺥ|ﺦ|ﺨ|ﺧ", r"خ"),
        (r"ڏ|ډ|ﺪ|ﺩ", r"د"),
        (r"ﺫ|ﺬ|ﻧ", r"ذ"),
        (r"ڙ|ڗ|ڒ|ڑ|ڕ|ﺭ|ﺮ", r"ر"),
        (r"ﺰ|ﺯ", r"ز"),
        (r"ﮊ", r"ژ"),
        (r"ݭ|ݜ|ﺱ|ﺲ|ښ|ﺴ|ﺳ", r"س"),
        (r"ﺵ|ﺶ|ﺸ|ﺷ", r"ش"),
        (r"ﺺ|ﺼ|ﺻ", r"ص"),
        (r"ﺽ|ﺾ|ﺿ|ﻀ", r"ض"),
        (r"ﻁ|ﻂ|ﻃ|ﻄ", r"ط"),
        (r"ﻆ|ﻇ|ﻈ", r"ظ"),
        (r"ڠ|ﻉ|ﻊ|ﻋ", r"ع"),
        (r"ﻎ|ۼ|ﻍ|ﻐ|ﻏ", r"غ"),
        (r"ﻒ|ﻑ|ﻔ|ﻓ", r"ف"),
        (r"ﻕ|ڤ|ﻖ|ﻗ", r"ق"),
        (r"ڭ|ﻚ|ﮎ|ﻜ|ﮏ|ګ|ﻛ|ﮑ|ﮐ|ڪ|ك", r"ک"),
        (r"ﮚ|ﮒ|ﮓ|ﮕ|ﮔ", r"گ"),
        (r"ﻝ|ﻞ|ﻠ|ڵ", r"ل"),
        (r"ﻡ|ﻤ|ﻢ|ﻣ", r"م"),
        (r"ڼ|ﻦ|ﻥ|ﻨ", r"ن"),
        (r"ވ|ﯙ|ۈ|ۋ|ﺆ|ۊ|ۇ|ۏ|ۅ|ۉ|ﻭ|ﻮ|ؤ", r"و"),
        (r"ﺔ|ﻬ|ھ|ﻩ|ﻫ|ﻪ|ۀ|ە|ة|ہ", r"ه"),
        (r"ﭛ|ﻯ|ۍ|ﻰ|ﻱ|ﻲ|ں|ﻳ|ﻴ|ﯼ|ې|ﯽ|ﯾ|ﯿ|ێ|ے|ى|ي", r"ی"),
        (r"¬", r"‌"),
        (r"•|·|●|·|・|∙|｡|ⴰ", r"."),
        (r",|٬|٫|‚|，", r"،"),
        (r"ʕ|\?", r"؟"),
        (r"|ِ||ُ||َ||ٍ||ٌ||ً", r""),
    ]

    for pattern, replac in regex_list:
        text = re.sub(pattern, replac, text)

    # replace arabic and english digits with equivalent persian digits
    num_dict = dict()
    if convert_digits:
        num_dict[u"0"] = u"۰"
        num_dict[u"1"] = u"۱"
        num_dict[u"2"] = u"۲"
        num_dict[u"3"] = u"۳"
        num_dict[u"4"] = u"۴"
        num_dict[u"5"] = u"۵"
        num_dict[u"6"] = u"۶"
        num_dict[u"7"] = u"۷"
        num_dict[u"8"] = u"۸"
        num_dict[u"9"] = u"۹"
        num_dict[u"%"] = u"٪"

    num_dict[u"٠"] = u"۰"
    num_dict[u"١"] = u"۱"
    num_dict[u"٢"] = u"۲"
    num_dict[u"٣"] = u"۳"
    num_dict[u"٤"] = u"۴"
    num_dict[u"٥"] = u"۵"
    num_dict[u"٦"] = u"۶"
    num_dict[u"٧"] = u"۷"
    num_dict[u"٨"] = u"۸"
    num_dict[u"٩"] = u"۹"

    num_pattern = re.compile(r"(" + "|".join(num_dict.keys()) + r")")
    text = num_pattern.sub(lambda x: num_dict[x.group()], text)

    punctuation_after, punctuation_before = r"\.:!،؛؟»\]\)\}", r"«\[\(\{"

    regex_list = [
        # replace quotation with «»
        ('"([^\n"]+)"', r"«\1»"),
        # replace single quotation with «»
        ("'([^\n\"]+)'", r"«\1»"),
        # replace ٬ with «»
        ('٬([^\n"]+)٬', r"«\1»"),
        # replace Double Angle Bracket with «»
        ('《([^\n"]+)》', r"«\1»"),
        # replace dot with momayez
        ("([\d+])\.([\d+])", r"\1٫\2"),
        # replace 3 dots
        (r" ?\.\.\.", " … "),
        # fix ی space
        (r"([^ ]ه) ی ", r"\1‌ی "),
        # put zwnj after می, نمی
        (r"(^| )(ن?می) ", r"\1\2‌"),
        # put zwnj before تر, تری, ترین, گر, گری, ها, های
        (
            r"(?<=[^\n\d "
            + punctuation_after
            + punctuation_before
            + "]{2}) (تر(ین?)?|گری?|های?)(?=[ \n"
            + punctuation_after
            + punctuation_before
            + "]|$)",
            r"‌\1",
        ),
        # join ام, ایم, اش, اند, ای, اید, ات
        (
            r"([^ ]ه) (ا(م|یم|ش|ند|ی|ید|ت))(?=[ \n" + punctuation_after + "]|$)",
            r"\1‌\2",
        ),
        # remove space before and after quotation
        ('" ([^\n"]+) "', r'"\1"'),
        # remove space before punctuations
        (" ([" + punctuation_after + "])", r"\1"),
        # remove space after punctuations
        ("([" + punctuation_before + "]) ", r"\1"),
        # put space after . and :
        (
            "(["
            + punctuation_after[:3]
            + "])([^ "
            + punctuation_after
            + "\d۰۱۲۳۴۵۶۷۸۹])",
            r"\1 \2",
        ),
        # put space after punctuation
        (
            "([" + punctuation_after[3:] + "])([^ " + punctuation_after + "])",
            r"\1 \2",
        ),
        # put space before punctuations
        (
            "([^ " + punctuation_before + "])([" + punctuation_before + "])",
            r"\1 \2",
        ),
        # Remove repeating characters (keep 2 repeats)
        (r"(.)\1+", r"\1\1"),
    ]

    for pattern, replac in regex_list:
        text = re.sub(pattern, replac, text)

    return text


def clean(
    text: str,
    remove_links=True,
    remove_mentions=True,
    remove_hashtags=False,
    remove_hashtag=True,
    remove_underline=True,
    remove_emojis=True,
    normalize_persian=True,
    remove_punctuations=False,
    fix_multiple_punctuations=True,
    remove_3dots=False,
    remove_non_persian_letters=True,
    remove_extraspaces=True,
) -> str:
    """
    Summary:


    Arguments:
        text [type:string]

    Returns:
        cleaned Persian text [type:string]
    """
    if remove_links:
        # replace persian and arabic digits with equivalent englis digits
        num_dict = dict()
        num_dict[u"۰"] = u"0"
        num_dict[u"۱"] = u"1"
        num_dict[u"۲"] = u"2"
        num_dict[u"۳"] = u"3"
        num_dict[u"۴"] = u"4"
        num_dict[u"۵"] = u"5"
        num_dict[u"۶"] = u"6"
        num_dict[u"۷"] = u"7"
        num_dict[u"۸"] = u"8"
        num_dict[u"۹"] = u"9"

        num_dict[u"٠"] = u"0"
        num_dict[u"١"] = u"1"
        num_dict[u"٢"] = u"2"
        num_dict[u"٣"] = u"3"
        num_dict[u"٤"] = u"4"
        num_dict[u"٥"] = u"5"
        num_dict[u"٦"] = u"6"
        num_dict[u"٧"] = u"7"
        num_dict[u"٨"] = u"8"
        num_dict[u"٩"] = u"9"

        num_dict[u"٪"] = u"%"
        num_dict[u"؟"] = u"?"

        num_pattern = re.compile(r"(" + "|".join(num_dict.keys()) + r")")
        text = num_pattern.sub(lambda x: num_dict[x.group()], text)

        # Remove links
        text = re.sub(
            r"""(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""",
            "",
            text,
        )

    if remove_mentions:
        # Remove mentions
        words = []
        for word in re.findall(r"\S+|\n", text):
            if word:
                if word[0] != "@":
                    words.append(word)
        text = " ".join(words)

    if remove_hashtags:
        # Remove hashtags
        words = []
        for word in re.findall(r"\S+|\n", text):
            if word:
                if word[0] != "#":
                    words.append(word)
        text = " ".join(words)

    if remove_hashtag:
        # Remove hashtags
        text = text.replace("#", " ")

    if remove_underline:
        # Remove _
        text = text.replace("_", " ")

    if remove_emojis:
        # Remove emojis
        text = emoji.get_emoji_regexp().sub(u"", text)

        text = (
            text.replace(":(", "")
            .replace(":)", "")
            .replace(": (", "")
            .replace(": )", "")
        )
        text = text.replace(":|", "").replace(": |", "")

    if normalize_persian:
        # Normalize Perian words
        text = normalize(text)

    if remove_punctuations:
        # Remove punctuations
        punctuations = """!()-![]{};+'",<>?@#$%\^&*_~|=۔؟:«»؛ـ،٫"""
        text = text.replace("/", " ")
        text = "".join([i for i in text if not i in punctuations])

    if fix_multiple_punctuations:
        # replace multiple punctuations
        regex_list = [
            (r"،+(?=،)", ""),
            (r"؟+(?=؟)", ""),
            (r"\?+(?=\?)", ""),
            (r"\.+(?=\.)", ""),
            (r"\!+(?=\!)", ""),
        ]

        for pattern, replac in regex_list:
            text = re.sub(pattern, replac, text)

    if remove_3dots:
        # Remove …
        text = text.replace("…", "")

    if remove_non_persian_letters:
        # Remove non-Persian letters
        pattern = r"[^×'\"\،*﷼٫!٪(\)\«»ـ+÷|\{}\[\]:؛\.؟/<>…\\;‭‮‬‪‫‐−_ ‌۰۱۲۳۴۵۶۷۸۹ئآابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیچ\n]"
        text = re.sub(pattern, "", text)

    # Fix orphan ":"
    if text:
        if text[-1] == ":":
            text = text[-1] + "."
        if text[0] == ":":
            text = text[1:]
    if remove_extraspaces:
        # Remove extra spaces
        text = re.sub(" +", " ", text).strip()

    # Return cleaned data
    return text
