from abc import ABC, abstractmethod, abstractproperty
from typing import Any, Optional, Collection

from pydantic import BaseModel


class IStorage(ABC):
    container: Any
    unique: Any

    @abstractmethod
    def initialize(self,
                   connection: Any):
        ...

    @abstractmethod
    def read(self,
             offset: int = -1,
             limit: int = 0):
        ...

    @abstractmethod
    def iterator(self):
        ...

    @abstractmethod
    def write(self,
              entity: Any | BaseModel,
              id_: Optional[int | str] = None):
        ...

    @abstractmethod
    def commit(self):
        ...
