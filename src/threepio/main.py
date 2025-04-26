import argparse
import asyncio
import logging
import os

from envutils import find_source_localization_file_path, generate_localization_file_name
from llm import LLMContext
from localization.config import read_localization_config_yaml
from localization.format import find_extension
from lockfile import write_lock_file, create_lock_file_path
from processor import create_source_processor
from threepio.llm import OpenAiLLMStrategy


async def main(llm_context: LLMContext, config_path: str):
    config = await read_localization_config_yaml(config_path)
    source_lang_file_path = find_source_localization_file_path(config.source_lang_code,
                                                               localization_root_path=config.localization_root_path,
                                                               file_name_pattern=config.file_name_pattern)

    lock_file_path = create_lock_file_path(config.localization_root_path)

    processor = await create_source_processor(llm_context,
                                              source_file_path=source_lang_file_path,
                                              lock_file_path=lock_file_path,
                                              context=config.context,
                                              tone=config.tone,
                                              glossary=config.glossary)

    extension = find_extension(source_lang_file_path)
    async with asyncio.TaskGroup() as tg:
        for target_lang_code in config.target_lang_codes:
            logging.info(f'Creating task for {target_lang_code}')
            target_file_name = generate_localization_file_name(target_lang_code, config.file_name_pattern, extension)
            target_path = os.path.join(config.localization_root_path, target_file_name)
            tg.create_task(processor.localize_to_target_language(target_path, target_lang_code))

        tg.create_task(write_lock_file(lock_file_path, processor.source_dict))

    logging.info('All tasks have finished.')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser(
        description='Process localization files based on configuration.',
        epilog='Example: python3 main.py config.yaml'
    )
    parser.add_argument("config_path", help="Path to the YAML configuration file")
    args = parser.parse_args()

    # TODO: Update this
    llm_strategy = OpenAiLLMStrategy()
    _llm_context = LLMContext(llm_strategy)

    # Run the async main function
    asyncio.run(main(_llm_context, args.config_path))
