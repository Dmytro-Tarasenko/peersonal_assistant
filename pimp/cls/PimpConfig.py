from typing import Dict
from pathlib import Path
from cls.AddressBook import AddressBook
from cls.NoteBook import Notebook
from abcs.DataProviderABC import DataProvider
from data_providers import PickleDataProvider, JsonDataProvider
import yaml


class Configleton(type):
    _instances = {}

    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super().__call__(*args, **kwargs)
        return self._instances[self]


class PimpConfig(metaclass=Configleton):
    """Main config storage for all app`s needs"""
    address_book: AddressBook = None
    note_book: Notebook = None

    __address_book_dp: DataProvider = None
    __note_book_dp: DataProvider = None

    __data_providers: Dict[str, DataProvider] = \
        {"file:pickle": PickleDataProvider.PickleDataProvider,
         "file:json": JsonDataProvider.JsonDataProvider}

    def __init__(self, config_path) -> None:
        super().__init__()
        self.__read_config(config_path)

    @staticmethod
    def __read_config(path):
        if Path(path).exists():
            with Path(path).open("r", encoding="utf-8") as fin:
                config = yaml.safe_load(fin)
        print(config)

    def refresh_data(self):
        pass


if __name__ == "__main__":
    pimp_config = PimpConfig(config_path="../config.yaml")
