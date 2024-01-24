from src.cls.AddressBook_pd import Birthday
from datetime import datetime

bd = Birthday(datetime.strptime("21-11-1978", "%d-%m-%Y"))

assert bd.local_str == "21-11-1978"
assert bd.date == datetime.strptime("21-11-1978", "%d-%m-%Y")
