import pytest

from threepio.envutils import generate_localization_file_name


@pytest.mark.parametrize('lang_code, pattern, expected', [
    ('en', '{language}.json', 'en.json'),
    ('fr', '{language}.xml', 'fr.xml'),
    ('de', 'messages_{language}.properties', 'messages_de.properties'),
    ('es', 'locale-{language}.txt', 'locale-es.txt'),
    ('it', '{language}_translations.yaml', 'it_translations.yaml'),
    ('ja', 'i18n-{language}.po', 'i18n-ja.po'),
    ('zh', 'strings_{language}.resx', 'strings_zh.resx'),
])
def test_generate_localization_file_name(lang_code, pattern, expected):
    actual = generate_localization_file_name(lang_code, pattern)
    assert actual == expected
