from functions.utility import join_and_check_path
import os

from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the specified content to the specified file_path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write the content to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents to write to the file. This will overwrite the file's contents.",
            ),
        },
    ),
)


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
