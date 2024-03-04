from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    PastDate,
)
from typing import Optional, Set


class AddressModel(BaseModel):
    addr_string: Optional[str]
    city: Optional[str]
    country: Optional[str]
    zip: Optional[str] = Field(min_length=4, max_length=6)


class PhoneModel(BaseModel):
    model_config = {
        "str_strip_whitespace": "True",
        "coerce_numbers_to_string": "True",
    }
    phone: str = Field(min_length=6,
                       max_length=12,
                       pattern=r"^\d{6,12}$")


class ContactModel(BaseModel):
    name: str
    email: Optional[EmailStr]
    birthdate: Optional[PastDate]
    phones: Optional[Set[PhoneModel]]
    address: Optional[AddressModel]


if __name__ == "__main__":
    contact = ContactModel(name="John Doe",
                           email="some@where.com",
                           birthdate="1980-01-01",
                           phones=[{"phone": "1234567890"},
                                    {"phone": "   123456 "}],
                           address={"city": "New York",
                                    "country": "USA",
                                    "zip": "12345",
                                    "addr_string": "Some street 123"})
    print(contact.model_dump_json())
    print(contact.model_dump())
    print(contact)
    print(type(contact.birthdate))
