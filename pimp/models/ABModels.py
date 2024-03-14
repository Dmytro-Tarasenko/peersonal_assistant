from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    PastDate, PastDatetime,
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
    birthdate: Optional[PastDatetime] | None = None
    phones: Optional[List[PhoneModel]] = []
    address: Optional[AddressModel] | None = None


def update_model(model: BaseModel,
                 update_data: BaseModel) -> BaseModel:
    # TODO: option to consider nested models that will allow
    #       leave fields that are already set
    #       address=AddressModel(addr_string='Some street 123', city='New York', country='USA', zip='12345') =>
    #    => address=AddressModel(addr_string='New street 34', city='Chicago',country='USA', zip='12345') !=>
    #    !=> address=AddressModel(addr_string='New street 34', city='Chicago', country=None, zip=None)
    Model = model.__class__
    data = model.model_dump(warnings=False)
    new_model = Model(**data)
    new_data = update_data.model_dump(exclude_unset=True, warnings=False)
    updated_model = new_model.model_copy(update=new_data, deep=True)

    return Model(**updated_model.model_dump(warnings=False))


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

    print(contact)
    new_model = contact.__class__(**contact.model_dump())
    old_address = contact.address
    new_addr = AddressModel(addr_string="New street 34",
                            city="Chicago")
    contact = update_model(new_model, ContactModel(name=new_model.name, address=new_addr))
    # print(contact)
    #
    # print(old_address)
    # old_address = update_model(old_address, new_addr)
    # print(old_address)
    #
    # print(contact.model_json_schema())
