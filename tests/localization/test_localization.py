import os
import pytest
from tenacity import wait_none

from locawise import llm
from locawise.errors import LocalizationError, LLMApiError
from locawise.llm import LLMContext, LLMStrategy
from locawise.localization import localize
from google import genai

@pytest.mark.asyncio
@pytest.mark.parametrize("chunk_size", [
    1,
    2,
    3,
    4,
    10,
    50,
    100
])
async def test_localize_with_mock_strategy_and_valid_pairs(chunk_size):
    strategy = llm.MockLLMStrategy()
    context = LLMContext(strategy)
    pairs = {
        'key1': 'value1',
        'key2': 'value2',
        'key3': 'value3',
        'key4': 'value4',
        'key5': 'value5',
        'key6': 'value6',
        'key7': 'value7',
    }
    target_language = 'en'

    result = await localize(context, pairs, target_language, chunk_size=chunk_size)

    assert result == {
        'key1': 'TRANSLATED_value1',
        'key2': 'TRANSLATED_value2',
        'key3': 'TRANSLATED_value3',
        'key4': 'TRANSLATED_value4',
        'key5': 'TRANSLATED_value5',
        'key6': 'TRANSLATED_value6',
        'key7': 'TRANSLATED_value7',
    }


@pytest.mark.asyncio
async def test_localize_with_mock_strategy_and_llm_api_error(monkeypatch):
    strategy = llm.MockLLMStrategy()
    context = LLMContext(strategy)
@pytest.mark.asyncio
async def test_localize_with_real_gemini():
        # Note: Requires GEMINI_API_KEY environment variable to be set
        strategy = llm.GeminiLLMStrategy(model="gemini-2.5-flash")
        context = LLMContext(strategy)
        
        pairs = {
            'welcome_message': 'Welcome to our app!',
            'sign_up': 'Sign up for an account',
            'terms': 'By continuing, you agree to our Terms of Service',
            'settings': 'Settings',
            'dark_mode': 'Dark mode',
            'language': 'Language'
        }

        target_languages = ['cs',  'de', ]
        
        for lang in target_languages:
            print(f"\nTranslating to {lang}:")
            result = await localize(
                context,
                pairs, 
                target_language=lang,
                context="This is a mobile app interface", 
                tone="friendly and professional"
            )
            
            print(f"Original text -> Translation")
            print("-" * 50)
            for key, value in pairs.items():
                print(f"{value} -> {result[key]}")
            
            assert len(result) == len(pairs)
            assert all(isinstance(v, str) for v in result.values())
            assert all(len(v) > 0 for v in result.values())
            
            # Basic validation that translations aren't identical to source
            assert any(v != pairs[k] for k, v in result.items())

@pytest.mark.asyncio 
async def test_localize_with_real_gemini_technical_content():
        strategy = llm.GeminiLLMStrategy(model="gemini-2.5-flash")
        context = LLMContext(strategy)
        
        pairs = {
            'error_database': 'Database connection failed',
            'error_timeout': 'Request timed out after {0} seconds',
            'error_validation': 'Invalid input: field {0} must be between {1} and {2}',
            'success_backup': 'Backup completed successfully',
            'warning_disk': 'Low disk space warning: {0}% remaining'
        }

        print("\nTranslating technical content to Japanese:")
        result = await localize(
            context,
            pairs,
            target_language='ja',
            context="These are technical error messages for a system administrator",
            tone="formal and technical"
        )

        print("\nOriginal text -> Translation")
        print("-" * 50)
        for key, value in pairs.items():
            print(f"{value} -> {result[key]}")
        
        assert len(result) == len(pairs)
        assert all(isinstance(v, str) for v in result.values())
        assert all(len(v) > 0 for v in result.values())
