from pathlib import Path
import pickle
from collections import UserDict
from pydantic import BaseModel

from interfaces.IStorage import IStorage


class PickleFileStorage(IStorage):
    """Class that provides file storage (pickle binary)"""
    def __init__(self):
        super().__init__()
        self.container = UserDict()

    @property
    def capacity(self) -> int:
        return len(self.container)

    def initialize(self,
                   connection: Path,
                   model: BaseModel,
                   uniqe_filed: str):

        self.unique = uniqe_filed
        self.model = model
        self.connection = connection

        if not connection.exists():
            with open(connection, "wb") as fout:
                pickle.dump([], fout)
                return
        with open(connection, "rb") as fin:
            data = pickle.load(fin)
            for item in data:
                entity = self.model(**item)
                key_ = hash(entity.__getattribute__(self.unique))
                self.container[str(key_)] = entity

    def create(self,
               entity: BaseModel) -> str:
        """Writes entity to storage and returns id."""
        unique = entity.__getattribute__(self.unique)
        key_ = str(hash(unique))
        if not self.container.get(key_):
            self.container[key_] = entity
            return key_
        else:
            raise ValueError(f"Entity with {self.unique}"
                             + f" {unique} already exists")

    def read(self,
             offset: int = -1,
             limit: int = 0):
        start = offset if offset > 0 else 0
        end = start + limit if limit != 0 else len(self.container)
        return list(self.container.values())[start:end]

    def _is_gemini(self, entity: BaseModel):
        unique = entity.__getattribute__(self.unique)
        for _, value in self.container.items():
            if value.__getattribute__(self.unique) == unique:
                return True
        return False

    def update(self,
               entity: BaseModel,
               id_: int | str,
               strict: bool = False):
        """Update entity with id. """
        exclude = not strict
        stored_entity = self.container.get(id_)

        if self._is_gemini(entity):
            raise ValueError(f"Entity with {self.unique}"
                             + f" {entity.__getattribute__(self.unique)}"
                             + " already exists")

        if stored_entity is None:
            raise ValueError(f"Entity with id {id_} not found")
        update_data = entity.model_dump(exclude_unset=exclude,
                                        warnings=False)
        updated_entity = stored_entity.model_copy(update=update_data,
                                                  deep=True)
        self.container[id_] = updated_entity

    def delete(self, id_: int | str):
        """Removes entity from storage."""
        if id_ in self.container:
            self.container.pop(id_)
        else:
            raise ValueError(f"Entity with id {id_} not found")

    def commit(self):
        """Save changes to storage."""
        pickle_data = []
        for id_, entry in self.container.items():
            pickle_data.append(entry)
        with open(self.connection, "wb") as fout:
            pickle.dump(pickle_data, fout)

    def iterator(self):
        pass


if __name__ == "__main__":
    from pimp.models.ABModels import ContactModel
    storage = PickleFileStorage()
    storage.initialize(Path("data.bin"), ContactModel, "name")
    contact = ContactModel(name="John Doe",
                           email="some@where.com",
                           birthdate="1980-01-01",
                           phones=[{"phone": "1234567890"},
                                   {"phone": "   123456 "}],
                           address={"city": "New York",
                                    "country": "USA",
                                    "zip": "12345",
                                    "addr_string": "Some street 123"})
    id_1 = storage.create(contact)
    print(id_1)
    contact = ContactModel(name="Doe John",
                           email="some@where.com",
                           birthdate="1980-01-01",
                           phones=[{"phone": "1234567890"},
                                   {"phone": "   123456 "}],
                           address={"city": "New York",
                                    "country": "USA",
                                    "zip": "12345",
                                    "addr_string": "Some street 123"})
    id_2 = storage.create(contact)
    print(id_2)
    storage.commit()
    update_contact = ContactModel(name="Marie Jane")
    storage.update(update_contact, id_1, strict=True)
    storage.delete(id_2)
    storage.commit()
    print(storage.container)

