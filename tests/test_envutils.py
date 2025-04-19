import pytest

from src.threepio.envutils import generate_localization_file_name_without_extension, generate_localization_file_name


@pytest.mark.parametrize('lang_code, pattern, expected', [
    ('en', '{language}.{ext}', 'en.{ext}'),
    ('fr', '{language}.{ext}', 'fr.{ext}'),
    ('en', 'messages_{language}.{ext}', 'messages_en.{ext}'),
    ('en', 'messages_{language}.ext', 'messages_en.ext'),
    ('en', '{messages}_{language}.{ext}', '{messages}_en.{ext}'),

])
def test_generate_localization_file_name_without_extension(lang_code, pattern, expected):
    actual = generate_localization_file_name_without_extension(lang_code, pattern)
    assert actual == expected


@pytest.mark.parametrize('lang_code, pattern, extension, expected', [
    ('en', '{language}.{ext}', 'json', 'en.json'),
    ('fr', '{language}.{ext}', 'xml', 'fr.xml'),
    ('de', 'messages_{language}.{ext}', 'properties', 'messages_de.properties'),
    ('es', 'locale-{language}.{ext}', 'txt', 'locale-es.txt'),
    ('it', '{language}_translations.{ext}', 'yaml', 'it_translations.yaml'),
    ('ja', 'i18n-{language}.{ext}', 'po', 'i18n-ja.po'),
    ('zh', 'strings_{language}.{ext}', 'resx', 'strings_zh.resx'),
])
def test_generate_localization_file_name(lang_code, pattern, extension, expected):
    actual = generate_localization_file_name(lang_code, pattern, extension)
    assert actual == expected
