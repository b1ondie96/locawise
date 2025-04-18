import logging

from src.threepio.errors import FileSaveError
from src.threepio.fileutils import write_to_file
from src.threepio.localization.format import LocalizationFormat, detect_format


async def serialize_and_save(key_value_pairs: dict[str, str], target_path: str):
    """
    :raises LocalizationFormatError
    :raises FileSaveError
    :raises ValueError
    """
    if not target_path.strip():
        raise ValueError(f"Target path cannot be empty")

    localization_format = detect_format(target_path)
    content = serialize(key_value_pairs, localization_format=localization_format)

    try:
        await write_to_file(file_path=target_path, content=content)
    except Exception as e:
        logging.exception(f"Could not write content to target_path={target_path}")
        raise FileSaveError("Could not write content to target_path") from e


def serialize(key_value_map: dict[str, str], localization_format: LocalizationFormat) -> str:
    match localization_format:
        case LocalizationFormat.PROPERTIES:
            return serialize_to_properties_format(key_value_map)
        case _:
            raise ValueError(f"Serialization for {localization_format} is not implemented")


def serialize_to_properties_format(key_value_map: dict[str, str]) -> str:
    content = ""

    for k in sorted(key_value_map.keys()):
        content += f"{k}={key_value_map[k]}\n"

    return content
