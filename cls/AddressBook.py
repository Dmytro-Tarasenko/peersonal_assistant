from collections import UserDict
from typing import List
from datetime import datetime
import re


class Field:
    """
    Base class for address book fields.
    """
    def __init__(self, value: str):
        """
        Initializes a field with a value.
        :param value: Field value.
        """
        self.value = value

    def __repr__(self) -> str:
        """
        Returns the string representation of the field value.
        """
        return str(self.value)


class Name(Field):
    """
    A class for a name in an address book.
    """
    pass


class Birthday(Field):
    """
    Birthday class in the address book.
    """
    def __init__(self, value: str):
        """
        Initializes the birthday with a value.
        :param value: The birthday value in the string format 'DD-MM-YYYY'.
        """
        self.value = datetime.strptime(value, '%d-%m-%Y')

    def __repr__(self) -> str:
        """
        Returns a string representation of the birthday
        in the format 'DD-MM-YYYY'.
        """
        return self.value.strftime('%d-%m-%Y')


class Address(Field):
    """Class representing an address."""
    def __init__(self,
                 country: str = "",
                 zip_code: int = None,
                 city: str = "",
                 street: str = "",
                 house: str = "",
                 apartment: str = ""):
        """Initialize an Address object.
        Args:
            country (str): The country.
            zip_code (int): The postal code.
            city (str): The city.
            street (str): The street.
            house (str): The house number.
            apartment (str): The apartment number.
        """
        self.country = country.capitalize()
        self.zip_code = zip_code
        self.city = city.capitalize()
        self.street = street.capitalize()
        self.house = house
        self.apartment = apartment

    def __repr__(self) -> str:
        """Return a string representation of the Address object."""
        return (
            f'{self.country}, '
            f'{self.zip_code}, '
            f'{self.city}, '
            f'str. {self.street}, '
            f'bld. {self.house}, '
            f'app. {self.apartment}'
        )


class Record:
    """
    Class for writing in the address book.
    """
    def __init__(self,
                 name: str = "",
                 birthday: str = "",
                 email: str = "",
                 address: Address = None,
                 phones: List[str] = None):
        """
        Initializes a record.
        :param name: Name to record.
        :param birthday: Birthday to record in string format 'DD-MM-YYYY'.
        This field is optional.
        """
        self.name = name
        self.birthday = birthday
        self.address = address
        self.email = email
        self.phones = phones if phones else []

    def add_phone(self, value: str):
        """
        Adds a phone number to a record.
        :param value: The phone number to add.
        """
        self.phones.append(value)

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
        if self.birthday:
            self.birthday = value
        else:
            self.birthday = Birthday(value)

    def __repr__(self) -> str:
        """
        Returns the string representation of the record.
        """
        phones = ('|'.join(str(phone) for phone in self.phones)
                  if self.phones else 'None')
        return (
            f"Name: {self.name}, "
            f"phones: {phones}, "
            f"Address: {self.address}, "
            f"email: {self.email}, "
            f"Birthday: {self.birthday}"
        )

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """
        Changes the old phone number to the new one.
        Parameters:
        old_phone (str): Old phone number to change.
        new_phone (str): New phone number to replace the old one.
        Returns: None
        """
        for phone in self.phones:
            if phone == old_phone:
                phone_id = self.phones.index(phone)
                self.phones[phone_id] = new_phone
                break
        else:
            raise ValueError("phone_not_found")

    def remove_phone(self, value: str) -> None:
        """
        Removes a phone number from the phone list.
        Parameters:
        value (str): The phone number to delete.
        Returns: None
        """
        for phone in self.phones:
            if phone == value:
                self.phones.remove(phone)
                break
        else:
            raise ValueError("phone_not_found")

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
        name_str = f"$NAME${self.name}"
        address_str = f"$ADDRESS${self.address}"
        email_str = f"$EMAIL${self.email}"
        phones_str = f"$PHONES${'| '.join(str(p) for p in self.phones)}"
        bday_str = f"$BDAY${self.birthday if self.birthday else ''}"
        return (
            f"{name_str}::"
            f"{address_str}::"
            f"{email_str}::"
            f"{phones_str}::"
            f"{bday_str}"
        )


class AddressBook(UserDict):
    """Class representing an address book."""

    def __iter__(self) -> iter:
        """Return an iterator over the records in the address book."""
        return iter(self.data.values())

    def __getitem__(self, key):
        """Get an item from the address book."""
        return self.data[key.search_str]

    def print_address_book(self):
        """Print all records in the address book."""
        for record in self.values():
            print(record)

    def add_record(self, record: 'Record') -> None:
        """Add a new entry to the address book.

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

    def delete_record(self, record: 'Record') -> None:
        """Delete a record from the address book.
        Args:
            record (Record): The record to be deleted.
        """
        if record.name in self.data:
            del self.data[record.name]
        else:
            raise ValueError("No_find_records")

    def upcoming_birthdays(self) -> List[Record]:
        """Return a list of contacts with birthdays upcoming from
        tomorrow to 7 days ahead.
        Returns: List[Record]: List of records with upcoming birthdays.
        """
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        upcoming_date = tomorrow + datetime.timedelta(days=6)
        upcoming_contacts = [
            record for record in self.values()
            if tomorrow <= record.birthday <= upcoming_date
        ]
        return upcoming_contacts

    def find_record(self, search_params: List[str]) -> List[Record]:
        """
        Finds records in the address book based on a list of search parameters.

        Args:
            search_params (List[str]): A list of search parameters.

        Returns:
            List[Record]: A list of the found records.
        """

        search_exprs = [re.compile(f"({search_param})")
                        for search_param in search_params]

        results = []
        for record in self.values():
            for search_expr in search_exprs:
                if search_expr.search(record.search_str):
                    results.append(record)
                    break

        return results