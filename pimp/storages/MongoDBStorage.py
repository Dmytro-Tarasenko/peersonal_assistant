
from pydantic import BaseModel
from interfaces import IStorage


class MongoDBStorage(IStorage):

    @property
    def capacity(self):
        return 0

    def initialize(self):
        pass

    def create(self,
               entity: BaseModel):
        pass

    def read(self,
             offset: int = -1,
             limit: int = 0):
        pass

    def update(self,
               id_: Any,
               entity: BaseModel,
               strict: bool = False):
        pass

    def delete(self,
               id_: Any):
        pass

    def commit(self):
        pass

    def iterator(self):
        pass