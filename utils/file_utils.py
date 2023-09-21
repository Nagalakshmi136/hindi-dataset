import json
from typing import Union, Any
from pathlib import Path


def resolve_path(file_path: Union[str, Path]) -> Path:
    if isinstance(file_path, str):
        file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} not found")
    return file_path


def load_json(file_path: Union[str, Path]) -> Any:
    file_path = resolve_path(file_path)

    with open(file_path, "r", encoding="utf-8") as file_reader:
        try:
            json_data = json.load(file_reader)
        except json.decoder.JSONDecodeError:
            json_data = {}
            
    return json_data

def create_dir(dir_path):
    dir_path.mkdir(parents=True,exist_ok=True)
    return dir_path
        
    