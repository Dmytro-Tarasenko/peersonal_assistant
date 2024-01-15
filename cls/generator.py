import faker
<<<<<<< Updated upstream
import pickle
from AddressBook import Record, Address, AddressBook
=======
>>>>>>> Stashed changes

fake = faker.Faker()


def generate_contact():
    name = fake.name()
<<<<<<< Updated upstream
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
address_book_list = list(address_book)

with open('addressbook.bin', 'wb') as f:
    pickle.dump(address_book_list, f)

with open('addressbook.bin', 'rb') as f:
    address_book_list = pickle.load(f)
print(address_book_list)
=======
    address = fake.address().replace('\n', '|')
    email = fake.email()
    phone = fake.phone_number()
    bday = fake.date_of_birth(minimum_age=18,
                              maximum_age=60).strftime("%d-%m-%Y")
    contact = f"$NAME${name}::$ADDRESS${address}::$EMAIL${email}"
    contact += f"::$PHONES${phone}::$BDAY${bday}"
    contact += f"\n|Contact name: {name}| phones: {phone}"
    contact += f"| Address: {address}| email: {email}| Birthday: {bday}|"
    return contact


for _ in range(10):
    print(generate_contact())
>>>>>>> Stashed changes
