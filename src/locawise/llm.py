import json
import logging
import re
from abc import ABC, abstractmethod

import httpx
import openai
from google import genai
from google.genai import types
from google.genai.errors import APIError
from openai import APIStatusError, OpenAIError
from tenacity import retry, stop_after_attempt, retry_if_exception_type, \
    wait_random_exponential

from locawise.envutils import retrieve_openai_api_key
from locawise.errors import InvalidLLMOutputError, LLMApiError, TransientLLMApiError

_NON_RETRYABLE_ERROR_STATUS_CODES = [400, 401, 403, 404, 409, 422]


class LLMStrategy(ABC):
    @retry(stop=stop_after_attempt(8),
           wait=wait_random_exponential(multiplier=5, exp_base=3, max=300, min=15),
           retry=retry_if_exception_type(TransientLLMApiError))
    @abstractmethod
    async def call(self, system_prompt: str, user_prompt: str) -> dict[str, str]:
        pass


class LLMContext:
    def __init__(self, strategy: LLMStrategy):
        self.strategy = strategy

    async def call(self, system_prompt: str, user_prompt: str) -> dict[str, str]:
        """
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
    def __init__(self, model: str | None = None, api_key: str | None = None):
        if not model:
            self.model = 'gemini-2.5-pro'
        else:
            self.model = model

        self.temperature = 0
        
        # Configure Google AI Studio
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(self.model)

    async def call(self, system_prompt: str, user_prompt: str) -> dict[str, str]:
        config = self._create_config(system_prompt)
        try:
            response = await self.model.generate_content_async(
                prompt=user_prompt,
                generation_config=config
            )
        except Exception as e:
            if hasattr(e, 'status_code') and e.status_code in _NON_RETRYABLE_ERROR_STATUS_CODES:
                raise LLMApiError from e
            else:
                raise TransientLLMApiError from e

        return _parse_json_text(response.text)

    def _create_config(self, system_prompt):
        return genai.types.GenerationConfig(
            temperature=self.temperature,
            candidate_count=1,
            max_output_tokens=2048
        )

class OpenAiLLMStrategy(LLMStrategy):
    def __init__(self, model: str | None = None):
        self.client = openai.AsyncClient(api_key=retrieve_openai_api_key(), max_retries=0,
                                         timeout=httpx.Timeout(600, connect=10))
        if not model:
            self.model = 'gpt-4.1-mini'
        else:
            self.model = model
        self.temperature = 0

    async def call(self, system_prompt: str, user_prompt: str) -> dict[str, str]:
        try:
            response = await self.client.responses.create(
                model=self.model,
                instructions=system_prompt,
                input=user_prompt,
                temperature=self.temperature,
            )
        except APIStatusError as e:
            if e.status_code in _NON_RETRYABLE_ERROR_STATUS_CODES:
                raise LLMApiError from e
            else:
                logging.warning(f"Transient llm api error occurred. status={e.status_code}")
                raise TransientLLMApiError from e
        except OpenAIError as e:
            raise TransientLLMApiError from e
        except Exception as e:
            raise LLMApiError from e

        return _parse_json_text(response.output_text)


def _extract_json_text(text) -> str:
    pattern = r"```json\s*([\s\S]*?)\s*```"
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return text


def _parse_json_text(text: str) -> dict[str, str]:
    try:
        json_text: str = text
        if text.strip().startswith('```json'):
            json_text: str = _extract_json_text(text)
        return json.loads(json_text)
    except Exception as e:
        logging.warning('Invalid LLM output. This generally happens when you use a "dumber" LLM model or '
                        'a model with low maximum output tokens. Please change '
                        'the LLM model.')
        raise InvalidLLMOutputError from e


def create_strategy(model: str | None, api_key: str | None = None) -> LLMStrategy:
    openai_key = retrieve_openai_api_key()
    if openai_key:
        return OpenAiLLMStrategy(model=model)

    try:
        return GeminiLLMStrategy(model=model, api_key=api_key)
    except Exception as e:
        logging.error("No API key found for any supported LLM providers. Please add the necessary "
                     "environment variables.")
        raise ValueError('No API key found for LLM providers.') from e
