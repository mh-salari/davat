"""Tests for normalize_persian()."""

from davat import normalize_persian

ZWNJ = "\u200c"


# --- README examples ---


def test_readme_diacritics():
    result = normalize_persian("بِسْمِ اللَّهِ الرَّحْمنِ الرَّحِيمِ")
    assert result == "بسم الله الرحمن الرحیم"


def test_readme_mixed():
    text = """این یك متن تست است که حروف عربي ، کشیـــــده \n'اعداد 12345' و... دارد     که می خواهیم آن را نرمالایز کنیم ."""
    result = normalize_persian(text)
    assert "یک" in result  # Arabic ك → Persian ک
    assert "عربی" in result  # Arabic ي → Persian ی
    assert "کشیده" in result  # keshide removed
    assert "۱۲۳۴۵" in result  # digits converted
    assert "…" in result  # three dots → ellipsis
    assert f"می{ZWNJ}" in result  # zwnj after می


# --- Diacritics removal ---


def test_diacritics_fatha():
    assert "\u064e" not in normalize_persian("بَ")


def test_diacritics_kasra():
    assert "\u0650" not in normalize_persian("بِ")


def test_diacritics_damma():
    assert "\u064f" not in normalize_persian("بُ")


def test_diacritics_tanwin():
    assert "\u064b" not in normalize_persian("کتاباً")


def test_diacritics_shadda():
    assert "\u0651" not in normalize_persian("اللّه")


# --- Arabic → Persian character normalization ---


def test_arabic_yeh():
    assert normalize_persian("عربي") == "عربی"


def test_arabic_kaf():
    assert normalize_persian("كتاب") == "کتاب"


def test_arabic_alef_variants():
    result = normalize_persian("إسلام أحمد")
    assert "إ" not in result
    assert "أ" not in result
    assert "ا" in result


def test_arabic_taa_marbuta():
    result = normalize_persian("مدرسة")
    assert result == "مدرسه"


def test_arabic_waw():
    result = normalize_persian("ؤلاد")
    assert result == "ولاد"


# --- Digit conversion ---


def test_english_digits():
    assert "۱۲۳" in normalize_persian("عدد 123")


def test_arabic_digits():
    assert "۴۵۶" in normalize_persian("عدد ٤٥٦")


def test_mixed_digits():
    result = normalize_persian("٣ و 7")
    assert "۳" in result
    assert "۷" in result


# --- Keshide removal ---


def test_keshide_removed():
    result = normalize_persian("کشیـــده")
    assert "ـ" not in result
    assert "کشیده" in result


def test_single_keshide():
    assert "ـ" not in normalize_persian("سلاـم")


# --- Quotation normalization ---


def test_double_quotes_to_guillemets():
    assert "«سلام»" in normalize_persian('"سلام"')


def test_single_quotes_to_guillemets():
    assert "«سلام»" in normalize_persian("'سلام'")


def test_angle_brackets_to_guillemets():
    assert "«سلام»" in normalize_persian("《سلام》")


# --- Ellipsis ---


def test_three_dots_to_ellipsis():
    assert "…" in normalize_persian("و...")


def test_three_dots_with_space():
    assert "…" in normalize_persian("و ...")


# --- ZWNJ fixes ---


def test_zwnj_mi():
    result = normalize_persian("می خواهیم")
    assert f"می{ZWNJ}" in result


def test_zwnj_nemi():
    result = normalize_persian("نمی دانیم")
    assert f"نمی{ZWNJ}" in result


def test_zwnj_heh_yeh():
    result = normalize_persian("خانه ی ما")
    assert f"ه{ZWNJ}ی" in result


def test_zwnj_heh_am():
    result = normalize_persian("خانه ام")
    assert f"ه{ZWNJ}ا" in result


def test_zwnj_heh_ash():
    result = normalize_persian("خانه اش")
    assert f"ه{ZWNJ}ا" in result


def test_zwnj_ha():
    result = normalize_persian("کتاب ها")
    assert ZWNJ in result


def test_zwnj_tar():
    result = normalize_persian("بزرگ تر")
    assert ZWNJ in result


# --- Repeated character collapse (default: simple, no dictionary) ---


# -- Exaggerated text (3+ chars) collapsed to single --


def test_repeated_chars_collapsed():
    assert normalize_persian("عاااللللییییی") == "عالی"


def test_repeated_exclamatory():
    assert normalize_persian("خوووب") == "خوب"


def test_repeated_laughter():
    # Without dictionary: 3+ → single
    assert normalize_persian("ههههههه") == "ه"


def test_repeated_siin():
    assert normalize_persian("بسسسسیار") == "بسیار"


def test_repeated_vaay():
    assert normalize_persian("وااای") == "وای"


def test_repeated_nahh():
    # Without dictionary: 3+ → single
    assert normalize_persian("نهههه") == "نه"


def test_repeated_salam():
    assert normalize_persian("سلاااام") == "سلام"


def test_exaggerated_moassese_simple():
    # Without dictionary: 3+ → single (loses the legitimate double)
    assert normalize_persian("موسسسسسه") == "موسه"


def test_exaggerated_allah_simple():
    # Without dictionary: 3+ → single (loses the legitimate double)
    assert normalize_persian("اللله") == "اله"


def test_exaggerated_taraddod_simple():
    # Without dictionary: 3+ → single
    assert normalize_persian("تردددد") == "ترد"


def test_exaggerated_moqarrar_simple():
    assert normalize_persian("مقررر") == "مقر"


def test_exaggerated_adad_simple():
    assert normalize_persian("عددد") == "عد"


# -- Dictionary-aware collapse (use_dictionary=True) --


def test_dict_repeated_chars_collapsed():
    assert normalize_persian("عاااللللییییی", use_dictionary=True) == "عالی"


def test_dict_laughter():
    # هه is a real word → dictionary preserves the double
    assert normalize_persian("ههههههه", use_dictionary=True) == "هه"


def test_dict_nahh():
    # نهه is a real word → dictionary preserves the double
    assert normalize_persian("نهههه", use_dictionary=True) == "نهه"


def test_dict_exaggerated_moassese():
    # موسسه has legitimate سس
    assert normalize_persian("موسسسسسه", use_dictionary=True) == "موسسه"


def test_dict_exaggerated_allah():
    # الله has legitimate لل
    assert normalize_persian("اللله", use_dictionary=True) == "الله"


def test_dict_exaggerated_taraddod():
    assert normalize_persian("تردددد", use_dictionary=True) == "تردد"


def test_dict_exaggerated_moqarrar():
    assert normalize_persian("مقررر", use_dictionary=True) == "مقرر"


def test_dict_exaggerated_adad():
    assert normalize_persian("عددد", use_dictionary=True) == "عدد"


# -- Exactly 2 repeated chars preserved (legitimate doubles) --
# Arabic geminate roots (2nd=3rd radical) produce real doubled letters
# in standard Persian writing. These must NOT be collapsed.


def test_allah_preserved():
    assert normalize_persian("الله") == "الله"


def test_moassese_preserved():
    assert normalize_persian("موسسه") == "موسسه"


def test_moasses_preserved():
    # مؤسس (founder) - مؤ normalizes to مو
    assert "سس" in normalize_persian("مؤسس")


def test_zarar_preserved():
    assert normalize_persian("ضرر") == "ضرر"


def test_madad_preserved():
    assert normalize_persian("مدد") == "مدد"


def test_adad_preserved():
    assert normalize_persian("عدد") == "عدد"


def test_sharar_preserved():
    assert normalize_persian("شرر") == "شرر"


def test_taraddod_preserved():
    assert normalize_persian("تردد") == "تردد"


def test_taaddod_preserved():
    assert normalize_persian("تعدد") == "تعدد"


def test_tajaddod_preserved():
    assert normalize_persian("تجدد") == "تجدد"


def test_tamaddod_preserved():
    assert normalize_persian("تمدد") == "تمدد"


def test_moqarrar_preserved():
    assert normalize_persian("مقرر") == "مقرر"


def test_mokarrar_preserved():
    assert normalize_persian("مکرر") == "مکرر"


def test_mohaqqeq_preserved():
    assert normalize_persian("محقق") == "محقق"


def test_mosammam_preserved():
    assert normalize_persian("مصمم") == "مصمم"


def test_moallal_preserved():
    assert normalize_persian("معلل") == "معلل"


def test_motammem_preserved():
    assert normalize_persian("متمم") == "متمم"


# -- Shadda words: diacritic removed, single letter remains --


def test_shadda_bacche():
    assert normalize_persian("بچّه") == "بچه"


def test_shadda_naqqash():
    assert normalize_persian("نقّاش") == "نقاش"


def test_shadda_mohammad():
    assert normalize_persian("محمّد") == "محمد"


def test_shadda_darre():
    assert normalize_persian("درّه") == "دره"


def test_shadda_barre():
    assert normalize_persian("برّه") == "بره"


def test_shadda_tappe():
    assert normalize_persian("تپّه") == "تپه"


def test_shadda_pelle():
    assert normalize_persian("پلّه") == "پله"


def test_shadda_qolle():
    assert normalize_persian("قلّه") == "قله"


def test_shadda_najjar():
    assert normalize_persian("نجّار") == "نجار"


def test_shadda_avval():
    assert normalize_persian("اوّل") == "اول"


def test_shadda_tashakkor():
    assert normalize_persian("تشکّر") == "تشکر"


def test_single_chars_unchanged():
    assert normalize_persian("سلام") == "سلام"


# --- Punctuation spacing ---


def test_space_before_period_removed():
    result = normalize_persian("سلام .")
    assert " ." not in result


def test_no_space_after_period_before_word_char():
    result = normalize_persian("سلام.دنیا")
    # no space added after period before word characters (\w)
    assert ".د" in result


def test_space_added_after_period_before_non_word():
    result = normalize_persian("سلام.«دنیا»")
    # space added after period before non-word, non-space chars
    assert ". «" in result


# --- English context fixes ---


def test_english_question_mark_preserved():
    result = normalize_persian("example? test")
    assert "example?" in result


def test_english_comma_in_numbers():
    result = normalize_persian("1,234")
    assert "1,234" in result or "۱,۲۳۴" not in result


def test_english_dot_in_numbers():
    result = normalize_persian("3.14")
    assert "3.14" in result or "۳.۱۴" not in result


# --- Edge cases ---


def test_empty_string():
    assert normalize_persian("") == ""


def test_only_whitespace():
    result = normalize_persian("   ")
    assert result.strip() == "" or result == "   "


def test_already_normalized():
    text = "این یک متن ساده فارسی است"
    assert normalize_persian(text) == text


def test_carriage_return_removed():
    assert "\r" not in normalize_persian("سلام\rدنیا")


def test_non_breaking_space():
    result = normalize_persian("سلام\xa0دنیا")
    assert "\xa0" not in result
