from abc import ABC, abstractmethod


class DataProvider(ABC):
    @property
    @abstractmethod
    def source(self):
        pass

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def read_data(self):
        pass

    @abstractmethod
    def update_data(self):
        pass

    @abstractmethod
    def write_data(self):
        pass
