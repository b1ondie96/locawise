import pytest

from threepio.diffutils import retrieve_nom_source_keys, retrieve_keys_to_be_localized
from threepio.lockfile import hash_key_value_pair


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


@pytest.mark.parametrize("source_dict, target_dict, expected", [
    ({'a', 'b'}, {'c', 'd', 'e'}, {'a', 'b'}),
    ({'a', 'b'}, {'a', 'b', 'e'}, set()),
    ({'a', 'b'}, {'c', 'b', 'e'}, {'a'}),
    ({'a', 'b'}, {'c', 'a', 'e'}, {'b'}),
    ({'a', 'b'}, set(), {'b', 'a'}),
    (set(), set(), set()),
])
def test_retrieve_keys_to_be_translated_without_nom_keys(source_dict: set[str], target_dict: set[str],
                                                         expected: set[str]):
    d1 = {}
    for key in source_dict:
        d1[key] = key
    d2 = {}
    for key in target_dict:
        d2[key] = key

    result = retrieve_keys_to_be_localized(d1, d2, nom_keys=set())
    assert expected == result


@pytest.mark.parametrize("source_dict, target_dict, nom_keys, expected", [
    ({'a', 'b'}, {'a', 'd', 'e'}, {'a'}, {'a', 'b'}),
    ({'a', 'b'}, {'a', 'b', 'e'}, set(), set()),
    ({'a', 'b'}, {'c', 'b', 'e'}, {'c'}, {'a', 'c'}),
    ({'a', 'b'}, {'c', 'a', 'e'}, {'a'}, {'a', 'b'}),
    ({'a', 'b'}, set(), {'b', 'a'}, {'b', 'a'}),
    (set(), set(), set(), set()),
])
def test_retrieve_keys_to_be_translated_with_nom_keys(source_dict: set[str],
                                                      target_dict: set[str],
                                                      nom_keys: set[str],
                                                      expected: set[str]):
    d1 = {}
    for key in source_dict:
        d1[key] = key
    d2 = {}
    for key in target_dict:
        d2[key] = key

    result = retrieve_keys_to_be_localized(d1, d2, nom_keys=nom_keys)
    assert expected == result
