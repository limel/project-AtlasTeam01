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


class Phone(Field):
    PHONE_NUMBER_REGEX = r"^\+?\d[\d\s-]{8,14}\d$"

    @staticmethod
    def normalize(phone: str) -> str:
        """Return a normalized phone number with spaces and hyphens removed."""
        return re.sub(r"[\s-]", "", phone)

    def __init__(self, phone: str):
        if not re.match(Phone.PHONE_NUMBER_REGEX, phone):
            raise ValueError("Invalid phone number format")
        normalized_phone = Phone.normalize(phone)
        super().__init__(normalized_phone)


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
    MIN_YEAR = 1900
    MAX_AGE = 120

    def __init__(self, date: str):
        try:
            parsed_date = datetime.strptime(date, Birthday.DATE_FORMAT).date()
        except ValueError as e:
            raise ValueError(
                "Invalid birthday. Use format DD.MM.YYYY and valid calendar date"
            ) from e

        current_year = datetime.now().year
        age = current_year - parsed_date.year

        if parsed_date.year > current_year:
            raise ValueError("Birthday cannot be in the future")

        if parsed_date.year < Birthday.MIN_YEAR:
            raise ValueError(f"Year must be after {Birthday.MIN_YEAR}")

        if age > Birthday.MAX_AGE:
            raise ValueError("Birthday year is unrealistic")

        self.value = parsed_date

    def __str__(self):
        return self.value.strftime(Birthday.DATE_FORMAT)
