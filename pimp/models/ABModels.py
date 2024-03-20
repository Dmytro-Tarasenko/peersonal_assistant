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
