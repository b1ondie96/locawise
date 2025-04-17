import itertools
from itertools import batched


def chunk_dict(data, size: int):
    chunks = []
    for item in (dict(batch) for batch in batched(data.items(), size)):
        chunks.append(item)
    return chunks


def simple_union(*dicts):
    return dict(itertools.chain.from_iterable(dct.items() for dct in dicts))


def unsafe_subdict(original_dict: dict, sub_keys: set):
    "unsafe in the sense that if a key is not in the dict it will raise an error"
    return dict((k, original_dict[k]) for k in sub_keys)
