"""Abstract base class for book storage"""
from abc import ABC, abstractmethod


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
