import os

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads the contents of a file relative to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path relative to the working directory.",
                }
            },
            "required": ["file_path"],
        },
    },
}


def get_file_content(working_directory: str, file_path: str) -> str:
    MAX_CHARS = 10000
    try:
        absolute_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_working_dir, file_path))
        valid_target_dir = (
            os.path.commonpath([absolute_working_dir, target_dir])
            == absolute_working_dir
        )
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_dir, "r") as file:
            file_content = file.read(MAX_CHARS)
            if file.read(1):
                file_content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return file_content
    except Exception as e:
        return f"Error: {e}"
