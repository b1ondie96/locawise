import asyncio
import logging

from src.threepio.dictutils import chunk_dict, simple_union
from src.threepio.errors import LLMApiError, InvalidLLMOutputError, LocalizationError
from src.threepio.llm import LLMContext
from src.threepio.localization.prompts import generate_system_prompt, generate_user_prompt


async def localize(llm_context: LLMContext,
                   pairs: dict[str, str],
                   target_language: str,
                   context: str = '',
                   tone: str = '',
                   glossary: dict[str, str] | None = None,
                   chunk_size: int = 30
                   ) -> dict[str, str]:
    if glossary is None:
        glossary = {}
    system_prompt = generate_system_prompt(context=context, glossary=glossary, tone=tone)
    chunks = chunk_dict(pairs, chunk_size)

    tasks = []
    try:
        async with asyncio.TaskGroup() as tg:
            logging.info("Generating tasks for translation")
            for chunk in chunks:
                user_prompt = generate_user_prompt(chunk, target_language)
                tasks.append(tg.create_task(llm_context.call(system_prompt, user_prompt)))
    except* (LLMApiError, InvalidLLMOutputError) as e:
        logging.warning(f"Translation failed. {e}")
        raise LocalizationError
    except* Exception:
        logging.exception("Unknown error occurred!")
        raise LocalizationError

    results = [task.result() for task in tasks]
    return simple_union(*results)
