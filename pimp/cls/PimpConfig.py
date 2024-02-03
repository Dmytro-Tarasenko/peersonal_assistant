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

    # def __init__(self, config_path=None) -> None:
    #     super().__init__()
    #     self.__read_config(config_path)

    def read_config(self, path):
        if Path(path).exists():
            with Path(path).open("r", encoding="utf-8") as fin:
                config = yaml.safe_load(fin)
            ab_section = config["AddressBook"]
            nb_section = config["NoteBook"]

            #TODO: remove after tests and in production variant
            # ab_section["connection"] = "../" + ab_section["connection"]
            # nb_section["connection"] = "../" + nb_section["connection"]

            print(Path.cwd())
            self.__address_book_dp = self.__data_providers[ab_section["provider"]](ab_section["connection"])
            self.address_book = self.__address_book_dp.read_data()

            self.__note_book_dp = self.__data_providers[nb_section["provider"]](nb_section["connection"])
            self.note_book = self.__note_book_dp.read_data()

    def refresh_data(self):
        pass


if __name__ == "__main__":
    cwd_ = Path.cwd()/"../"
    print(cwd_)
    pimp_config = PimpConfig(config_path="../config.yaml")
    conf_2 = PimpConfig()

    print(pimp_config.address_book.data)
    print(conf_2.address_book.data)

    print(pimp_config.note_book.data)
    print(conf_2.note_book.data)
