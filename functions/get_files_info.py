import os
from functions.utility import join_and_check_path


def get_files_info(working_directory, directory="."):
    directory, success = join_and_check_path(working_directory, directory)
    if not success:
        return directory
    if not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'
    try:
        files = os.listdir(directory)
    except Exception as e:
        return f"Error: {e}"
    files_info = []
    for file in files:
        try:
            filepath = os.path.join(directory, file)
            size = os.path.getsize(filepath)
            is_dir = os.path.isdir(filepath)
            files_info.append(
                f"- {file}: file_size={size} bytes, is_dir={is_dir}")
        except Exception as e:
            return f"Error: {e}"
    return "\n".join(files_info)
