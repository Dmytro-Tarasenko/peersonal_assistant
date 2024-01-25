from src.cls.AddressBook_pd import Record, Phone, Birthday, Address
from datetime import datetime, timedelta
import pytest

rec = Record(name="Vasyl Petrenko")
rec.birthday = Birthday(date=(datetime.today().date() - timedelta(days=34345)))
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

assert rec.search_str == ("%NAME%Vasyl Petrenko::"
                          + "%ADDRESS%Ukraine Kharkiv maydan Nezalezhnosty 7 8::"
                          + "%EMAIL%some.adr@some.dom::"
                          + "%PHONES%1234567890|2345678901|3456789012::"
                          + "%BDAY%13-01-1930::")

with pytest.raises(ValueError, match="is not a valid Phone instance"):
    rec.add_phone(1234567890)

assert rec.add_phone(Phone(number=6789012345)) == True

check = [i.number for i in rec.phones]

assert "6789012345" in check
