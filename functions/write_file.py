from functions.utility import join_and_check_path
import os


def write_file(working_directory, file_path, content):
    file_path, sucess = join_and_check_path(working_directory, file_path)
    if not sucess:
        return file_path
    if not os.path.exists(file_path):
        dirs = os.path.dirname(file_path)
        if not os.path.isdir(dirs):
            os.makedirs(dirs)

    try:
        with open(file_path, "w") as file:
            file.write(content)
    except Exception as e:
        return f"Error: {e}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
