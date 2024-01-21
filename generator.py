import faker
import pickle
from cls.AddressBook_pd import Record, Address, AddressBook
from random import randrange
fake = faker.Faker()

def make_phone():
    phone = ""
    for _ in range(10):
        phone += str(randrange(0, 10))
    return phone

def generate_contact():
    name = fake.name()
    phone = [make_phone()]
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
    for _ in range(15):
        contact = generate_contact()
        ab.add_record(contact)
    return ab

address_book = AddressBook()
address_book = address_book_generator()

with open('data/addressbook.bin', 'wb') as f:
    pickle.dump(address_book, f)

with open('data/addressbook.bin', 'rb') as f:
    address_book: AddressBook = pickle.load(f)

print(address_book.upcoming_mates(40))
print(address_book.today_mates())



