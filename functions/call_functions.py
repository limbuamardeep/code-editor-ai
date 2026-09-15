from collections.abc import Callable

from .get_file_content import get_file_content
from .get_files_info import get_files_info
from .write_file import write_file
from .run_python_file import run_python_file
import json

function_map: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "write_file": write_file,
    "run_python_file": run_python_file,
}


def call_function(tool_call, verbose: bool = False) -> dict:
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments or "{}")
    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    function_to_call = function_map.get(function_name)
    if function_to_call is None:
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": f"Error: Unknown function: {function_name}",
        }
    else:
        function_args["working_directory"] = "./calculator"
        try:
            result = function_to_call(**function_args)
        except Exception as err:
            result = f"Error: {err}"
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result,
        }
