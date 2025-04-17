from src.threepio.diffutils import retrieve_nom_source_keys
from src.threepio.lockfile import hash_key_value_pair


def test_retrieve_nom_source_keys_no_hashes():
    hashes = set()
    source_dict = {
        'a': 'b',
        'c': 'd',
        'e': 'f'
    }

    result = retrieve_nom_source_keys(hashes, source_dict)

    assert result == {'a', 'c', 'e'}


def test_retrieve_nom_source_keys_with_hashes():
    source_dict = {
        'a': 'b',
        'c': 'd',
        'e': 'f'
    }
    hashes = set()

    hashes.add(hash_key_value_pair('a', 'b'))

    result = retrieve_nom_source_keys(hashes, source_dict)

    assert result == {'c', 'e'}


def test_retrieve_nom_source_keys_with_old_hashes():
    source_dict = {
        'a': 'b',
        'c': 'd',
        'e': 'f'
    }
    hashes = set()

    hashes.add(hash_key_value_pair('a', 'd'))

    result = retrieve_nom_source_keys(hashes, source_dict)

    assert result == {'a', 'c', 'e'}


def test_retrieve_nom_source_keys_up_to_date_dict():
    source_dict = {
        'a': 'b',
        'c': 'd',
        'e': 'f'
    }
    hashes = set()

    hashes.add(hash_key_value_pair('a', 'b'))
    hashes.add(hash_key_value_pair('c', 'd'))
    hashes.add(hash_key_value_pair('e', 'f'))

    result = retrieve_nom_source_keys(hashes, source_dict)

    assert result == set()


def test_retrieve_nom_source_keys_up_to_date_dict_with_more_hashes():
    source_dict = {
        'a': 'b',
        'c': 'd',
        'e': 'f'
    }
    hashes = set()

    hashes.add(hash_key_value_pair('a', 'b'))
    hashes.add(hash_key_value_pair('c', 'd'))
    hashes.add(hash_key_value_pair('e', 'f'))
    hashes.add(hash_key_value_pair('g', 'q'))
    hashes.add(hash_key_value_pair('h', '1'))

    result = retrieve_nom_source_keys(hashes, source_dict)

    assert result == set()
