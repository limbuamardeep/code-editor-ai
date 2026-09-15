# Code Editor Ai

A small Python project for learning how to build an AI coding agent with OpenAI-compatible tool calls. It includes a calculator application used as the agent's working directory and four tools for inspecting, running, and modifying files.

## Requirements

- Python 3.13 or newer
- `uv`
- An OpenRouter API key

## Setup

Install the project dependencies:

```bash
uv sync
```

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your-api-key
```

## Run the Agent

Pass the user's request as a positional argument:

```bash
uv run main.py "Explain how the calculator renders the result to the console."
```

Use `--verbose` to print function arguments and token usage:

```bash
uv run main.py --verbose "List the files in the calculator project."
```

The agent operates in `calculator/`. Its available tools are:

- `get_files_info`: list files and directories
- `get_file_content`: read a file, truncating output after 10,000 characters
- `run_python_file`: execute a Python file with optional arguments
- `write_file`: create or overwrite a file

## Run the Calculator

Evaluate an expression using the calculator CLI:

```bash
uv run calculator/main.py "3 + 7 * 2"
```

Output:

```json
{
	"expression": "3 + 7 * 2",
	"result": 17
}
```

Expressions use whitespace-separated numbers and operators. Supported operators are `+`, `-`, `*`, and `/`, with normal multiplication and division precedence.

Running without an expression prints usage information:

```bash
uv run calculator/main.py
```

## Tests

Run the calculator unit tests:

```bash
uv run python -m unittest discover -s calculator -p 'tests.py'
```

The root-level `test_*.py` files are small manual smoke tests for the agent tools:

```bash
uv run test_get_files_info.py
uv run test_get_file_content.py
uv run test_run_python_file.py
uv run test_write_file.py
```

## Project Layout

```text
main.py                    AI agent entrypoint
call_function.py           Available tool schemas
functions/                 Tool implementations and dispatcher
prompts.py                 Agent system prompt
calculator/main.py         Calculator CLI
calculator/pkg/            Calculator and JSON rendering logic
calculator/tests.py        Calculator unit tests
```
