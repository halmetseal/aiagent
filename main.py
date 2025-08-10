import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


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

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )
    print(f"Gemini: {response.text}")
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {
              response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
