from functions.utility import join_and_check_path
import os
from functions.config import MAX_CHARS


def get_file_content(working_directory, file_path):
    file_path, success = join_and_check_path(working_directory, file_path)
    if not success:
        return file_path
    if not os.path.isfile(file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(file_path, "r") as file:
            file_content_string = file.read(MAX_CHARS)
    except Exception as e:
        return f"Error: {e}"
    return file_content_string
