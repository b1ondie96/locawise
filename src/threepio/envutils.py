import base64
import json
import os

from google.oauth2 import service_account
from google.oauth2.service_account import Credentials


# AIzaSyACM-WDxNuOpFEWyyQKLnw9l0ryPs04zZ8
def retrieve_gemini_api_key() -> str | None:
    return os.environ.get('VERTEX_AI_SERVICE_ACCOUNT_JSON_KEY_BASE64')
    # return os.environ.get('GEMINI_API_KEY')


def retrieve_openai_api_key():
    return os.environ.get('OPENAI_API_KEY')


def generate_localization_file_name(lang_code: str, file_name_pattern: str) -> str:
    return file_name_pattern.replace('{language}', lang_code)


def generate_vertex_ai_credentials_from_base64(encoded_text: str) -> Credentials:
    bytes_data = base64.b64decode(encoded_text)
    service_account_key = json.loads(bytes_data.decode('utf-8'))
    credentials: Credentials = service_account.Credentials.from_service_account_info(service_account_key)
    return credentials.with_scopes(
        ['https://www.googleapis.com/auth/cloud-platform', 'https://www.googleapis.com/auth/cloud-platform.read-only'])
