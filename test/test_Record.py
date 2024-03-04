from pimp.cls.AddressBook import Record, Phone, Birthday, Address
from datetime import datetime
import pytest
import json

rec = Record(name="Vasyl Petrenko")
rec.birthday = Birthday(date=(datetime.strptime("13-01-1930", "%d-%m-%Y").date()))
adr = Address(country="Ukraine",
              city="Kharkiv",
              zip=61001,
              street="maydan Nezalezhnosty",
              house=7,
              apartment=8)

phones = [Phone(number=1234567890),
          Phone(number=2345678901),
          Phone(number=3456789012)]

rec.address = adr
rec.phones = phones
rec.email = "some.adr@some.dom"

check_str = ("%NAME%Vasyl Petrenko::"
             + "%ADDRESS%Ukraine 61001 Kharkiv maydan Nezalezhnosty 7 8::"
             + "%EMAIL%some.adr@some.dom::"
             + "%PHONES%1234567890|2345678901|3456789012::"
             + "%BDAY%13-01-1930::")

# search string creation
assert rec.search_str == check_str

# Phones block
with pytest.raises(ValueError, match="is not a valid Phone instance"):
    rec.add_phone(1234567890)

assert rec.add_phone(Phone(number=6789012345)) is True

check = [i.number for i in rec.phones]
assert "6789012345" in check

assert rec.edit_phone(old_phone=Phone(number=6789012345),
                      new_phone=Phone(number=6789012354)) is True

check = [i.number for i in rec.phones]
assert "6789012345" not in check
assert "6789012354" in check

with pytest.raises(ValueError,
                   match=f"Phone {6789012345} is not found"):
    rec.edit_phone(old_phone=Phone(number=6789012345),
                   new_phone=Phone(number=6789012354))

with pytest.raises(ValueError,
                   match=f"Phone {6789012345} is not found"):
    rec.delete_phone(Phone(number=6789012345))

rec.delete_phone(Phone(number=6789012354))

check = [i.number for i in rec.phones]
assert "6789012354" not in check

# email block
with pytest.raises(ValueError,
                   match="Could not process empty email"):
    rec.set_email("")

with pytest.raises(ValueError,
                   match="The email address is not valid"):
    rec.set_email("asdasd")

assert rec.set_email("some.adr2@some2.dom") is True

assert rec.email == "some.adr2@some2.dom"

rec.delete_email()
assert rec.email is None
rec.set_email("some.adr2@some2.dom")

# birthday block

# addres block
adr1 = Address()
with pytest.raises(ValueError,
                   match="Could not process empty address"):
    rec.set_address(adr1)

adr1 = Address(country="Ukraine",
               city="Kyiv",
               zip="01001",
               street="maydan Nezalezhnosty",
               house=7,
               apartment=8)

assert rec.set_address(adr1) is True

check_str = ("%NAME%Vasyl Petrenko::"
             + "%ADDRESS%Ukraine 01001 Kyiv maydan Nezalezhnosty 7 8::"
             + "%EMAIL%some.adr2@some2.dom::"
             + "%PHONES%1234567890|2345678901|3456789012::"
             + "%BDAY%13-01-1930::")

assert rec.search_str == check_str

assert rec.delete_address() is True

check_str = ("%NAME%Vasyl Petrenko::"
             + "%ADDRESS%::"
             + "%EMAIL%some.adr2@some2.dom::"
             + "%PHONES%1234567890|2345678901|3456789012::"
             + "%BDAY%13-01-1930::")

assert rec.search_str == check_str

with pytest.raises(ValueError,
                   match="Record got no address field"):
    rec.delete_address()
