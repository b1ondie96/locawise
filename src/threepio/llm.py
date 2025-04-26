import json
import logging
import re
from abc import ABC, abstractmethod

import openai
from google import genai
from google.genai import types
from tenacity import retry, stop_after_attempt, wait_exponential, wait_random

from threepio import envutils
from threepio.envutils import retrieve_openai_api_key
from threepio.errors import InvalidLLMOutputError, LLMApiError


class LLMStrategy(ABC):
    @abstractmethod
    async def call(self, system_prompt: str, user_prompt: str) -> dict[str, str]:
        pass


class LLMContext:
    def __init__(self, strategy: LLMStrategy):
        self.strategy = strategy

    @retry(stop=stop_after_attempt(4), wait=wait_exponential(multiplier=5, exp_base=2) + wait_random(min=0, max=2))
    async def call(self, system_prompt: str, user_prompt: str) -> dict[str, str]:
        """
        :raise InvalidLLMOutputError
        :raise LLMApiError
         """
        return await self.strategy.call(system_prompt, user_prompt)


class MockLLMStrategy(LLMStrategy):
    def __init__(self):
        self.regex = r'\{(?:[^{}]|(?:\{[^{}]*\}))*\}'

    def _extract_pairs_from_prompt(self, prompt: str) -> dict[str, str]:
        input_match = re.search(self.regex, prompt, re.DOTALL)
        if not input_match:
            return {}

        pairs_str = input_match.group(0).strip()

        try:
            pairs = json.loads(pairs_str)
            return {str(k): str(v) for k, v in pairs.items()}
        except json.JSONDecodeError:
            logging.exception("Json could not be decoded.")
            return {}

    async def call(self, system_prompt: str, user_prompt: str) -> dict[str, str]:
        if "THROW_LLM_API_ERROR" in user_prompt:
            raise LLMApiError
        if "THROW_INVALID_LLM_OUTPUT_ERROR" in user_prompt:
            raise InvalidLLMOutputError

        pairs = self._extract_pairs_from_prompt(user_prompt)
        output = {}
        for k, v in pairs.items():
            output[k] = f"TRANSLATED_{v}"

        return output


class GeminiLLMStrategy(LLMStrategy):
    def __init__(self):
        self.client = genai.Client(api_key=envutils.retrieve_gemini_api_key())
        self.model = 'gemini-2.0-flash'
        self.temperature = 0.1

    async def call(self, system_prompt: str, user_prompt: str) -> dict[str, str]:
        config = self._create_config(system_prompt)
        try:
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=user_prompt,
                config=config
            )
        except Exception:
            logging.exception(f'LLM call failed')
            raise LLMApiError

        try:
            return _parse_json_text(response.text)
        except Exception:
            logging.exception(f'{response.text} could not be parsed into a dictionary')
            raise InvalidLLMOutputError

    def _create_config(self, system_prompt):
        return types.GenerateContentConfig(temperature=self.temperature,
                                           system_instruction=system_prompt,
                                           automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
                                           )


class OpenAiLLMStrategy(LLMStrategy):
    def __init__(self):
        self.client = openai.AsyncClient(api_key=retrieve_openai_api_key(), max_retries=1)
        self.model = 'gpt-4.5-preview'
        self.temperature = 0.1

    async def call(self, system_prompt: str, user_prompt: str) -> dict[str, str]:
        try:
            response = await self.client.responses.create(
                model=self.model,
                instructions=system_prompt,
                input=user_prompt,
                temperature=self.temperature,
            )
        except Exception:
            logging.exception(f'LLM call failed')
            raise LLMApiError

        try:
            return _parse_json_text(response.output_text)
        except Exception:
            logging.exception(f'{response.text} could not be parsed into a dictionary')
            raise InvalidLLMOutputError


def _extract_json_text(text) -> str:
    pattern = r"```json\s*([\s\S]*?)\s*```"
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return text


def _parse_json_text(text: str) -> dict[str, str]:
    json_text: str = text
    if text.strip().startswith('```json'):
        json_text: str = _extract_json_text(text)

    return json.loads(json_text)
