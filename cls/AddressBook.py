from collections import UserDict
from typing import List
import datetime


class Address:
    """Class representing an address."""
    def __init__(self, country: str, zip_code: int, city: str, street: str, house: str, apartment: str):
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

    def __repr__(self):
        """Return a string representation of the Address object."""
        return f"{self.country}|{self.zip_code}|{self.city}|{self.street}|{self.house}|{self.apartment}"


class AddressBook(UserDict):
    """Class representing an address book."""
    def add_record(self, record: 'Record') -> None:
        """Add a new record to the address book.

        Args:
            record (Record): The record to be added.
        """
        self.data[record.search_str] = record

    def edit_record(self, old_record: 'Record', new_record: 'Record') -> None:
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

    def upcoming_birthdays(self, days: int = 7) -> List['Record']:
        """Return a list of contacts with birthdays upcoming in the specified number of days.

        Args:
            days (int): The number of days to look ahead.

        Returns:
            List[Record]: List of records with upcoming birthdays.
        """
        today = datetime.date.today()
        upcoming_date = today + datetime.timedelta(days=days)
        upcoming_contacts = [record for record in self.values() if record.birthday == upcoming_date]
        return upcoming_contacts


if __name__ == "__main__":
    address_book = AddressBook()
