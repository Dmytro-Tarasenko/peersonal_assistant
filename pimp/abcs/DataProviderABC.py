from abc import ABC, abstractmethod
from typing import Any


class DataProvider(ABC):
    @property
    @abstractmethod
    def source_description(self) -> Any:
        pass

    @abstractmethod
    def open(self) -> bool:
        pass

    @abstractmethod
    def close(self) -> bool:
        pass

    @abstractmethod
    def read_data(self) -> Any:
        pass

    @abstractmethod
    def update_data(self) -> bool:
        pass

    @abstractmethod
    def write_data(self) -> bool:
        pass
