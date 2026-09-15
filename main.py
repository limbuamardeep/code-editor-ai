import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions
from functions.call_functions import call_function
import json

load_dotenv()
try:
    api_key = os.environ.get("OPENROUTER_API_KEY")
except RuntimeError:
    print("No Api key found!")


parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]


def main():
    for _ in range(20):
        try:
            response = client.chat.completions.create(
                model="openrouter/free", messages=messages, tools=available_functions
            )
            prompt_tokens = response.usage.prompt_tokens
            response_tokens = response.usage.completion_tokens
        except RuntimeError:
            print("Api request failed")
        if args.verbose:
            print(f"User prompt:{args.user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
        message = response.choices[0].message
        messages.append(message)
        if not message.tool_calls:
            print(message.content)
            break
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, verbose=args.verbose)
                print(result_message["content"])
                messages.append(result_message)
                if args.verbose:
                    print(f"-> {result_message['content']}")

    else:
        print("Reached maximum tool-call iterations.")


if __name__ == "__main__":
    main()
