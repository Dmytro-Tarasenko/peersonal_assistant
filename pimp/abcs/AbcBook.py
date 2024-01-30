"""Abstract base class for book storage"""
from abc import ABC, ABCMeta, abstractmethod
from collections import UserDict


class Singleton(ABCMeta, type):
    """
    Singleton metaclass for ensuring only one instance of a class.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Book(ABC, metaclass=Singleton):
    @abstractmethod
    def add_record(self, record):
        pass

    @abstractmethod
    def edit_record(self,
                    old_record,
                    new_record):
        pass

    @abstractmethod
    def delete_record(self, record):
        pass

    @abstractmethod
    def find_record(self, search_conditions):
        pass

    @abstractmethod
    def iterator(self):
        pass

class TestBook(Book, UserDict):
    def add_record(self, record):
        pass

    def edit_record(self,
                    old_record,
                    new_record):
        pass

    def delete_record(self, record):
        pass

    def find_record(self, search_conditions):
        pass

    def iterator(self):
        pass


if __name__ == "__main__":
    tb1 = TestBook()
    tb2 = TestBook()

    print(tb1)
    print(tb2)

    print(tb1 == tb2)