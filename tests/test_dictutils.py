from src.threepio.dictutils import chunk_dict, simple_union


def test_chunk_dict_empty_dict():
    d1 = {}
    actual = chunk_dict(d1, 10)
    assert actual == []


def test_chunk_dict_dict_with_single_element():
    d1 = {'key1': 'value1'}
    actual = chunk_dict(d1, 1)
    assert len(actual) == 1
    assert actual[0] == d1


def test_chunk_dict_dict_with_multiple_elements():
    d1 = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
    actual = chunk_dict(d1, 2)
    assert len(actual) == 2
    assert actual[0]['key1'] == 'value1'
    assert actual[0]['key2'] == 'value2'
    assert actual[1]['key3'] == 'value3'


def test_simple_union_empty_dicts():
    d1 = {}
    d2 = {}
    actual = simple_union(d1, d2)

    assert actual == {}


def test_simple_union_one_empty_one_full_dicts():
    d1 = {}
    d2 = {'k1': 'v1', 'k2': 'v2'}

    actual = simple_union(d1, d2)

    assert actual == d2


def test_simple_union_three_dicts():
    d1 = {'k1': 'v1'}
    d2 = {'k2': 'v2'}
    d3 = {'k3': 'v3'}

    actual = simple_union(d1, d2, d3)

    assert actual == {'k1': 'v1', 'k2': 'v2', 'k3': 'v3'}
