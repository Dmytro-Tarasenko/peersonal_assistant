import faker
import pickle
from cls.AddressBook import Record, Address, AddressBook

fake = faker.Faker()


def generate_contact():
    name = fake.name()
    phone = [fake.phone_number()]
    bday = fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%d-%m-%Y")
    email = fake.email()

    country = fake.country()
    zip_code = fake.zipcode()
    city = fake.city()
    street = fake.street_name()
    house = fake.building_number()
    apartment = fake.random_int(min=1, max=100)

    adr = Address(country=country, zip_code=zip_code, city=city,
                  street=street, house=house, apartment=apartment)
    rec = Record(name=name, birthday=bday, phones=phone,
                 email=email, address=adr)

    return rec


def address_book_generator():
    ab = AddressBook()
    for _ in range(10):
        contact = generate_contact()
        ab.add_record(contact)
    return ab


address_book = address_book_generator()


with open('data/addressbook.bin', 'wb') as f:
    pickle.dump(address_book, f)

with open('data/addressbook.bin', 'rb') as f:
    address_book = pickle.load(f)
print(address_book)
