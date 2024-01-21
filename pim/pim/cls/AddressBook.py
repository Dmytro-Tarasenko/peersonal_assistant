from collections import UserDict
from typing import List
from datetime import datetime, timedelta
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

    # def __repr__(self) -> str:
    #     """
    #     Returns the string representation of the field value.
    #     """
    #     return str(self.value)


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
                 country: str |None = None,
                 zip_code: str |None = None,
                 city: str |None = None,
                 street: str |None = None,
                 house: str |None = None,
                 apartment: str |None = None):
        """Initialize an Address object.
        Args:
            country (str): The country.
            zip_code (int): The postal code.
            city (str): The city.
            street (str): The street.
            house (str): The house number.
            apartment (str): The apartment number.
        """
        self.country = country.capitalize() if country else None
        self.zip_code = zip_code if zip_code else None
        self.city = city.capitalize() if city else None
        self.street = street.capitalize() if street else None
        self.house = house if house else None
        self.apartment = apartment if apartment else None

    def __repr__(self) -> str:
        """Return a string representation of the Address object."""
        country = f'{self.country}, ' if self.country else ""
        zip = f'{self.zip_code}, ' if self.zip_code else ""
        city = f'{self.city}, ' if self.city else ""
        street = f'str. {self.street}, ' if self.street else ""
        house = f'bld. {self.house}, ' if self.house else ""
        apprt = f'app. {self.apartment}, ' if self.apartment else ""
        return f"{country}{zip}{city}{street}{house}{apprt}"


class Record:
    """
    Class for writing in the address book.
    """
    def __init__(self,
                 name: str = "",
                 birthday: str = "",
                 email: str = "",
                 address: Address = Address(),
                 phones: List[str] = []):
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