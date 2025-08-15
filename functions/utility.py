import os


def join_and_check_path(working_directory, file_path):
    directory = os.path.join(working_directory, file_path)
    if not os.path.abspath(directory).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory', False
    return directory, True
