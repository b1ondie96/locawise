from locawise.lockfile import create_lock_file_content


def test_create_lock_file_content(mocker):
    input_map = {
        'name': 'ahmet',
        'age': '19',
        'frank': 'jordan',
        'location': 'istanbul'
    }

    def hash_key_value_pair(key, value):
        return f'{key}={value}'

    mocker.patch('locawise.lockfile.hash_key_value_pair', side_effect=hash_key_value_pair)

    result = create_lock_file_content(input_map)

    expected_output = "name=ahmet\nage=19\nfrank=jordan\nlocation=istanbul\n"

    assert result == expected_output
