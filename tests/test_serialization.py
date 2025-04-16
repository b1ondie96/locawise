from src.threepio.localization_format import LocalizationFormat
from src.threepio.serialization import serialize_to_properties_format, serialize


def test_serialize_properties_format(mocker):
    input_map = {'name': 'hey'}
    localization_format = LocalizationFormat.PROPERTIES
    mock = mocker.patch('src.threepio.serialization.serialize_to_properties_format')

    serialize(input_map, localization_format)

    mock.assert_called_with(input_map)


def test_serialize_to_properties_format_empty_dict():
    input_map = {}
    result = serialize_to_properties_format(input_map)

    assert result == ''


def test_serialize_to_properties_format_single_pair():
    input_map = {'name': 'jordan'}

    result = serialize_to_properties_format(input_map)
    assert result == 'name=jordan\n'


def test_serialize_to_properties_format_multiple_pairs():
    input_map = {
        'age': '19',
        'message': 'I love world',
        'location': 'frankfurt  ',
        'distance': '150',
        'presence': '',
    }

    result = serialize_to_properties_format(input_map)
    assert result == 'age=19\nmessage=I love world\nlocation=frankfurt  \ndistance=150\npresence=\n'
