from cls.AddressBook_pd import Address, Phone

adr = Address(zip_code=12346)
adr.zip_code = 54321
print(adr)

phone1 = Phone(number=1234567890)
phone2 = Phone(number="1234567890")

print(phone1 == phone2)
