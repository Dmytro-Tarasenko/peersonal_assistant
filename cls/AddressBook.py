from collections import UserDict
from typing import List
from datetime import *


class Field:
    """
    Base class for address book fields.
    """
    def __init__(self, value: str | int):
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

    def __le__(self, other: 'Birthday') -> bool:
        """Compare the birthday with another birthday."""
        return self.value.date() <= other.value.date()

    def __eq__(self, other: 'Birthday') -> bool:
        """Check if two birthdays are equal."""
        return self.value.date() == other.value.date()


class Phone(Field):
    """
    A class for a phone number in an address book.
    """
    pass


class Email(Field):
    """
    A class for email in the address book.
    """
    pass


class Address:
    """Class representing an address."""
    def __init__(self,
                 country: str,
                 zip_code: int,
                 city: str,
                 street: str,
                 house: str,
                 apartment: str):
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
        return f"{self.country}|{self.zip_code}|{self.city}|{self.street}|{self.house}|{self.apartment}"


class Record:
    """
    Class for writing in the address book.
    """
    def __init__(self,
                 name: str,
                 birthday: str = None,
                 email: str = None,
                 address: Address = None,
                 phones: List[Phone] = None):
        """
        Initializes a record.
        :param name: Name to record.
        :param birthday: Birthday to record in string format 'DD-MM-YYYY'.
        This field is optional.
        """
        self.name = Name(name)
        self.birthday = Birthday(birthday) if birthday else None
        self.address = address
        self.email = Email(email) if email else None
        self.phones = phones if phones is not None else []
        self.search_str = name.lower()

    def add_phone(self, value: str):
        """
        Adds a phone number to a record.
        :param value: The phone number to add.
        """
        self.phones.append(Phone(value))

    def add_edit_address(self,
                         country: str = None,
                         zip_code: int = None,
                         city: str = None,
                         street: str = None,
                         house: str = None,
                         apartment: str = None):
        """
        Adds or edit an address in a record.
        """
        if self.address:
            if country:
                self.address.country = country
            if zip_code:
                self.address.zip_code = zip_code
            if city:
                self.address.city = city
            if street:
                self.address.street = street
            if house:
                self.address.house = house
            if apartment:
                self.address.apartment = apartment
        else:
            self.address = Address(country, zip_code, city,
                                   street, house, apartment)

    def add_edit_email(self, value: str):
        """
        Adds or updates email in a record.
        :param value: Email to add.
        """
        if self.address:
            self.email = value
        else:
            self.email = Email(value)

    def add_edit_birthday(self, value: str):
        """
        Adds or changes a birthday in a record.
        :param value: The birthday to add or change
        in the string format 'DD-MM-YYYY'.
        """
        if self.birthday:
            self.birthday = Birthday(value)
        else:
            self.birthday = Birthday(value)

    def __repr__(self) -> str:
        """
        Returns the string representation of the record.
        """
        phones = (' | '.join(str(phone) for phone in self.phones)
                  if self.phones else 'None')
        return (
            f"|Contact name: {self.name}| "
            f"phones: {phones}| "
            f"Address: {self.address}| "
            f"email: {self.email}| "
            f"Birthday: {self.birthday}|"
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
            if phone.value == old_phone:
                phone.value = new_phone
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
            if phone.value == value:
                self.phones.remove(phone)
                break
        else:
            raise ValueError("phone_not_found")

    def del_address(self) -> None:
        """
        Deletes the address from the record.
        Returns: None
        """
        self.address = None

    def del_email(self) -> None:
        """
        Deletes an email from a record.
        Returns: None
        """
        self.email = None


class AddressBook(UserDict):
    """Class representing an address book."""

    def __iter__(self):
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
        """Додайте новий запис до адресної книги.

        Args:
            record (Record): Запис, який слід додати.
        """
        self.data[record.search_str] = record

    def edit_record(self,
                    old_record: Record,
                    new_record: Record) -> None:
        """Edit an existing record in the address book.

        Args:
            old_record (Record): The current record to be edited.
            new_record (Record): The new record.
        """
        if old_record.search_str in self.data:
            del self.data[old_record.search_str]
            self.add_record(new_record)

    def delete_record(self, record: 'Record') -> None:
        """Delete a record from the address book.

        Args:
            record (Record): The record to be deleted.
        """
        if record.search_str in self.data:
            del self.data[record.search_str]

    def upcoming_birthdays(self) -> List['Record']:
        """Return a list of contacts with birthdays upcoming from tomorrow to 7 days ahead.

        Returns:
            List[Record]: List of records with upcoming birthdays.
        """
        today = date.today()
        tomorrow = today + timedelta(days=1)
        upcoming_date = tomorrow + timedelta(days=6)

        upcoming_contacts = [
            record for record in self.values() 
            if record.birthday is not None and tomorrow <= record.birthday.value.date() <= upcoming_date
        ]

        return upcoming_contacts

    def find_record(self, search_param: str) -> 'Record':
        """Find a record in the address book based on search parameters.

        Args:
            search_param (str): Search parameter (e.g., name, birthday).

        Returns:
            Record: The found record.
        """
        for record in self.values():
            if (
                record.name.value.lower() == search_param.lower() or
                (record.birthday is not None and record.birthday.value.strftime('%d-%m-%Y') == search_param)
            ):
                return record

        raise ValueError("Record not found.")