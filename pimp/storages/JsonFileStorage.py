from typing import Any, Optional
from pathlib import Path
import json
from collections import UserDict
from pydantic import BaseModel

from interfaces.IStorage import IStorage
from models.ABModels import ContactModel

class JsonFileStorage(IStorage):
    """Class that provides file storage"""
    def __init__(self):
        super().__init__()
        self.container = UserDict()

    def initialize(self,
                   connection: Path,
                   model: BaseModel,
                   uniqe_filed: str):

        self.unique = uniqe_filed
        self.model = model
        self.connection = connection

        if not connection.exists():
            with open(connection, "w") as fout:
                json.dump([], fout)
                return
        with open(connection, "r") as fin:
            data = json.load(fin)
            for item in data:
                self.container[item[uniqe_filed]] = model(**item)

    def create(self,
               entity: BaseModel) -> (str, Any):
        """Writes entity to storage and returns id."""
        unique = entity.__getattribute__(self.unique)
        if not self.container.get(unique):
            self.container[hash(unique)] = entity
            return hash(unique), entity

    def read(self,
             offset: int = -1,
             limit: int = 0):
        pass

    def update(self,
              entity: Any,
              id_: int | str):
        """Update entity with id. """
        pass

    def delete(self, id_: int | str):
        """Removes entity from storage."""
        pass

    def commit(self):
        """Save changes to storage."""
        json_data = []
        for id_, entry in self.container.items():
            json_data.append({id_: entry.model_dump(warnings=False)})
        with open(self.connection, "w") as fout:
            json.dump(json_data, fout)

    def iterator(self):
        pass


if __name__ == "__main__":
    from pimp.models.ABModels import ContactModel, AddressModel, PhoneModel
    storage = JsonFileStorage()
    storage.initialize(Path("data.json"), ContactModel, "name")
    contact = ContactModel(name="John Doe",
                           email="some@where.com",
                           birthdate="1980-01-01",
                           phones=[{"phone": "1234567890"},
                                   {"phone": "   123456 "}],
                           address={"city": "New York",
                                    "country": "USA",
                                    "zip": "12345",
                                    "addr_string": "Some street 123"})
    id_, _ = storage.create(contact)
    print(id_)
