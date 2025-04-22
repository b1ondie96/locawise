from threepio.localization.format import LocalizationFormat
from threepio.serialization import serialize_to_properties_format, serialize


def test_serialize_properties_format(mocker):
    input_map = {'name': 'hey'}
    localization_format = LocalizationFormat.PROPERTIES
    mock = mocker.patch('threepio.serialization.serialize_to_properties_format')

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
    assert result == 'age=19\ndistance=150\nlocation=frankfurt  \nmessage=I love world\npresence=\n'


def test_serialize_to_properties_format_multilines():
    input_map = {
        'description': 'This is a test\nwith multiple lines',
        'message': 'Long message\nwith new lines\nMany lines\n',
        'location': 'frankfurt  ',
    }
    expected = """description=This is a test\\nwith multiple lines
location=frankfurt  
message=Long message\\nwith new lines\\nMany lines\\n
"""

    result = serialize_to_properties_format(input_map)
    assert result == expected
