import aiofiles
import jproperties

from src.threepio.errors import ParseError
from src.threepio.localization_formats import detect_format, LocalizationFormat


async def parse(file_path: str):
    localization_format: LocalizationFormat = detect_format(file_path)
    file_content = await read_file(file_path)

    match localization_format:
        case LocalizationFormat.PROPERTIES:
            return parse_java_properties_file(file_content)
        case _:
            raise ValueError(f"Parsing is not implemented for format={localization_format}")


async def read_file(file_path: str) -> str:
    async with aiofiles.open(file_path, mode='r', encoding='UTF-8') as f:
        contents = await f.read()
        return contents


async def parse_java_properties_file(file_content: str) -> dict[str, str]:
    try:
        p = jproperties.Properties()
        p.load(file_content, encoding='UTF-8')
        return p.properties
    except Exception as e:
        raise ParseError("Java properties file could not be parsed") from e
