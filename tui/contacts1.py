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
    """
    A class for an address in an address book.
    """
    def __init__(self,
                 capitalize: str = None,
                 zip_code:  int = None,
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

    def _add_capitalize(self, value: str):
        """
        Adds or changes the field name in the address.
        :param value: The name of the area to add or modify.
        """
        self.capitalize = value

    def _add_zip_code(self, value: int):
        """
        Adds or changes the postal code in the address.
        :param value: The zip code to add or change.
        """
        self.zip_code = value

    def _add_city(self, value: str):
        """
        Adds or changes the name of the city in the address.
        :param value: The name of the city to add or change.
        """
        self.city = value

    def _add_street(self, value: str):
        """
        Adds or changes the street name in the address.
        :param value: Street name to add or change.
        """
        self.street = value

    def _add_house(self, value: str):
        """
        Adds or changes the house number in the address.
        :param value: House number to add or change.
        """
        self.house = value

    def _add_apartment(self, value: str):
        """
        Adds or changes the apartment number in the address.
        :param value: Apartment number to add or change.
        """
        self.apartment = value

    def __repr__(self) -> str:
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
            f"|{capitalize} | "
            f"{zip_code} | "
            f"{city} | "
            f"{street} | "
            f"{house} | "
            f"{apartment} "
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
    def __init__(self, name: str, birthday: str = None, email: str = None):
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
                         capitalize: str = None,
                         zip_code: int = None,
                         city: str = None,
                         street: str = None,
                         house: str = None,
                         apartment: str = None):
        """
        Adds or edit an address in a record.
        """
        if self.address:
            if capitalize:
                self.address.capitalize = capitalize
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
            self.address = Address(capitalize, zip_code, city,
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
