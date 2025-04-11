import aiofiles
import jproperties


async def parse_java_properties_file(file_path: str) -> dict[str, str]:
    p = jproperties.Properties()
    async with aiofiles.open(file_path, mode='r', encoding='UTF-8') as f:
        contents = await f.read()
        p.load(contents, encoding='UTF-8')

    return p.properties
