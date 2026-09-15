import os
from pathlib import Path

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        absolute_path_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(
            os.path.join(absolute_path_working_dir, directory)
        )
        valid_target_dir = (
            os.path.commonpath([absolute_path_working_dir, target_dir])
            == absolute_path_working_dir
        )
    except Exception as e:
        return f"Error: {e}"
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not Path(target_dir).is_dir():
        return f'Error: "{directory}" is not a directory'
    if valid_target_dir:
        try:
            file_dict = {}
            list_dir = os.listdir(target_dir)
            content = ""
            for files in list_dir:
                full_path = os.path.join(target_dir, files)
                is_dir = os.path.isdir(full_path)
                file_size = os.path.getsize(full_path)
                file_dict[files] = {"file_size": file_size, "is_dir": is_dir}
            for keys, values in file_dict.items():
                content += f"- {keys}: file_size={values['file_size']} bytes, is_dir={values['is_dir']}\n"
        except Exception as err:
            return f"Error: {err}"
        return content
