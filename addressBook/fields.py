# addressBook/fields.py
import re
from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass
    # def __init__(self, value):
    #     self.value = value.strip().title()


class Phone(Field):
    REQUIRED_LENGTH = 10

    def __init__(self, phone):
        if not phone.isdigit():
            raise ValueError("Phone number must contain only digits")
        if len(phone) != Phone.REQUIRED_LENGTH:
            raise ValueError(f"Phone number must be {Phone.REQUIRED_LENGTH} digits long")
        self.value = phone


class Email(Field):
    EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    def __init__(self, email: str):
        if not self.is_valid(email):
            raise ValueError(f"Invalid email address: {email}")
        self.value = email

    @classmethod
    def is_valid(cls, email: str) -> bool:
        return re.match(cls.EMAIL_REGEX, email) is not None

class Address(Field):
    pass

class Birthday(Field):
    DATE_FORMAT = "%d.%m.%Y"

    def __init__(self, date: str):
        try:
            self.value = datetime.strptime(date, Birthday.DATE_FORMAT).date()
        except ValueError as e:
            raise ValueError("Invalid date format. Use DD.MM.YYYY") from e

    def __str__(self):
        return self.value.strftime(Birthday.DATE_FORMAT)
