from abc import ABC, abstractmethod
from typing import Any


class DataProvider(ABC):
    @property
    @abstractmethod
    def source_description(self) -> dict:
        pass

    @abstractmethod
    def read_data(self) -> Any:
        pass

    @abstractmethod
    def write_data(self, data: Any) -> bool:
        pass

    @abstractmethod
    def update_data(self, data: Any) -> bool:
        pass