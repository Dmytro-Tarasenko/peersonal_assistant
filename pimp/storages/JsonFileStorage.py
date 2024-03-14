from typing import Any, Optional
from pathlib import Path
import json
from collections import UserDict
from pydantic import BaseModel

from interfaces.IStorage import IStorage


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
                entity = self.model(**item)
                key_ = hash(entity.__getattribute__(self.unique))
                self.container[key_] = entity

    def create(self,
               entity: BaseModel) -> str:
        """Writes entity to storage and returns id."""
        unique = entity.__getattribute__(self.unique)
        if not self.container.get(hash(unique)):
            self.container[hash(unique)] = entity
            return str(hash(unique))
        else:
            raise ValueError(f"Entity with {self.unique}"
                             + f" {unique} already exists")

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
            json_data.append(entry.model_dump(warnings=False))
        with open(self.connection, "w", encoding='utf-8') as fout:
            json.dump(json_data, fout, ensure_ascii=False, default=str)

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
    id_ = storage.create(contact)
    print(id_)
    contact = ContactModel(name="Doe John",
                           email="some@where.com",
                           birthdate="1980-01-01",
                           phones=[{"phone": "1234567890"},
                                   {"phone": "   123456 "}],
                           address={"city": "New York",
                                    "country": "USA",
                                    "zip": "12345",
                                    "addr_string": "Some street 123"})
    id_ = storage.create(contact)
    print(id_)
    storage.commit()
    print(len(storage.container), len(storage.container.data))
