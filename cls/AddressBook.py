from collections import UserDict
from typing import List
from datetime import datetime
import pickle

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


class Phone(Field):
    """
    A class for a phone number in an address book.
    """
    pass


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
            f'{self.country}|'
            f'{self.zip_code}|'
            f'{self.city}|'
            f'{self.street}|'
            f'{self.house}|'
            f'{self.apartment}'
        )


class Email(Field):
    """
    A class for email in the address book.
    """
    pass


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
        self.address = None
        self.email = Email(email) if email else None
        self.phones = []

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
            self.birthday = value
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

    @property
    def search_str(self) -> str:
        name_str = f"$NAME${self.name.value}"
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
        else:
            raise ValueError("No_find_records")

    def delete_record(self, record: 'Record') -> None:
        """Delete a record from the address book.
        Args:
            record (Record): The record to be deleted.
        """
        if record.search_str in self.data:
            del self.data[record.search_str]
        else:
            raise ValueError("No_find_records")

    def find_record(self, query: str) -> List['Record']:
        """Search for records in the address book.
        Args:
            query (str): The search query.
        Returns: List[Record] - List of records that match
        the search query.
        """
        records = [
            record for record in self.data.values()
            if query.lower() in record.search_str.lower()
        ]
        if not records:
            print("No_find_records")
        else:
            return records

    def print_address_book(self):
        for key, record in self.data.items():
            print(key)
            print(record)
            print()

    def upcoming_birthdays(self) -> List['Record']:
        """Return a list of contacts with birthdays upcoming from tomorrow to 7 days ahead.
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


address_book = AddressBook()
rec_1 = Record('Bill', '25-12-1990')
# print(rec_1)
rec_1.add_edit_address('Ukrane', '45125', 'Kyiv', 'Voli', '51', '150')
# print(rec_1)
rec_1.add_phone('1234567899')
# print(rec_1)
rec_1.add_edit_address(street='Svobody')
# print(rec_1)
rec_1.add_phone('7894561230')
# print(rec_1)
rec_1.add_edit_email('noe@gmd.pkj')
# print(rec_1)
rec_1.remove_phone('7894561230')
# print(rec_1)
rec_1.edit_phone('1234567899', '9994567890')
# print(rec_1)
# rec_1.del_address()
# print(rec_1)
rec_2 = Record('Noy', '05-02-1980', 'noy@gmail.poj')
# print(rec_2)
rec_2.add_phone('5196547535')
rec_2.add_edit_address('Ukrane', 78956, 'Dnepr', 'Molody', '78', '25')
rec_2.add_edit_birthday('10-10-1990')
# print(rec_2)
rec_2.add_edit_address(zip_code=78912)
# print(rec_2)
address_book.add_record(rec_1)
# print(dictions)
address_book.add_record(rec_2)
# print(dictions)
rec_3 = Record('Nam', '20-12-2000', 'name@gmail.com')
rec_3.add_phone('4444567855')
rec_3.add_edit_address('Ukraine', 95147, 'Dnepr', 'Soborna', '2', '50')
address_book.add_record(rec_3)
rec_2 = Record('Noy', '05-02-1980', 'noy@gmail.com')
rec_2.add_edit_address('Ukraine', 12345, 'Lviv', 'Voli', '205', '15')
rec_2.add_phone('1234561237895')
rec_2.add_phone('9595858575752')

address_book.add_record(rec_2)
address_book.add_record(rec_1)
rec_4 = Record('Kat', '15-01-1950', 'kat@kat.joy')
address_book.add_record(rec_4)
rec_new = Record('Pill', '25-12-1990')
address_book.add_record(rec_new)
record1 = Record("Іван", '06-07-1998', "ivan.petrov@example.com")
record2 = Record("Петро", '23-04-2005', "petro.ivanov@example.com")
address_book.add_record(record1)
address_book.add_record(record2)
record1.add_edit_birthday('23-04-2005')

rec_5 = Record('Dan', '25-12-2000', 'ghj@nji.gh')
rec_5.add_edit_address(country='Ukraine', zip_code=12345, city='Odesa', street='Voly', house= '10', apartment='5')
rec_5.add_phone('4555552123')
address_book.add_record(rec_5)

rec_7 = Record('Ivan', '24-02-2020', 'okj@noi.gh')
rec_7.add_edit_address(country='Ukraine', zip_code=78945, city='Fastov', street='Drugby', house= '140', apartment='54')
rec_7.add_phone('45558743642')
address_book.add_record(rec_7)

rec_6 = Record('Jolly', '05-12-1950', 'j@ji.gh')
rec_6.add_edit_address(country='USA', zip_code=58524, city='Orlean', street='New', house= '200', apartment='500')
rec_6.add_phone('23232323568945')
address_book.add_record(rec_6)

rec_8 = Record('Mary', '25-12-1984', 'g@ni.gh')
rec_8.add_edit_address(country='Poland', zip_code=45615, city='Lublin', street='Kurva', house= '6', apartment='45')
rec_8.add_phone('44444445115')
address_book.add_record(rec_8)

rec_9 = Record('Oly', '25-12-2000', 'ghj@nji.gh')
rec_9.add_edit_address(country='Ukraine', zip_code=85345, city='Odyn', street='Vody', house= '17', apartment='9')
rec_9.add_phone('66212352123')
address_book.add_record(rec_9)

rec_10 = Record('Dan', '25-12-2000', 'ghj@nji.gh')
rec_10.add_edit_address(country='Moldova', zip_code=58345, city='Kisiniv', street='Ukrainy', house= '62', apartment='1')
rec_10.add_phone('2589631475')
address_book.add_record(rec_10)
address_book.print_address_book()


with open('addressbook.bin', 'wb') as f:
    pickle.dump(address_book, f)
