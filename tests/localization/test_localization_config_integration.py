import pytest

from locawise.errors import InvalidYamlConfigError
from locawise.localization.config import read_localization_config_yaml, LocalizationConfig
from tests.utils import get_absolute_path

DEFAULT_GLOSSARY = {'key1': 'value1', 'key2': 'value2'}


@pytest.mark.asyncio(loop_scope='module')
@pytest.mark.parametrize('file_path, expected', [
    ('resources/localizationconfigs/config_with_missing_values.yaml',
     LocalizationConfig(version='v1.0', context='', glossary=DEFAULT_GLOSSARY, tone='', source_lang_code='en',
                        target_lang_codes={'fr', 'de', 'es', })),

    ('resources/localizationconfigs/config_with_all_values.yaml',
     LocalizationConfig(version='v1.0', context='You work for a finance company', glossary=DEFAULT_GLOSSARY,
                        tone='Be as kind as possible', source_lang_code='tr', target_lang_codes={'fr'})),

])
async def test_read_localization_config_yaml_yaml_with_missing_values(file_path: str, expected: LocalizationConfig):
    path = get_absolute_path(file_path)
    result = await read_localization_config_yaml(path)

    assert expected == result


@pytest.mark.asyncio(loop_scope='module')
async def test_read_localization_config_yaml_invalid_yaml():
    with pytest.raises(InvalidYamlConfigError):
        path = get_absolute_path('resources/localizationconfigs/invalid.yaml')
        await read_localization_config_yaml(path)


@pytest.mark.asyncio(loop_scope='module')
async def test_read_localization_config_yaml_invalid_language_code_yaml():
    with pytest.raises(InvalidYamlConfigError):
        path = get_absolute_path('resources/localizationconfigs/invalid_lang_code.yaml')
        await read_localization_config_yaml(path)
