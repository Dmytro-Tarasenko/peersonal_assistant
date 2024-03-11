from interfaces import AbcBook
from models.ABModels import PhoneModel, ContactModel, AddressModel


class Record:
    """Record class contains contact information and provides basic operations"""
    contact: ContactModel

    def find_phone(self, search_phone: str) -> PhoneModel | None:
        """Finds phone in Contact."""
        for phone in self.contact.phones:
            if phone == search_phone:
                return phone

    def add_phone(self, phone: str) -> bool:
        """Adds phone to phone list"""
        if not self.find_phone(phone):
            self.contact.phones.append(PhoneModel(phone=phone))
            return True
        raise ValueError(f"Phone already exists: {phone}")

    def edit_phone(self, old_phone: str, new_phone: str) -> bool:
        """Replaces old phone with new one"""
        for ind, phone in enumerate(self.contact.phones):
            if phone == old_phone:
                self.contact.phones[ind] = PhoneModel(phone=new_phone)
                return True
        raise ValueError(f"Phone not found: {old_phone}")

    def delete_phone(self, del_phone: str) -> bool:
        """Deletes phone from phones list"""
        for ind, phone in enumerate(self.contact.phones):
            if phone == del_phone:
                self.contact.phones.pop(ind)
                return True
        raise ValueError(f"Phone not found: {del_phone}")

    def record_dumps(self) -> str:
        """Returns json dump of the record"""
        return self.contact.model_dump_json()
