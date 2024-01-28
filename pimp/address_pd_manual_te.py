from pimp.cls.AddressBook_pd import Address, Phone, Birthday
from datetime import datetime, timedelta

adr = Address(zip_code=12346)
adr.zip_code = 54321
print(adr)

phone1 = Phone(number=1234567890)
phone2 = Phone(number="1234567890")

print(phone1 == phone2)

print(phone1 == Phone(number=1234567890))

bd = Birthday(date=(datetime.today().date()-timedelta(days=132540)))

print(bd.local_str)
