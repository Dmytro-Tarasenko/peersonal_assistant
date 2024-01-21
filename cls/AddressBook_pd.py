from collections import UserDict
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
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
                                   message=("{value} is not valid. Phone number "
                                            + "should consist of 10 digits."))

        return value


class Record(BaseModel):
    """
    Class for writing in the address book.
    """
    name: str
    birthday: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Address = Address()
    phones: List[Phone] = []

    def add_phone(self, value: str | int):
        """
        Adds a phone number to a record.
        :param value: The phone number to add.
        """
        self.phones.append(Phone(value))

    def add_edit_address(self,
                         address: Address = Address()):
        """
        Adds or edit an address in a record.
        """
        self.address = address

    def add_edit_email(self, value: str = ""):
        """
        Adds or updates email in a record.
        :param value: Email to add.
        """
        self.address.email = value

    def add_edit_birthday(self, value: str):
        """
        Adds or changes a birthday in a record.
        :param value: The birthday to add or change
        in the string format 'DD-MM-YYYY'.
        """
        self.birthday = value

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
        address_str = f"%ADDRESS%{self.address}"
        email_str = f"%EMAIL%{self.email}"
        phones_str = f"%PHONES%{'|'.join(str(p) for p in self.phones)}"
        bday_str = f"%BDAY%{self.birthday if self.birthday else ''}"
        return (
            f"{name_str}::"
            f"{address_str}::"
            f"{email_str}::"
            f"{phones_str}::"
            f"{bday_str}"
        )


class AddressBook(UserDict):
    """Class representing an address book."""
    def __getitem__(self, name: str) -> None:
        if name in self.data:
            return self.data.get(name)
        return None

    def iterator(self) -> Record:
        """Return an iterator over the records in the address book."""
        yield self.data.values()

    def print_address_book(self):
        """Print all records in the address book."""
        for record in self.values():
            print(record)

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
            raise ValueError("No_find_records")

    def delete_record(self, name: str) -> None:
        """Delete a record from the address book.
        Args:
            record (Record): The record to be deleted.
        """
        if self.data[name]:
            self.data.pop(name)
        else:
            raise ValueError("No_find_records")

    def upcoming_mates(self, days: int) -> List[Record]:
        """Return a list of contacts with birthdays upcoming from tomorrow to 7 days ahead.
        Returns: List[Record]: List of records with upcoming birthdays.
        """
        checks = []
        for inc in range(1, days+1):
            check = (datetime.today() + timedelta(days=inc)).strftime("%d-%m")
            checks.append(check)
        res = []
        for record in self.data.values():
            if record.birthday[:5] in checks:
                res.append(record)

        return res

    def today_mates(self) -> List[Record]:
        today_check = datetime.today().strftime("%d-%m")
        res = []
        for record in self.data.values():
            if record.birthday.startswith(today_check):
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
        search_exprs = []
        for param in search_params:
            param = (param.replace("\\", "")
                     .replace(".", "")
                     .replace("-", "")
                     .replace(",", ""))
            search_field,  search_cond = param.rsplit("%", maxsplit=1)
            search_field += "%"
            search_exprs.append(rf"{search_field}{regexp_block}"
                                 + rf"{search_cond}{regexp_block}::")

        results = []
        for record in self.values():
            for search_expr in search_exprs:
                if re.search(search_expr, record.search_str, re.I):
                    results.append(record)
                    break

        return results
