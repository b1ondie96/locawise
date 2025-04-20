import pytest

from src.threepio.errors import LocalizationFormatError
from src.threepio.localization.format import find_extension, LocalizationFormat, detect_format


@pytest.mark.parametrize('file_path, expected_extension', [
    ('hey.csv', 'csv'),
    ('hello.json', 'json'),
    ('rather_long_name_with_many_under_scores.txt', 'txt'),
    (' .csv', 'csv'),
    ('.csv', 'csv'),
    ('q12.prp', 'prp'),
    ('prp', ''),
    ('', ''),
    ('           ', ''),
    (' ', ''),
    ('www.facebook.com', 'com'),
    ('hello.csv.txt', 'txt'),
    ('frank.txt.csv', 'csv'),
    ('.gitignore.ignore.txt', 'txt'),
])
def test_find_suffix(file_path: str, expected_extension: str):
    actual = find_extension(file_path)
    assert actual == expected_extension


def test_detect_format_properties_file(mocker):
    find_suffix_mock = mocker.patch("src.threepio.localization.format.find_suffix")
    find_suffix_mock.return_value = "properties"

    assert detect_format("abc") == LocalizationFormat.PROPERTIES


@pytest.mark.parametrize('extension', [
    'j',
    'python',
    'json',
    'yaml',
    '',
    '        ',
    '',
    'csv',
    'aab',
])
def test_detect_format_invalid_file(extension: str, mocker):
    find_suffix_mock = mocker.patch("src.threepio.localization.format.find_suffix")
    find_suffix_mock.return_value = extension

    with pytest.raises(LocalizationFormatError):
        detect_format("anyfile")
