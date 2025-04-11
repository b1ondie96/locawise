import pytest

from src.threepio.parsing import parse_java_properties_file
from tests.parsing_fixtures import expected_dict_for_default_java_properties
from tests.parsing_fixtures import expected_dict_for_multiline_java_properties
from tests.parsing_fixtures import expected_dict_for_special_characters_java_properties
from tests.utils import get_absolute_path


@pytest.mark.asyncio(loop_scope="module")
async def test_java_properties_with_equals_parsing(expected_dict_for_default_java_properties: dict[str, str]):
    properties = await parse_java_properties_file(get_absolute_path("resources/default_with_equals.properties"))

    assert len(properties) == len(expected_dict_for_default_java_properties)
    assert properties == expected_dict_for_default_java_properties


@pytest.mark.asyncio(loop_scope="module")
async def test_java_properties_with_colons__parsing(expected_dict_for_default_java_properties: dict[str, str]):
    properties = await parse_java_properties_file(get_absolute_path("resources/default_with_colon.properties"))

    assert len(properties) == len(expected_dict_for_default_java_properties)
    assert properties == expected_dict_for_default_java_properties


@pytest.mark.asyncio(loop_scope="module")
async def test_java_properties_with_special_characters_parsing(
        expected_dict_for_special_characters_java_properties: dict[str, str]):
    properties = await parse_java_properties_file(get_absolute_path("resources/special_characters.properties"))

    assert len(properties) == len(expected_dict_for_special_characters_java_properties)
    assert properties == expected_dict_for_special_characters_java_properties


@pytest.mark.asyncio(loop_scope="module")
async def test_java_properties_with_multiline_parsing(
        expected_dict_for_multiline_java_properties: dict[str, str]):
    properties = await parse_java_properties_file(get_absolute_path("resources/multiline.properties"))

    assert len(properties) == len(expected_dict_for_multiline_java_properties)
    assert properties == expected_dict_for_multiline_java_properties
