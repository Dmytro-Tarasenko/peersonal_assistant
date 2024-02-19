from collections import UserDict
from typing import List, Optional
from datetime import datetime
from pydantic import (BaseModel,
                      EmailStr,
                      field_validator,
                      ConfigDict,
                      PastDate)
import re
from interfaces.AbcBook import Book


class ZipFormatError(Exception):
    """Custom error that is raised when zip is not of a right format"""

    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


class PhoneNumberError(Exception):
    """Custom error that is raised when phone number is not valid"""

    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


class Address(BaseModel):
    """Class representing an address."""
    model_config = ConfigDict(coerce_numbers_to_str=True)

    country: Optional[str] = None
    zip: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    house: Optional[str] = None
    apartment: Optional[str] = None

    @property
    def as_string(self):
        parts = [*self]
        return " ".join([part[1] for part in parts if part[1]])

    @field_validator("zip")
    @classmethod
    def zip_valid(cls, value: str) -> str:
        if not value.isdigit() or len(value) != 5:
            raise ZipFormatError(value=value,
                                 message="ZIP should contain 5 digits.")

        return value


class Phone(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True,
                              validate_assignment=True)
    number: str

    @field_validator("number")
    @classmethod
    def phones_valid(cls, value: str) -> str:
        if not value.isdigit() or len(value) != 10:
            raise PhoneNumberError(value=value,
                                   message=(f"{value} is not valid. Phone number "
                                            + "should consist of 10 digits."))

        return value


class Birthday(BaseModel):
    """Birthday with local string property"""
    model_config = ConfigDict(validate_assignment=True)

    date: PastDate

    @property
    def local_str(self) -> str:
        return self.date.strftime("%d-%m-%Y")

    @property
    def days_to_birthday(self) -> int:
        cur_year = datetime.today().year
        bday_to_be = datetime(day=self.date.day,
                              month=self.date.month,
                              year=cur_year).date()
        if bday_to_be < datetime.today().date():
            bday_to_be = datetime(day=self.date.day,
                                  month=self.date.month,
                                  year=cur_year+1).date()
        return (bday_to_be - datetime.today().date()).days


class Record(BaseModel):
    """
    Class for writing in the address book.
    """
    model_config = ConfigDict(coerce_numbers_to_str=True,
                              validate_assignment=True)

    id: int = 0
    name: str
    birthday: Optional[Birthday] = None
    email: Optional[EmailStr] = None
    address: Optional[Address] = None
    phones: Optional[List[Phone]] = None

    def add_phone(self, value: Phone) -> bool:
        """
        Adds a phone number to a record.
        :param value: The phone number to add.
        """
        if isinstance(value, Phone) and value.number:
            self.phones.append(value)
            return True
        else:
            raise ValueError(f"{value} is not a valid Phone instance")

    def edit_phone(self,
                   old_phone: Phone,
                   new_phone: Phone) -> bool:
        for index, phone in enumerate(self.phones):
            if phone == old_phone:
                self.phones.pop(index)
                self.phones.append(new_phone)
                return True

        raise ValueError(f"Phone {old_phone.number} is not found")

    def delete_phone(self, del_phone: Phone) -> bool:
        for index, phone in enumerate(self.phones):
            if phone == del_phone:
                self.phones.pop(index)
                return True

        raise ValueError(f"Phone {del_phone.number} is not found")

    def set_address(self,
                    address: Address) -> bool:
        """
        Adds or edit an address in a record.
        """
        if isinstance(address, Address) and address.as_string != "":
            self.address = address
            return True
        else:
            raise ValueError("Could not process empty address. Use "
                             + "delete_address to wipe address from record")

    def set_email(self, value: EmailStr) -> bool:
        """
        Adds or updates email in a record.
        :param value: Email to add.
        """
        if value:
            self.email = value
            return True
        else:
            raise ValueError("Could not process empty email")

    def delete_email(self) -> None:
        """
        Deletes an email from a record.
        Returns: None
        """
        self.email = None

    def set_birthday(self, value: str):
        """
        Adds or changes a birthday in a record.
        :param value: The birthday to add or change
        in the string format 'DD-MM-YYYY'.
        """
        if value:
            self.birthday = Birthday(value)
        else:
            raise ValueError("Could not process empty birthday")

    def delete_address(self) -> bool:
        """
        Deletes the address from the record.
        Returns: None
        """
        if self.address:
            self.address = None
            return True
        raise ValueError("Record got no address field")

    @property
    def search_str(self) -> str:
        name_str = self.name
        address_str = self.address.as_string if self.address else ""
        email_str = self.email
        phones_str = '|'.join(str(p.number) for p in self.phones)
        bday_str = self.birthday.local_str if self.birthday else ""
        return (
            f"%NAME%{name_str}::"
            f"%ADDRESS%{address_str}::"
            f"%EMAIL%{email_str}::"
            f"%PHONES%{phones_str}::"
            f"%BDAY%{bday_str}::"
        )


class AddressBook(Book, UserDict[int, Record]):
    """Class representing an address book."""
    def __getitem__(self, name: str) -> Record | None:
        """Return a record from the address book by name."""
        for record in self.data.values():
            if record.name == name:
                return record

    def iterator(self) -> Record:
        """Return an iterator over the records in the address book."""
        for _ in range(self.records_quantity):
            yield self.get_records(_, 1)[0]

    def get_records(self, start: int = 0, limit: int = 5) -> List[Record]:
        """Return a list of records from the address book.

        Args:
            start (int): The start index.
            limit (int): The quantity of records.

        Returns:
            List[Record]: A list of records from the address book.
        """
        return list(self.data.values())[start: start + limit]

    def add_record(self, record: Record) -> bool:
        """Додайте новий запис до адресної книги.

        Args:
            record (Record): The record to be added.
        """
        if not self.get(record.name):
            AddressBook.record_counter += 1
            AddressBook.record_id += 1
            record.id = AddressBook.record_id
            self.data[record.id] = record
            return True

        raise KeyError(f"Record {record.name} already exists")

    def edit_record(self,
                    old_record: Record,
                    new_record: Record) -> bool:
        """Edit an existing record in the address book.
        Args:
            old_record (Record): The current record to be edited.
            new_record (Record): The new record.
        """
        if old_record.id in self.data:
            new_record.id = old_record.id
            self.data[new_record.id] = new_record
            return True
        else:
            raise ValueError("no_such_record")

    def delete_record(self, record: Record) -> None:
        """Delete a record from the address book.
        Args:
            record (Record): The record to delete.
        """
        if record.id in self.data:
            self.data.pop(record.id)
            AddressBook.record_counter -= 1
        else:
            raise ValueError("no_such_record")

    def upcoming_mates(self, days: int) -> List[Record]:
        """Return a list of contacts with birthdays upcoming from tomorrow to 7 days ahead.
        Returns: List[Record]: List of records with upcoming birthdays.
        """
        res = []
        for record in self.data.values():
            if record.birthday:
                if 1 <= record.birthday.days_to_birthday <= days:
                    res.append(record)

        return res

    def today_mates(self) -> List[Record]:
        res = []
        for record in self.data.values():
            if record.birthday:
                if record.birthday.days_to_birthday == 0:
                    res.append(record)
        return res

    def find_record(self, search_params: List[str]) -> List[Record]:
        """
        Finds records in the address book based on a list of search parameters.

        Args:
            search_params (List[str]): A list of search parameters.

        Returns:
            List[Record]: A list of the found records.
        """
        regexp_block = r"[\w\.\, ]*"
        search_exprsns = []
        for param in search_params:
            param = (param.replace("\\", "")
                     .replace(".", "")
                     .replace("-", "")
                     .replace(",", ""))
            search_field,  search_cond = param.rsplit("%", maxsplit=1)
            search_field += "%"
            search_exprsns.append(rf"{search_field}{regexp_block}"
                                  + rf"{search_cond}{regexp_block}::")

        results = []
        for record in self.values():
            for search_expr in search_exprsns:
                if re.search(search_expr, record.search_str, re.I):
                    results.append(record)
                    break

        return results
