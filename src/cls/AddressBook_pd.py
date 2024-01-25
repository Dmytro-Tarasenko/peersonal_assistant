from collections import UserDict
from typing import List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict, PositiveInt, PastDate
import re


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
    zip_code: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    house: Optional[str] = None
    apartment: Optional[str] = None

    @property
    def as_string(self):
        parts = [*self]
        return " ".join([part[1] for part in parts if part[1]])

    @field_validator("zip_code")
    @classmethod
    def zip_code_valid(cls, value: str) -> str:
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
    def phones_valid(cls, value: str):
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

    name: str
    birthday: Optional[Birthday] = None
    email: Optional[EmailStr] = None
    address: Optional[Address] = None
    phones: List[Phone] = []

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
        for phone in self.phones:
            if phone == old_phone:
                self.phones.pop(phone)
                self.phones.append(new_phone)
                return True
        raise ValueError(f"Phone {old_phone.number} is not found")

    def delete_phone(self, del_phone: Phone) -> bool:
        for phone in self.phones:
            if phone == del_phone:
                self.phones.pop(phone)
                return True
        raise ValueError(f"Phone {del_phone.number} is not found")

    def set_address(self,
                    address: Address):
        """
        Adds or edit an address in a record.
        """
        if address:
            self.address = address
        else:
            raise ValueError("Could not process empty address")

    def set_email(self, value: EmailStr):
        """
        Adds or updates email in a record.
        :param value: Email to add.
        """
        if value:
            self.address.email = value
        else:
            raise ValueError("Could not process empty email")

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

    def del_address(self) -> None:
        """
        Deletes the address from the record.
        Returns: None
        """
        self.address = Address()

    def del_email(self) -> None:
        """
        Deletes an email from a record.
        Returns: None
        """
        self.email = None

    @property
    def search_str(self) -> str:
        name_str = f"%NAME%{self.name}"
        address_str = f"%ADDRESS%{self.address.as_string}"
        email_str = f"%EMAIL%{self.email}"
        phones_str = f"%PHONES%{'|'.join(str(p.number) for p in self.phones)}"
        bday_str = f"%BDAY%{self.birthday.local_str if self.birthday else ''}"
        return (
            f"{name_str}::"
            f"{address_str}::"
            f"{email_str}::"
            f"{phones_str}::"
            f"{bday_str}::"
        )


class AddressBook(UserDict[str, Record]):
    """Class representing an address book."""
    def __getitem__(self, name: str) -> Record | None:
        if name in self.data:
            return self.data.get(name)

    def iterator(self) -> Record:
        """Return an iterator over the records in the address book."""
        yield self.data.values()

    def add_record(self, record: Record) -> None:
        """Додайте новий запис до адресної книги.

        Args:
            record (Record): The record to be added.
        """
        self.data[record.name] = record

    def edit_record(self,
                    old_record: Record,
                    new_record: Record) -> None:
        """Edit an existing record in the address book.
        Args:
            old_record (Record): The current record to be edited.
            new_record (Record): The new record.
        """
        if old_record.name in self.data:
            self.data.pop[old_record.name]
            self.add_record(new_record)
        else:
            raise ValueError("no_such_record")

    def delete_record(self, name: str) -> None:
        """Delete a record from the address book.
        Args:
            name (str): name of record to delete.
        """
        if name in self.data:
            self.data.pop(name)
        else:
            raise ValueError("no_such_record")

    def upcoming_mates(self, days: int) -> List[Record]:
        """Return a list of contacts with birthdays upcoming from tomorrow to 7 days ahead.
        Returns: List[Record]: List of records with upcoming birthdays.
        """
        res = []
        for record in self.data.values():
            if 1 <= record.birthday.days_to_birthday <= days:
                res.append(record)

        return res

    def today_mates(self) -> List[Record]:
        res = []
        for record in self.data.values():
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
