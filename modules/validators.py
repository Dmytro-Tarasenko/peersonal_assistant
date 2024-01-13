from textual.validation import Validator, ValidationResult
from datetime import datetime
import re


class NameValidator(Validator):
    """
            Перевіряє коректність введеного імені.

            Параметри:
            - value (str): Введене значення для перевірки.

            Повертає:
            - ValidationResult: Результат перевірки.
            """
    def validate(self, value: str) -> ValidationResult:
        if value.isalpha() and value[0].isupper() and len(value) > 1:
            return self.success()
        else:
            return self.failure("Invalid name. Please enter a valid name starting with an uppercase letter"
                                " and containing only alphabetical characters.")


class PhoneNumberValidator(Validator):
    """
            Перевіряє коректність введеного номера телефону.

            Параметри:
            - value (str): Введене значення для перевірки.

            Повертає:
            - ValidationResult: Результат перевірки.
            """
    def validate(self, value: str) -> ValidationResult:
        if value.isdigit() and len(value) == 10:
            return self.success()
        else:
            return self.failure("Invalid phone number. Please enter 10 digits.")


class BirthdayValidator(Validator):
    """
           Перевіряє коректність введеної дати народження.

           Параметри:
           - value (str): Введене значення для перевірки.

           Повертає:
           - ValidationResult: Результат перевірки.
           """
    def validate(self, value: str) -> ValidationResult:
        if len(value) == 10:
            try:
                datetime.strptime(value, '%d-%m-%Y')
                return self.success()
            except ValueError:
                return self.failure('Invalid birthday format. Please use DD-MM-YYYY.')
        else:
            return self.failure('Invalid birthday format. Please use DD-MM-YYYY.')


class EmailValidator(Validator):
    """
            Перевіряє коректність введеної електронної адреси.

            Параметри:
            - value (str): Введене значення для перевірки.

            Повертає:
            - ValidationResult: Результат перевірки.
            """
    def validate(self, value: str) -> ValidationResult:
        pattern = r"^[a-zA-Z0-9.]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$"
        if re.match(pattern, value):
            return self.success()
        else:
            return self.failure("Invalid email address. Use Exa.mple123@email.com format")
