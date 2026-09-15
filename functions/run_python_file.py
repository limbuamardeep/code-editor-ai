import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a Python file relative to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string"},
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                },
            },
            "required": ["file_path"],
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        absolute_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_working_dir, file_path))
        valid_target_dir = (
            os.path.commonpath([absolute_working_dir, target_dir])
            == absolute_working_dir
        )
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
    except Exception as err:
        return f"Error: {err}"
    try:
        command = ["python", target_dir]
        if args:
            command.extend(args)

        result = subprocess.run(
            command, cwd=working_directory, capture_output=True, text=True, timeout=30
        )
        out_string = ""
        if result.returncode != 0:
            out_string += f"Process exited with code {result.returncode}"
        if len(result.stdout) == 0 and len(result.stderr) == 0:
            out_string += "No output produced"
        out_string += f"STDOUT: {result.stdout}"
        out_string += f"STDERR: {result.stderr}"
        return out_string
    except Exception as e:
        return f"Error: executing Python file: {e}"
