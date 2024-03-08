from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    PastDate,
)
from typing import Optional, List


class AddressModel(BaseModel):
    addr_string: Optional[str] | None = None
    city: Optional[str] | None = None
    country: Optional[str] | None = None
    zip: Optional[str] = Field(min_length=4, max_length=6, default=None)


class PhoneModel(BaseModel):
    model_config = {
        "str_strip_whitespace": "True",
        "coerce_numbers_to_string": "True",
    }
    phone: str = Field(min_length=6,
                       max_length=12,
                       pattern=r"^\d{6,12}$")

    def __hash__(self):
        return hash(self.phone)


class ContactModel(BaseModel):
    name: str
    email: Optional[EmailStr] | None = None
    birthdate: Optional[PastDate] | None = None
    phones: Optional[List[PhoneModel]] = []
    address: Optional[AddressModel] | None = None


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
