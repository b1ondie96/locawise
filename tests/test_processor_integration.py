import json
import os

import pytest
from aiofiles import tempfile

from threepio.fileutils import read_file, write_to_file
from threepio.llm import MockLLMStrategy, LLMContext
from threepio.processor import SourceProcessor


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


@pytest.mark.asyncio
async def test_localize_to_target_language_empty_target_path_empty_lock_file_json(source_processor):
    async with tempfile.TemporaryDirectory() as temp_dir:
        target_path = os.path.join(temp_dir, "test_localization.json")
        await source_processor.localize_to_target_language(target_path, 'tr')
        content = await read_file(target_path)

        # Parse JSON content
        json_content = json.loads(content)
        expected = {
            "key1": "TRANSLATED_value1",
            "key2": "TRANSLATED_value2",
            "key3": "TRANSLATED_value3",
            "key4": "TRANSLATED_value4",
            "key5": "TRANSLATED_value5"
        }

        assert json_content == expected


@pytest.mark.asyncio
async def test_localize_to_target_language_existing_target_path_empty_lock_file_json(source_processor: SourceProcessor):
    async with tempfile.TemporaryDirectory() as temp_dir:
        target_path = os.path.join(temp_dir, "test_localization.json")

        existing_target_content = json.dumps({
            "key1": "Hello",
            "key2": "Hiya"
        }, indent=2)

        await write_to_file(target_path, existing_target_content)
        await source_processor.localize_to_target_language(target_path, 'tr')
        content = await read_file(target_path)

        json_content = json.loads(content)
        expected = {
            "key1": "Hello",
            "key2": "Hiya",
            "key3": "TRANSLATED_value3",
            "key4": "TRANSLATED_value4",
            "key5": "TRANSLATED_value5"
        }

        assert json_content == expected


@pytest.mark.asyncio
async def test_localize_to_target_language_existing_target_path_existing_lock_file_json(source_processor):
    async with tempfile.TemporaryDirectory() as temp_dir:
        target_path = os.path.join(temp_dir, "test_localization.json")

        existing_target_content = json.dumps({
            "key1": "Hello",
            "key2": "Hiya"
        }, indent=2)

        await write_to_file(target_path, existing_target_content)

        source_processor.nom_keys = {'key1', 'key2'}

        await source_processor.localize_to_target_language(target_path, 'tr')
        content = await read_file(target_path)

        json_content = json.loads(content)
        expected = {
            "key1": "TRANSLATED_value1",
            "key2": "TRANSLATED_value2",
            "key3": "TRANSLATED_value3",
            "key4": "TRANSLATED_value4",
            "key5": "TRANSLATED_value5"
        }

        assert json_content == expected


@pytest.mark.asyncio
async def test_localize_to_target_language_nested_json():
    # Create a source processor with nested structure
    llm_strategy = MockLLMStrategy()
    llm_context = LLMContext(llm_strategy)
    nested_source_dict = {
        'general_/app_name': 'value1',
        'general_/welcome': 'value2',
        'navigation_/home': 'value3',
        'navigation_/settings': 'value4',
        "footer": "value5"
    }

    nested_processor = SourceProcessor(
        llm_context=llm_context,
        source_dict=nested_source_dict,
        nom_keys=set()
    )

    async with tempfile.TemporaryDirectory() as temp_dir:
        target_path = os.path.join(temp_dir, "test_nested_localization.json")
        await nested_processor.localize_to_target_language(target_path, 'tr')
        content = await read_file(target_path)

        json_content = json.loads(content)
        expected = {
            "general": {
                "app_name": "TRANSLATED_value1",
                "welcome": "TRANSLATED_value2"
            },
            "navigation": {
                "home": "TRANSLATED_value3",
                "settings": "TRANSLATED_value4"
            },
            "footer": "TRANSLATED_value5"
        }

        assert json_content == expected


@pytest.mark.asyncio
async def test_localize_to_target_language_partial_nested_json(source_processor):
    # Create a source processor with nested structure
    llm_strategy = MockLLMStrategy()
    llm_context = LLMContext(llm_strategy)
    nested_source_dict = {
        'general_/app_name': 'value1',
        'general_/welcome': 'value2',
        'navigation_/home': 'value3',
        'navigation_/settings': 'value4',
    }

    nested_processor = SourceProcessor(
        llm_context=llm_context,
        source_dict=nested_source_dict,
        nom_keys=set()
    )

    async with tempfile.TemporaryDirectory() as temp_dir:
        target_path = os.path.join(temp_dir, "test_partial_nested_localization.json")

        # Create existing partial translation
        existing_content = {
            "general": {
                "app_name": "Existing App Name",
                "welcome": "Existing Welcome"
            }
        }

        await write_to_file(target_path, json.dumps(existing_content, indent=2))
        await nested_processor.localize_to_target_language(target_path, 'tr')
        content = await read_file(target_path)

        json_content = json.loads(content)
        expected = {
            "general": {
                "app_name": "Existing App Name",
                "welcome": "Existing Welcome"
            },
            "navigation": {
                "home": "TRANSLATED_value3",
                "settings": "TRANSLATED_value4"
            }
        }

        assert json_content == expected
