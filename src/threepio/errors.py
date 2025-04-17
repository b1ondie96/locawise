class ParseError(Exception):
    pass


class InvalidYamlConfigError(Exception):
    pass


class LLMApiError(Exception):
    pass


class InvalidLLMOutputError(Exception):
    pass


class LocalizationFailedError(Exception):
    pass
