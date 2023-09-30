import json
import os
from pathlib import Path
from typing import Any, Union


def resolve_path(file_path: Union[str, Path]) -> Path:
    
    """Checking the given path exist or not and return path if exist

    Args:
        file_path (Union[str, Path]): path of the file

    Raises:
        FileNotFoundError: if path not exist raises error

    Returns:
        Path: if path exist return path
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} not found")
    return file_path


def load_json(file_path: Union[str, Path]) -> Any:
    """Load data from json file

    Args:
        file_path (Union[str, Path]): The path of the json file

    Returns:
        Any: dictionary with the data in file
    """
    file_path = resolve_path(file_path)

    with open(file_path, "r", encoding="utf-8") as file_reader:
        try:
            json_data = json.load(file_reader)
        except json.decoder.JSONDecodeError:
            json_data = {}

    return json_data


def create_dir(dir_path: Union[str, Path]) -> Path:
    """Creating the directory with given path

    Args:
        dir_path (Union[str, Path]): path of the directory that should create

    Returns:
        Path: Created directory path
    """
    if isinstance(dir_path, str):
        dir_path = Path(dir_path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def remove_file(audio_file: Path) -> None:
    """removing the file from given path

    Args:
        audio_file (Path): The path of the file that should remove
    """
    if os.path.exists(audio_file):
        os.remove(audio_file)
