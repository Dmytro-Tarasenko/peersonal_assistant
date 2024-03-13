from typing import Any
from pathlib import Path
from json import load, dump

from interfaces.StorageABC import Storage


class JsonStorage(Storage):
    """Provides read/write operation with json.load/json.dump"""
    def __init__(self, path) -> None:
        self.__connection = Path(path)
        self.source = "file:json"

    @property
    def source_description(self) -> dict:
        return {"connection": self.__connection,
                "source": self.source}

    def read_data(self) -> Any:
        with self.__connection.open("r") as fin:
            try:
                obj = load(fin)
                return obj
            except Exception as err:
                return err

    def update_data(self, data: Any) -> bool:
        return True

    def write_data(self, data: Any) -> bool:
        return True
