"""Abstract base class for book storage"""
from abc import ABC, abstractmethod


class Singleton(abc.ABCMeta, type):
    """
    Singleton metaclass for ensuring only one instance of a class.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class AbstractSingleton(abc.ABC, metaclass=Singleton):
    """
    Abstract Singleton class for ensuring only one instance of a class,
        this class also ensures all abstract methods are implemented.
    """
    pass

class Book(ABC):
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
