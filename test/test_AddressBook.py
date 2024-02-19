# AddressBook tests go here
from pimp.cls.AddressBook import AddressBook, Record, Birthday, Address, Phone
from datetime import datetime
import pytest

ab = AddressBook()

rec = Record(name="Vasyl Petrenko")
rec.birthday = Birthday(date=(datetime.strptime("13-01-1990", "%d-%m-%Y").date()))
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

assert ab.add_record(rec) is True
with pytest.raises(KeyError,
                   match="Record Vasyl Petrenko already exists"):
    ab.add_record(rec)

rec = Record(name="Vasylyna Vlashchenko")
rec.birthday = Birthday(date=(datetime.strptime("13-02-1999", "%d-%m-%Y").date()))
adr = Address(country="Ukraine",
              city="Kharkiv",
              zip=61001,
              street="maydan Nezalezhnosty",
              house=9,
              apartment=12)

rec.phones = [Phone(number=7482984023)]
rec.email = "nifiga@nide.nema"

ab.add_record(rec)

rec = Record(name="Jeorge Cassius")
rec.birthday = Birthday(date=(datetime.strptime("15-06-1999", "%d-%m-%Y").date()))
adr = Address(country="Republica de Cabo Verde",
              city="Boa Vista")

rec.phones = [Phone(number=5869471425)]
rec.email = "vista@rio.cv"

ab.add_record(rec)

assert ab.record_counter == 3
assert ab.record_id == 3

ab.delete_record(rec)
ab.add_record(rec)

assert ab.records_quantity == 3
assert ab.record_id == 4

ab.delete_record(rec)
ab.add_record(rec)

assert ab.record_id == rec.id == 5

rec1 = Record(name="Gustavo Gaviria")
rec1.address = rec.address
rec1.phones = rec.phones
rec1.birthday = rec.birthday

assert ab.data[5].name != rec1.name

ab.edit_record(rec, rec1)

assert ab.data[5].name == rec1.name
assert ab.records_quantity == 3
assert ab.record_id == 5
