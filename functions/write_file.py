import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content to a file relative to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string"},
                "content": {"type": "string"},
            },
            "required": ["file_path", "content"],
        },
    },
}


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        absolute_path_working_dir = os.path.abspath(working_directory)
        target_path = os.path.normpath(
            os.path.join(absolute_path_working_dir, file_path)
        )
        valid_target_dir = (
            os.path.commonpath([absolute_path_working_dir, target_path])
            == absolute_path_working_dir
        )
    except Exception as e:
        return f"Error: {e}"
    if not valid_target_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    try:
        parent_dirs = os.path.dirname(target_path)
        os.makedirs(parent_dirs, exist_ok=True)
        with open(target_path, "w") as file:
            file.write(content)
    except Exception as err:
        return f"Error: {err}"
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
