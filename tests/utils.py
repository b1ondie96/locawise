import os

from threepio.regexutils import remove_all_whitespace


def get_absolute_path(file_path: str) -> str:
    return os.path.join(os.path.dirname(__file__), file_path)


def compare_ignoring_white_space(actual: str, expected: str):
    assert remove_all_whitespace(actual) == remove_all_whitespace(expected)
