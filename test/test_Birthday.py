from pydantic import ValidationError

from src.cls.AddressBook_pd import Birthday
from datetime import datetime, timedelta
import pytest


bd = Birthday(date=datetime.strptime("21-11-1978", "%d-%m-%Y"))

assert bd.local_str == "21-11-1978"

assert bd.date == datetime.strptime("21-11-1978", "%d-%m-%Y").date()

with pytest.raises(ValidationError, match="Date should be in the past"):
    Birthday(date=datetime.today().date())

with pytest.raises(ValidationError, match="Input should be a valid date or datetime"):
    bd.date = "12-11-2978"