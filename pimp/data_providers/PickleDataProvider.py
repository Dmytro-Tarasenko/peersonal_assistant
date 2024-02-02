from abcs.DataProviderABC import DataProvider
from pathlib import Path
from typing import Any
from pickle import load, dump


class PickleDataProvider(DataProvider):
    """Provides read/write operation with pickle.load/pickle.dump"""
    def __init__(self, path) -> None:
        self.__connection = Path(path)
        self.source = "file:pickle"

    @property
    def source_description(self) -> dict:
        return {"connection": self.__connection,
                "source": self.source}

    def update_data(self, data) -> bool:
        return True

    def read_data(self) -> Any:
        obj_path: Path = self.__connection
        if obj_path.exists():
            with obj_path.open("rb") as fin:
                try:
                    obj = load(fin)
                except Exception as err:
                    return err
            return obj

    def write_data(self, data: Any) -> bool:
        obj_path = self.__connection
        with obj_path.open("wb") as fout:
            try:
                dump(data, fout)
            except Exception:
                return False
        return True
