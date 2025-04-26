import os


# AIzaSyACM-WDxNuOpFEWyyQKLnw9l0ryPs04zZ8
def retrieve_gemini_api_key() -> str | None:
    return "AIzaSyACM-WDxNuOpFEWyyQKLnw9l0ryPs04zZ8"
    # return os.environ.get('GEMINI_API_KEY')


def retrieve_openai_api_key():
    return ("sk-proj-eri6U8H9zBlaOvi7GbQ3SnBqF0-gbx5oS06DGx8aFkW7ayEh"
            "--TvJZt9TiN66NQbipBJ6v99XtT3BlbkFJSTQKfNJ0fDodJE1zveip40nAPUjhSg8ZBvNevj1ECP2QSFHWQ7lYc5qN6f4C80"
            "-Mm5sHnaFy0A")


def generate_localization_file_name(lang_code: str, file_name_pattern: str) -> str:
    return file_name_pattern.replace('{language}', lang_code)

