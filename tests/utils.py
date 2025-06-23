import os

from locawise.androidutils import parse_xml_string
from locawise.fileutils import read_file
from locawise.regexutils import remove_all_whitespace


def get_absolute_path(file_path: str) -> str:
    return os.path.join(os.path.dirname(__file__), file_path)


def compare_ignoring_white_space(actual: str, expected: str):
    assert remove_all_whitespace(actual) == remove_all_whitespace(expected)


def compare_collapsing_tabs_and_new_lines(actual: str, expected: str):
    assert collapse_tabs_and_new_lines(actual) == collapse_tabs_and_new_lines(expected)


def collapse_tabs_and_new_lines(text):
    # Replace all tabs and newlines with empty strings
    result = text.replace('\t', '').replace('\n', '')

    return result


async def parse_xml_file(file_path: str) -> dict[str, str]:
    """
    Reads an XML file and returns its content as a string.
    :param file_path: Path to the XML file.
    :return: Content of the XML file as a string.
    """

    file_content = await read_file(file_path)
    return parse_xml_string(file_content)
