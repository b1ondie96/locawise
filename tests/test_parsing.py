import pytest

from threepio.parsing import parse_java_properties_file, read_file
from tests.parsing_fixtures import expected_dict_for_default_java_properties
from tests.parsing_fixtures import expected_dict_for_multiline_java_properties
from tests.parsing_fixtures import expected_dict_for_special_characters_java_properties
from tests.utils import get_absolute_path


@pytest.mark.asyncio(loop_scope="module")
async def test_java_properties_with_equals_parsing(expected_dict_for_default_java_properties: dict[str, str]):
    absolute_path = get_absolute_path("resources/properties/default_with_equals.properties")
    file_content = await read_file(absolute_path)
    properties = await parse_java_properties_file(file_content)

    assert len(properties) == len(expected_dict_for_default_java_properties)
    assert properties == expected_dict_for_default_java_properties


@pytest.mark.asyncio(loop_scope="module")
async def test_java_properties_with_colons__parsing(expected_dict_for_default_java_properties: dict[str, str]):
    absolute_path = get_absolute_path("resources/properties/default_with_colon.properties")
    file_content = await read_file(absolute_path)
    properties = await parse_java_properties_file(file_content)

    assert len(properties) == len(expected_dict_for_default_java_properties)
    assert properties == expected_dict_for_default_java_properties


@pytest.mark.asyncio(loop_scope="module")
async def test_java_properties_with_special_characters_parsing(
        expected_dict_for_special_characters_java_properties: dict[str, str]):
    absolute_path = get_absolute_path("resources/properties/special_characters.properties")
    file_content = await read_file(absolute_path)
    properties = await parse_java_properties_file(file_content)

    assert len(properties) == len(expected_dict_for_special_characters_java_properties)
    assert properties == expected_dict_for_special_characters_java_properties


@pytest.mark.asyncio(loop_scope="module")
async def test_java_properties_with_multiline_parsing(
        expected_dict_for_multiline_java_properties: dict[str, str]):
    absolute_path = get_absolute_path("resources/properties/multiline.properties")
    file_content = await read_file(absolute_path)
    properties = await parse_java_properties_file(file_content)

    assert len(properties) == len(expected_dict_for_multiline_java_properties)
    assert properties == expected_dict_for_multiline_java_properties
