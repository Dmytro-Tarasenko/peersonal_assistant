from abc import ABC, abstractmethod, abstractproperty
from typing import Any, Optional, Collection

from pydantic import BaseModel


class IStorage(ABC):
    container: Optional[Any] = None
    unique: str
    model: BaseModel
    connection: Any

    @abstractmethod
    def initialize(self,
                   connection: Any,
                   model: BaseModel,
                   unique_field: str):
        ...

    @abstractmethod
    def create(self,
               entity: BaseModel) -> str | int:
        ...

    @abstractmethod
    def read(self,
             offset: int = -1,
             limit: int = 0):
        ...

    @abstractmethod
    def update(self,
               entity: BaseModel,
               id_: int | str):
        ...

    @abstractmethod
    def delete(self,
               id_: int | str):
        ...

    @abstractmethod
    def iterator(self):
        ...

    @abstractmethod
    def commit(self):
        ...
