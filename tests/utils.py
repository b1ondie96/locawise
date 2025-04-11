import os


def get_absolute_path(file_path: str) -> str:
    return os.path.join(os.path.dirname(__file__), file_path)
