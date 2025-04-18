from src.threepio.localization.format import LocalizationFormat


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
