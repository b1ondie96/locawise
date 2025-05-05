import pytest

from locawise.dictutils import chunk_dict, simple_union, flatten_dict, unflatten_dict
from locawise.errors import UnsupportedLocalizationKeyError


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


def test_flatten_dict_empty_dict():
    _dict = {}
    result = flatten_dict(_dict, level_separator='//')
    assert result == {}


def test_flatten_dict_no_nested_levels():
    _dict = {
        'a': 'a1',
        'b': 'b1',
        'c': 'c1'
    }
    result = flatten_dict(_dict, level_separator='//')

    expected = {
        'a': 'a1',
        'b': 'b1',
        'c': 'c1'
    }
    assert result == expected


def test_flatten_dict_single_one_nested_level():
    _dict = {
        'a': {
            'b': 'b1',
            'c': 'c1'
        }
    }
    result = flatten_dict(_dict, level_separator='//')

    expected = {
        'a//b': 'b1',
        'a//c': 'c1'
    }
    assert result == expected


def test_flatten_dict_multiple_one_nested_level():
    _dict = {
        'a': {
            'b': 'b1',
            'c': 'c1',
            'd': 'd1'
        },
        'b': {
            'b': 'b1',
            'c': 'c1',
            'd': 'd1'
        },
        'e': 'e1'
    }
    result = flatten_dict(_dict, level_separator='//')

    expected = {
        'a//b': 'b1',
        'a//c': 'c1',
        'a//d': 'd1',
        'b//b': 'b1',
        'b//c': 'c1',
        'b//d': 'd1',
        'e': 'e1'
    }
    assert result == expected


def test_flatten_dict_two_nested_levels():
    _dict = {
        'a': {
            'b': {
                'c': 'c1'
            },
            'd': {
                'e1': 'e2',
                'e3': 'e4',
            }
        }
    }
    result = flatten_dict(_dict, level_separator='//')

    expected = {
        'a//b//c': 'c1',
        'a//d//e1': 'e2',
        'a//d//e3': 'e4'
    }
    assert result == expected


def test_flatten_dict_mixed_two_nested_levels():
    _dict = {
        'a': {
            'b': {
                'c': 'c1',
                'd': 'd1'
            },
            'e': 'e1'
        },
        'f': 'f1'
    }
    result = flatten_dict(_dict, level_separator='//')

    expected = {
        'a//b//c': 'c1',
        'a//b//d': 'd1',
        'a//e': 'e1',
        'f': 'f1'
    }
    assert result == expected


def test_flatten_dict_one_nested_level_and_two_nested_level():
    _dict = {
        'a': {
            'b': 'b1'
        },
        'c': {
            'd': {
                'e': 'e1'
            }
        },
        'f': 'f1'
    }
    result = flatten_dict(_dict, level_separator='//')

    expected = {
        'a//b': 'b1',
        'c//d//e': 'e1',
        'f': 'f1'
    }
    assert result == expected


def test_flatten_dict_single_three_nested_levels():
    _dict = {
        'a': {
            'b': {
                'c': {
                    'd': 'd1'
                }
            }
        }
    }
    result = flatten_dict(_dict, level_separator='//')

    expected = {
        'a//b//c//d': 'd1'
    }
    assert result == expected


def test_flatten_dict_key_with_level_separator():
    _dict = {
        'a//': 'b'
    }

    with pytest.raises(UnsupportedLocalizationKeyError):
        flatten_dict(_dict, level_separator='//')


def test_unflatten_dict_empty_dict():
    _dict = {}
    result = unflatten_dict(_dict, '//')
    assert result == {}


def test_unflatten_dict_regular_dict():
    _dict = {
        'a': 'b',
        'a2': 'b2',
        'a3': 'b3',
        'a4': 'b4',
        'a5': 'b5',
    }
    result = unflatten_dict(_dict, '//')

    expected = {
        'a': 'b',
        'a2': 'b2',
        'a3': 'b3',
        'a4': 'b4',
        'a5': 'b5',
    }
    assert result == expected


def test_unflatten_dict_one_level_nested_dict():
    _dict = {
        'a//b1': 'c1',
        'a//b2': 'c2',
        'a//b3': 'c3',
    }

    result = unflatten_dict(_dict, '//')

    expected = {
        'a': {
            'b1': 'c1',
            'b2': 'c2',
            'b3': 'c3',
        }
    }

    assert result == expected


def test_unflatten_dict_one_level_nested_dict_with_regulars():
    _dict = {
        'a//b1': 'c1',
        'a//b2': 'c2',
        'a//b3': 'c3',
        'd1': 'e1',
        'd2': 'e2',
        'd3': 'e3',
    }

    result = unflatten_dict(_dict, '//')

    expected = {
        'a': {
            'b1': 'c1',
            'b2': 'c2',
            'b3': 'c3',
        },
        'd1': 'e1',
        'd2': 'e2',
        'd3': 'e3',
    }

    assert result == expected


def test_unflatten_dict_two_level_nested_dict():
    _dict = {
        'a//b//c1': 'h1',
        'a//b//c2': 'h2',
        'a//b//c3': 'h3',
    }

    result = unflatten_dict(_dict, '//')

    expected = {
        'a': {
            'b': {
                'c1': 'h1',
                'c2': 'h2',
                'c3': 'h3',
            }
        },
    }

    assert result == expected


def test_unflatten_dict_three_level_nested_dict():
    _dict = {
        'a//b//c//d1': 'h1',
        'a//b//c//d2': 'h2',
        'a//b//c//d3': 'h3',
    }

    result = unflatten_dict(_dict, '//')

    expected = {
        'a': {
            'b': {
                'c': {
                    'd1': 'h1',
                    'd2': 'h2',
                    'd3': 'h3',
                }
            }
        },
    }

    assert result == expected


def test_unflatten_dict_mixed_nested_dict():
    _dict = {
        'a//b//c//d1': 'h1',
        'a//b//c2//d2': 'h2',
        'a//b//c//d3': 'h3',
        'a//c//d': 'h4',
        'a//b//e//d': 'h5',
        'f': 'f1'
    }

    result = unflatten_dict(_dict, '//')

    expected = {
        'a': {
            'b': {
                'c': {
                    'd1': 'h1',
                    'd3': 'h3',
                },
                'c2': {
                    'd2': 'h2'
                },
                'e': {
                    'd': 'h5'
                }
            },
            'c': {
                'd': 'h4'
            }
        },
        'f': 'f1'
    }

    assert result == expected
