import os
import sys
from dotenv import load_dotenv
from google import genai


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def main():

    # Just the args stuff
    argv = sys.argv
    prompt = ""
    if len(argv) > 1:
        prompt = argv[1]
    else:
        print(f"Usage: {argv[0]} \"<prompt>\"")
        exit(1)

    # Program begins here
    print("Hello from ai-agent!\n")

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=prompt)
    print(f"Gemini: {response.text}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
