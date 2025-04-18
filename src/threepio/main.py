from src.threepio import parsing
from src.threepio.dictutils import unsafe_subdict
from src.threepio.diffutils import retrieve_keys_to_be_localized
from src.threepio.llm import LLMContext
from src.threepio.localization import localize


async def generate_localized_dictionary(
        llm_context: LLMContext,
        source_dict: dict[str, str],
        nom_keys: set[str],
        target_dict_path: str,
        target_language: str,
        context: str = '',
        tone: str = '',
        glossary: dict[str, str] | None = None,
) -> dict[str, str]:
    """
        Reads the target file, finds the keys that need localization, localizes them and returns the final target dict.

        Raises:
            ParsingError: If the target dictionary file cannot be parsed
            LocalizationFailedError: If the localization process fails
        """
    target_dict: dict[str, str] = await parsing.parse(file_path=target_dict_path)
    keys_to_be_localized: set[str] = retrieve_keys_to_be_localized(source_dict, target_dict, nom_keys)
    pairs_to_be_localized: dict[str, str] = unsafe_subdict(source_dict, keys_to_be_localized)
    localized_pairs = await localize(llm_context=llm_context,
                                     pairs=pairs_to_be_localized,
                                     target_language=target_language,
                                     context=context,
                                     tone=tone,
                                     glossary=glossary)

    target_dict.update(localized_pairs)

    return target_dict
