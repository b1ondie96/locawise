import logging
from typing import Self

import yaml
from pydantic import BaseModel, ValidationError, model_validator

from locawise.errors import InvalidYamlConfigError
from locawise.fileutils import read_file
from locawise.langutils import is_valid_two_letter_lang_code


class LocalizationConfig(BaseModel):
    version: str
    source_lang_code: str
    target_lang_codes: set[str] = {}
    localization_root_path: str = ''
    file_name_pattern: str = '{language}.{ext}'
    context: str = ''
    glossary: dict[str, str] = {}
    tone: str = ''
    llm_model: str | None = None
    llm_location: str | None = None

    @model_validator(mode='after')
    def validate_lang_codes(self) -> Self:
        if not is_valid_two_letter_lang_code(self.source_lang_code):
            raise ValueError(f'Invalid source language code {self.source_lang_code}')

        for lang_code in self.target_lang_codes:
            if not is_valid_two_letter_lang_code(lang_code):
                raise ValueError(f'{lang_code} is not a valid language code')

        return self


async def read_localization_config_yaml(file_path: str) -> LocalizationConfig:
    yaml_content = await read_file(file_path)
    yaml_dict = yaml.safe_load(yaml_content)
    if not isinstance(yaml_dict, dict):
        logging.error(f"Could not convert yaml file to config {yaml_dict}")
        raise InvalidYamlConfigError("Invalid YAML file")

    try:
        config = LocalizationConfig(**yaml_dict)
        return config
    except ValidationError as e:
        logging.error(f"Could not convert yaml file to config {yaml_dict} {e}")

        raise InvalidYamlConfigError("Invalid YAML file")
