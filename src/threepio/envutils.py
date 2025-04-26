import os


# AIzaSyACM-WDxNuOpFEWyyQKLnw9l0ryPs04zZ8
def retrieve_gemini_api_key() -> str | None:
    return "AIzaSyACM-WDxNuOpFEWyyQKLnw9l0ryPs04zZ8"
    # return os.environ.get('GEMINI_API_KEY')


def retrieve_openai_api_key():
    return ("sk-proj-eri6U8H9zBlaOvi7GbQ3SnBqF0-gbx5oS06DGx8aFkW7ayEh"
            "--TvJZt9TiN66NQbipBJ6v99XtT3BlbkFJSTQKfNJ0fDodJE1zveip40nAPUjhSg8ZBvNevj1ECP2QSFHWQ7lYc5qN6f4C80"
            "-Mm5sHnaFy0A")


def generate_localization_file_name_without_extension(lang_code: str, file_name_pattern: str) -> str:
    return file_name_pattern.replace('{language}', lang_code)


def generate_localization_file_name(lang_code: str, file_name_pattern: str, extension: str) -> str:
    return generate_localization_file_name_without_extension(lang_code, file_name_pattern).replace('{ext}', extension)


def find_source_localization_file_path(lang_code: str, localization_root_path: str, file_name_pattern: str) -> str:
    file_name_without_extension = generate_localization_file_name_without_extension(lang_code,
                                                                                    file_name_pattern=file_name_pattern)
    path = find_file_by_basename(file_name_without_extension,
                                 localization_root_path if localization_root_path else './')

    if not path:
        raise ValueError('Source localization file could not be found.')

    return path


def find_file_by_basename(basename, search_path) -> str | None:
    for root, dirs, files in os.walk(search_path):
        for file in files:
            # Check if the file name (without extension) matches the basename
            if str(os.path.splitext(file)[0]).lower() in basename.lower():
                return str(os.path.join(root, file))
    return None
