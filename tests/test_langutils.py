import pytest

from locawise.langutils import is_valid_two_letter_lang_code, retrieve_lang_full_name


@pytest.mark.parametrize('lang_code, expected', [
    ('tr', True),
    ('en', True),
    ('fr', True),
    ('de', True),
    ('es', True),
    ('eso', False),
    ('try', False),
    ('qwq', False),
    ('', False),
    (' ', False),
    ('tr ', False),
])
def test_is_valid_two_letter_lang_code(lang_code, expected):
    actual = is_valid_two_letter_lang_code(lang_code)
    assert actual == expected


@pytest.mark.parametrize('lang_code, expected', [
    ('tr', 'Turkish'),
    ('en', 'English'),
    ('fr', 'French'),
    ('de', 'German'),
])
def test_retrieve_lang_full_name(lang_code, expected):
    actual = retrieve_lang_full_name(lang_code)
    assert actual == expected
