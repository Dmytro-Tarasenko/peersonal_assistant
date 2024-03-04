from interfaces import AbcBook
from models.ABModels import PhoneModel, ContactModel, AddressModel


class Record:
    """Record class contains contact information and provides basic operations"""
    id: int = 0
    contact: ContactModel

    def find_phone(self, phone: str) -> PhoneModel | None:
        """Finds phone in Contact."""
        pass

    def add_phone(self, phone: str) -> bool:
        pass

    def edit_phone(self, old_phone: str, new_phone: str) -> PhoneModel | None:
        pass

    def delete_phone(self, phone: str) -> bool:
        pass
