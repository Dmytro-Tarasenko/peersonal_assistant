from typing import Any
from json import load, dump

from abcs.DataProviderABC import DataProvider


class JsonDataProvider(DataProvider):
    """Provides read/write operation with json.load/json.dump"""
    @property
    def source_description(self) -> dict:
        return dict()

    def read_data(self) -> Any:
        pass

    def update_data(self, data: Any) -> bool:
        return True

    def write_data(self, data: Any) -> bool:
        return True
