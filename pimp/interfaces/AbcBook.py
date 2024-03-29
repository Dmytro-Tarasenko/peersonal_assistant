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
    """Abstract base class for book storage."""
    record_counter: int = 0
    record_id: int = 0

    @property
    def records_quantity(self):
        return self.record_counter

    @abstractmethod
    def add_record(self, record):
        """Create."""
        pass

    @abstractmethod
    def get_records(self, start: int, limit: int):
        """Read."""
        pass

    @abstractmethod
    def edit_record(self,
                    old_record,
                    new_record):
        """Update."""
        pass

    @abstractmethod
    def delete_record(self, record):
        """Delete."""
        pass

    @abstractmethod
    def find_record(self, search_conditions):
        """Read (find)."""
        pass

    @abstractmethod
    def iterator(self):
        pass
