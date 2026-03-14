# addressBook/fields.py
from datetime import datetime

import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from email_validator import validate_email, EmailNotValidError

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    DEFAULT_COUNTRY = "UA"

    def __init__(self, phone: str):
        phone = phone.strip().replace(" ", "").replace("-", "")
        if not phone.startswith("+"):
            if len(phone) == 9:  # мобільний без коду (наприклад, 673000888)
                phone = "+380" + phone

        try:
            parsed = phonenumbers.parse(phone, self.DEFAULT_COUNTRY)
        except NumberParseException:
            raise ValueError(f"Invalid phone number: {phone}")

        if not phonenumbers.is_valid_number_for_region(parsed, self.DEFAULT_COUNTRY):
            raise ValueError(f"Phone number is not valid for Ukraine: {phone}")
        self.value = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)

class Email(Field):
    def __init__(self, email: str):
        try:
            v = validate_email(email, check_deliverability=False)
            self.value = v.email
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email address: {email}") from e


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

        today = datetime.now().date()
        age = today.year - parsed_date.year - (
                (today.month, today.day) < (parsed_date.month, parsed_date.day)
        )

        if parsed_date > today:
            raise ValueError("Oops! Birthday cannot be later than today")

        if parsed_date.year < Birthday.MIN_YEAR:
            raise ValueError(f"Year must be after {Birthday.MIN_YEAR}")

        if age > Birthday.MAX_AGE:
            raise ValueError("Birthday year is unrealistic")

        self.value = parsed_date

    def __str__(self):
        return self.value.strftime(Birthday.DATE_FORMAT)

