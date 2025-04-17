import itertools
from itertools import batched


def chunk_dict(data, size: int):
    chunks = []
    for item in (dict(batch) for batch in batched(data.items(), size)):
        chunks.append(item)
    return chunks


def simple_union(*dicts):
    return dict(itertools.chain.from_iterable(dct.items() for dct in dicts))
