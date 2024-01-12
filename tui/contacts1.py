from collections import UserDict
from datetime import datetime


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

    def __str__(self) -> str:
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

    def __str__(self) -> str:
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
    """
    A class for an address in an address book.
    """
    def __init__(self,
                 capitalize: str = None,
                 zip_code: str = None,
                 city: str = None,
                 street: str = None,
                 house: str = None,
                 apartment: str = None):
        """
        Initializes an address with details.
        :param capitalize: Area name.
        :param zip_code: Zip code.
        :param city: Name of the city.
        :param street: Street name.
        :param house: House number.
        :param apartment: Apartment number.
        """
        self.capitalize = capitalize
        self.zip_code = zip_code
        self.city = city
        self.street = street
        self.house = house
        self.apartment = apartment

# чи треба методи додавання полів в class Address(Field):
# як я зробив це нижче? якщо треба , то дороблю док стринги.

    def _add_capitalize(self, value: str):
        self.capitalize = value

    def _add_zip_code(self, value: str):
        self.zip_code = value

    def _add_city(self, value: str):
        self.city = value

    def _add_street(self, value: str):
        self.street = value

    def _add_house(self, value: str):
        self.house = value

    def _add_apartment(self, value: str):
        self.apartment = value

    def __str__(self) -> str:
        """
        Returns the string representation of the address.
        """
        capitalize = f"Capitalize: {self.capitalize}"
        zip_code = f"Zip: {self.zip_code}"
        city = f"City: {self.city}"
        street = f"Street: {self.street}"
        house = f"House: {self.house}"
        apartment = f"Apartment: {self.apartment}"
        return (
            f"{capitalize}, "
            f"{zip_code}, "
            f"{city}, "
            f"{street}, "
            f"{house}, "
            f"{apartment}"
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
    def __init__(self, name: str, birthday: str = None):
        """
        Initializes a record with name and birthday.
        :param name: Name to record.
        :param birthday: Birthday to record in string format 'DD-MM-YYYY'.
        This field is optional.
        """
        self.name = Name(name)
        self.birthday = Birthday(birthday) if birthday else None
        self.address = []
        self.email = []
        self.phones = []

    def add_phone(self, value: str):
        """
        Adds a phone number to a record.
        :param value: The phone number to add.
        """
        self.phones.append(Phone(value))

    def add_address(self,
                    capitalize: str = None,
                    zip_code: str = None,
                    city: str = None,
                    street: str = None,
                    house: str = None,
                    apartment: str = None):
        """
        Adds an address to a record.
        :param capitalize: Area name.
        :param zip_code: Zip code.
        :param city: Name of the city.
        :param street: Street name.
        :param house: House number.
        :param apartment: Apartment number.
        """
        self.address.append(Address(capitalize, zip_code, city,
                                    street, house, apartment))

    def add_email(self, value: str):
        """
        Adds an email to a record.
        :param value: Email to add.
        """
        self.email.append(Email(value))

    def add_birthday(self, value: str):
        """
        Adds or changes a birthday in a record.
        :param value: The birthday to add or change
        in the string format 'DD-MM-YYYY'.
        """
        self.birthday = Birthday(value)

# ЩО ТРЕБА ЗМІНИТИ, ДОРОБИТИ, ВИДАЛИТИ ТА ІНШІ ЗАУВАЖЕННЯ ПО КОДУ ВИЩЕ?
# ДАЛІ З КОДОМ НИЖЧЕ БУДУ ПРАЦЮВАТИ:

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
        return (
            f"{name_str}::"
            f"{address_str}::"
            f"{email_str}::"
            f"{phones_str}::"
            f"{bday_str}"
        )


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
