import logging

import jproperties

from src.threepio.errors import ParseError
from src.threepio.fileutils import read_file
from src.threepio.localization.format import detect_format, LocalizationFormat


async def parse(file_path: str) -> dict[str, str]:
    """

    :param file_path:
    :return:
    :raises LocalizationFormatError:
    :raises ParseError:
    :raises ValueError:
    """
    if not file_path:
        return {}
    localization_format: LocalizationFormat = detect_format(file_path)
    try:
        file_content = await read_file(file_path)
    except Exception as e:
        logging.exception(f"Unknown exception encountered while reading file. {file_path}")
        raise ParseError(f"Unknown exception while reading {file_path}") from e

    match localization_format:
        case LocalizationFormat.PROPERTIES:
            return await parse_java_properties_file(file_content)
        case _:
            raise ValueError(f"Parsing is not implemented for format={localization_format}")


async def parse_java_properties_file(file_content: str) -> dict[str, str]:
    try:
        p = jproperties.Properties()
        p.load(file_content, encoding='UTF-8')
        return p.properties
    except Exception as e:
        raise ParseError("Java properties file could not be parsed") from e
