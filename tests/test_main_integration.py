import pytest

from threepio.llm import MockLLMStrategy, LLMContext
from threepio.processor import generate_localized_dictionary
from tests.utils import get_absolute_path


def get_default_expected_dict():
    return {'app.title': 'Finans Yönetim Sistemi',
            'app.welcome': 'Kişisel finans yönetim sisteminize hoş geldiniz',
            'app.logout': 'Başarıyla çıkış yaptınız.',
            'error.invalid.credentials': 'TRANSLATED_Invalid username or password',
            'account.inactive': 'TRANSLATED_Your account has been inactive for {0} days',
            'transaction.success': 'TRANSLATED_Transaction completed successfully',
            'error.insufficient.funds': 'TRANSLATED_Insufficient funds to complete this transaction',
            'transaction.receipt': 'TRANSLATED_Transaction receipt has been sent to your email',
            'transaction.pending': 'TRANSLATED_Your transaction is pending approval',
            'account.balance': 'TRANSLATED_Current Balance: {0}'
            }


def get_all_translated_dict():
    return {'app.title': 'TRANSLATED_Financial Management System',
            'app.welcome': 'TRANSLATED_Welcome to your personal finance dashboard',
            'app.logout': 'TRANSLATED_You have been successfully logged out',
            'error.invalid.credentials': 'TRANSLATED_Invalid username or password',
            'account.inactive': 'TRANSLATED_Your account has been inactive for {0} days',
            'transaction.success': 'TRANSLATED_Transaction completed successfully',
            'error.insufficient.funds': 'TRANSLATED_Insufficient funds to complete this transaction',
            'transaction.receipt': 'TRANSLATED_Transaction receipt has been sent to your email',
            'transaction.pending': 'TRANSLATED_Your transaction is pending approval',
            'account.balance': 'TRANSLATED_Current Balance: {0}'
            }


@pytest.mark.asyncio
@pytest.mark.parametrize('nom_keys, expected', [
    (set(), get_default_expected_dict()),
    ({'app.title', 'app.welcome', 'app.logout'}, get_all_translated_dict())
])
async def test_generate_localized_dictionary_non_empty_source_dict_and_empty_properties_file(nom_keys, expected):
    source_dict = {
        # General application messages
        "app.title": "Financial Management System",
        "app.welcome": "Welcome to your personal finance dashboard",
        "app.logout": "You have been successfully logged out",

        # Error messages
        "error.invalid.credentials": "Invalid username or password",
        "error.insufficient.funds": "Insufficient funds to complete this transaction",

        # Transaction messages
        "transaction.success": "Transaction completed successfully",
        "transaction.pending": "Your transaction is pending approval",
        "transaction.receipt": "Transaction receipt has been sent to your email",

        # Account messages
        "account.balance": "Current Balance: {0}",
        "account.inactive": "Your account has been inactive for {0} days"
    }
    llm_strategy = MockLLMStrategy()
    llm_context = LLMContext(llm_strategy)

    result = await generate_localized_dictionary(
        llm_context=llm_context,
        source_dict=source_dict,
        nom_keys=nom_keys,
        target_dict_path=get_absolute_path('resources/languages/tr.properties'),
        target_language_full_name='Turkish'
    )

    assert result == expected
