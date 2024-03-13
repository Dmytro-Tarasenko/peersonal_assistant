from typing import Any, Optional, Dict

from interfaces.IStorage import IStorage
from collections import UserDict


class FileStorage(IStorage):
    """Class that provides file storage"""
    def __init__(self):
        super().__init__()
        self.container = UserDict()

    def initialize(self,
                   connection: Dict[str, str]):
        pass

    def read(self,
             offset: int = -1,
             limit: int = 0):
        pass

    def write(self,
              entity: Any,
              id_: Optional[int | str] = None):
        """Writes entity to storage.
        If id_ is defined - replace operation is performed,
        otherwise new entity should be writen.
        """
        pass

    def commit(self):
        pass
