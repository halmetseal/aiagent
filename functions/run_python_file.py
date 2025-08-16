from functions.utility import join_and_check_path
import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        completed_process = subprocess.run(["uv", "run", file_path] + args, check=False, timeout=30,
                                           capture_output=True, cwd=os.path.abspath(working_directory))
        output = ""
        output += f"STDOUT:\n{completed_process.stdout.decode('utf-8')}\nSTDERR:\n{
            completed_process.stderr.decode('utf-8')}"
        if completed_process.returncode != 0:
            output += f"\nProcess exited with code {
                completed_process.returncode}"
        if len(completed_process.stdout) == 0 and len(completed_process.stderr) == 0:
            output += "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"

    return output
