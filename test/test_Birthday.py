from pydantic import ValidationError

from pimp.cls.AddressBook import Birthday
from datetime import datetime, timedelta
import pytest


bd = Birthday(date=datetime.strptime("11-21-1978", "%m-%d-%Y"))

assert bd.local_str == "21-11-1978"

assert bd.date == datetime.strptime("11-21-1978", "%m-%d-%Y").date()

with pytest.raises(ValidationError, match="Date should be in the past"):
    Birthday(date=datetime.today().date())

with pytest.raises(ValidationError, match="Input should be a valid date or datetime"):
    bd.date = "12-11-2978"

today_check = datetime.today().date() + timedelta(days=350)
bd = Birthday(date=datetime(day=today_check.day,
                            month=today_check.month,
                            year=today_check.year-39))

assert bd.days_to_birthday == 350
