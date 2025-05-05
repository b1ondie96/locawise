import os

import pytest
from aiofiles import tempfile

from locawise.fileutils import read_file
from locawise.serialization import serialize_and_save


@pytest.mark.asyncio
@pytest.mark.parametrize("data, expected", [
    ({'a': 'a1', 'b': 'b1'}, 'a=a1\nb=b1\n'),
    ({'b': 'b1', 'a': 'a1'}, 'b=b1\na=a1\n'),
    ({'c': 'c1', 'b': 'b1', 'a': 'a1'}, 'c=c1\nb=b1\na=a1\n'),
    ({'b': 'b1'}, 'b=b1\n'),
    ({}, ''),
])
async def test_serialize_and_save_integration_valid_inputs(data, expected):
    async with tempfile.TemporaryDirectory() as temp_dir:
        test_file = os.path.join(temp_dir, "test_localization.properties")

        await serialize_and_save(data, test_file)

        content = await read_file(test_file)

        assert content == expected


@pytest.mark.asyncio
@pytest.mark.parametrize('path', [
    '  ',
    '',
    ' ',
    '      '
])
async def test_serialize_and_save_integration_empty_path(path):
    with pytest.raises(ValueError):
        await serialize_and_save({}, path)
