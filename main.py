import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ],

)


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {
              function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    working_directory = "./calculator"
    if function_call_part.name == "get_files_info":
        result = get_files_info(working_directory, **function_call_part.args)
    elif function_call_part.name == "get_file_content":
        result = get_file_content(working_directory, **function_call_part.args)
    elif function_call_part.name == "run_python_file":
        result = run_python_file(working_directory, **function_call_part.args)
    elif function_call_part.name == "write_file":
        result = write_file(working_directory, **function_call_part.args)
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {
                        function_call_part.name}"},
                )
            ],
        )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result},
            )
        ],
    )


def main():
    # Just the args stuff
    argv = sys.argv
    prompt = ""
    verbose = False
    if len(argv) > 2:
        if "--verbose" in argv[2:]:
            verbose = True
    if len(argv) > 1:
        prompt = argv[1]
    else:
        print(f"Usage: {argv[0]} \"<prompt>\"")
        exit(1)

    # Program begins here
    print("Hello from ai-agent!\n")

    if verbose:
        print(f"User prompt: {prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    try:
        for i in range(0, 20):

            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt)
            )
            if response.function_calls is []:
                print(response.text)
                break

            for candidate in response.candidates:
                messages.append(candidate.content)

            functions_called = response.function_calls
            print(f"Gemini: {response.text}")
            for function_call_part in functions_called:
                function_call_result = call_function(
                    function_call_part, verbose)
                if not hasattr(function_call_result.parts[0].function_response, "response"):
                    raise Exception(
                        f"Fatal Error: Function response of {function_call_part.name} does not have a response!")
                if verbose:
                    print(
                        f"-> {function_call_result.parts[0].function_response.response}")
                user_content = types.Content(
                    role="user", parts=function_call_result.parts)
                messages.append(user_content)
    except Exception as e:
        print(e)

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {
              response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
