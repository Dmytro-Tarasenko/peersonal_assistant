from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Birthday(Field):
    pass


class Phone(Field):
    pass


class Address(Field):
    def __init__(self, capitalize=None, zip=None, city=None,
                  street=None, house=None, apartment=None):
        self.capitalize = capitalize
        self.zip = zip
        self.city = city
        self.street = street
        self.house = house
        self.apartment = apartment

    def __str__(self):
        capitalize = f"Capitalize: {self.capitalize}"
        zip = f"Zip: {self.zip}"
        city = f"City: {self.city}"
        street = f"Street: {self.street}"
        house = f"House: {self.house}"
        apartment = f"Apartment: {self.apartment}"
        return f"{capitalize}, {zip}, {city}, {street}, {house}, {apartment}"


class Email(Field):
    pass


class Record:
    def __init__(self, name, address=None, email=None, birthday=None):
        self.name = Name(name)
        self.birthday = Birthday(birthday)
        self.address = Address(address)
        self.email = Email(email)
        self.phones = []

    def add_phone(self, value):
        self.phones.append(Phone(value))

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                break
        else:
            raise ValueError(f"Phone number {old_phone} not found")

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break
        else:
            raise ValueError(f"Phone number {phone} not found")

    def find_phone(self, value):
        for phone in self.phones:
            if value == phone.value:
                return phone

    def __str__(self):
        contact_name = f"Contact name: {self.name.value}"
        addreses = f"Address: {self.address}"
        email = f"email: {self.email}"
        phones = f"phones: {'| '.join(p.value for p in self.phones)}"
        bday = f"Birthday: {self.birthday}"
        return f"{contact_name}, {phones}, {addreses}, {email}, {bday}"

    def days_to_birthday(self):
        if self.birthday:
            now = datetime.now()
            next_birthday = datetime(now.year, self.birthday.date.month,
                                     self.birthday.date.day)
            if now > next_birthday:
                next_birthday = datetime(now.year + 1,
                                         self.birthday.date.month,
                                         self.birthday.date.day)
            return (next_birthday - now).days
        else:
            raise ValueError("Birthday not set")

    @property
    def search_str(self) -> str:
        name_str = f"$NAME${self.name.value}"
        address_str = f"$ADDRESS${', '.join(str(a) for a in self.address)}"
        email_str = f"$EMAIL${self.email}"
        phones_str = f"$PHONES${'| '.join(str(p) for p in self.phones)}"
        bday_str = f"$BDAY${self.birthday.value if self.birthday else ''}"
        return f"{name_str}::{address_str}::{email_str}::{phones_str}:
        :{bday_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        if record.name.value not in self.data:
            self.data[record.name.value] = record
        else:
            raise ValueError(f"Record: {record.name.value} already exists.")

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def __str__(self):
        records = "|".join(str(record) for record in self.data.values())
        return f"AddressBook({records})"