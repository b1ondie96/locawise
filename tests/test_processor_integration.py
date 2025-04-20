import os

import pytest
from aiofiles import tempfile

from src.threepio.fileutils import read_file, write_to_file
from src.threepio.llm import MockLLMStrategy, LLMContext
from src.threepio.processor import SourceProcessor


@pytest.fixture
def source_processor():
    llm_strategy = MockLLMStrategy()
    llm_context = LLMContext(llm_strategy)
    source_dict = {
        'key1': 'value1',
        'key2': 'value2',
        'key3': 'value3',
        'key4': 'value4',
        'key5': 'value5',
    }
    return SourceProcessor(llm_context=llm_context, source_dict=source_dict, nom_keys=set())


@pytest.mark.asyncio
async def test_localize_to_target_language_empty_target_path_empty_lock_file(source_processor):
    async with tempfile.TemporaryDirectory() as temp_dir:
        target_path = os.path.join(temp_dir, "test_localization.properties")
        await source_processor.localize_to_target_language(target_path, 'tr')
        content = await read_file(target_path)

        expected = """key1=TRANSLATED_value1
key2=TRANSLATED_value2
key3=TRANSLATED_value3
key4=TRANSLATED_value4
key5=TRANSLATED_value5
"""
        assert content == expected


@pytest.mark.asyncio
async def test_localize_to_target_language_existing_target_path_empty_lock_file(source_processor: SourceProcessor):
    async with tempfile.TemporaryDirectory() as temp_dir:
        target_path = os.path.join(temp_dir, "test_localization.properties")

        existing_target_content = '''key1=Hello
key2=Hiya
'''

        await write_to_file(target_path, existing_target_content)
        await source_processor.localize_to_target_language(target_path, 'tr')
        content = await read_file(target_path)

        expected = """key1=Hello
key2=Hiya
key3=TRANSLATED_value3
key4=TRANSLATED_value4
key5=TRANSLATED_value5
"""
        assert content == expected


@pytest.mark.asyncio
async def test_localize_to_target_language_existing_target_path_existing_lock_file(source_processor):
    async with tempfile.TemporaryDirectory() as temp_dir:
        target_path = os.path.join(temp_dir, "test_localization.properties")

        existing_target_content = '''key1=Hello
key2=Hiya
'''

        await write_to_file(target_path, existing_target_content)

        source_processor.nom_keys = {'key1', 'key2'}

        await source_processor.localize_to_target_language(target_path, 'tr')
        content = await read_file(target_path)

        expected = """key1=TRANSLATED_value1
key2=TRANSLATED_value2
key3=TRANSLATED_value3
key4=TRANSLATED_value4
key5=TRANSLATED_value5
"""

        assert content == expected


@pytest.mark.asyncio
async def test_localize_to_target_language_invalid_target_lang_code(source_processor):
    with pytest.raises(ValueError):
        await source_processor.localize_to_target_language('', 'tren')
