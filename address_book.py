import re
from typing import Optional, List
from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        self.value = value.strip().title()


class Phone(Field):
    REQUIRED_LENGTH = 10

    def __init__(self, phone):
        if not phone.isdigit():
            raise ValueError("Phone number must contain only digits")

        if len(phone) != Phone.REQUIRED_LENGTH:
            raise ValueError(
                f"The phone number must be {Phone.REQUIRED_LENGTH} digits long"
            )

        self.value = phone


class Email(Field):
    EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    def __init__(self, email: str):
        if not self.is_valid(email):
            raise ValueError(f"Invalid email address: {email}")
        self.value: str = email

    @classmethod
    def is_valid(cls, email: str) -> bool:
        """Перевірка email за допомогою regex"""
        return re.match(cls.EMAIL_REGEX, email) is not None


class Birthday(Field):
    DATE_FORMAT = "%d.%m.%Y"

    def __init__(self, date: str):
        try:
            birthday_date = datetime.strptime(date, Birthday.DATE_FORMAT)
            self.value = birthday_date.date()
        except ValueError as error:
            raise ValueError("Invalid date format. Use DD.MM.YYYY") from error

    def __str__(self):
        return self.value.strftime(Birthday.DATE_FORMAT)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.emails: list[Email] = []
        self.birthday: Optional[Birthday]  = None

    # ---------- PHONE ----------
    def add_phone(self, new_phone: str):
        if self._is_phone_exists(new_phone):
            raise ValueError(f"The phone number {new_phone} already exists")

        phone = Phone(new_phone)
        self.phones.append(phone)

    def remove_phone(self, phone_to_remove: str):
        phone = self.find_phone(phone_to_remove)
        if phone:
            self.phones.remove(phone)

    def edit_phone(self, old_phone: str, new_phone: str):
        phone = self.find_phone(old_phone)
        if phone:
            old_phone_index = self.phones.index(phone)
            self.phones[old_phone_index] = Phone(new_phone)

    def find_phone(self, phone: str) -> Phone | None:
        if not len(self.phones) > 0:
            raise ValueError("The phone list is empty")
        elif not self._is_phone_exists(phone):
            raise ValueError(f"Phone number {phone} not found")
        else:
            result = list(filter(lambda p: p.value == phone, self.phones))
            return result[0]

    def _is_phone_exists(self, phone):
        return any(p.value == phone for p in self.phones)


    # ---------- EMAIL ----------
    def add_email(self, new_email: str):
        email_obj = Email(new_email)
        if any(e.value == email_obj.value for e in self.emails):
            raise ValueError("Email already exists")
        self.emails.append(email_obj)

    def edit_email(self, old_email: str, new_email: str):
        email = next((e for e in self.emails if e.value == old_email), None)
        if not email:
            raise ValueError("Email not found")

        index = self.emails.index(email)
        self.emails[index] = Email(new_email)

    def delete_email(self, email_to_remove: str):
        email = next((e for e in self.emails if e.value == email_to_remove), None)
        if not email:
            raise ValueError("Email not found")
        self.emails.remove(email)


    # ---------- BIRTHDAY ----------
    def add_birthday(self, date: str):
        if self.birthday:
            raise ValueError("Birthday already exists!")

        self.birthday = Birthday(date)


    # ---------- STR ----------
    def __str__(self):
        phones = "; ".join(p.value for p in self.phones) if self.phones else "- empty"
        emails = "; ".join(e.value for e in self.emails) if self.emails else "- empty"
        birthday = str(self.birthday) if self.birthday else "- empty"
        return (
            f"Name: {self.name.value}, Phones: {phones}, "
            f"Emails: {emails}, Birthday: {birthday}"
        )


class AddressBook(UserDict):
    def add_record(self, new_record: Record):
        new_record_key = new_record.name.value.lower()
        self.data[new_record_key] = new_record

    def delete(self, record_name: str):
        record = self.find(record_name)
        if record:
            del self.data[record_name]

    def find(self, record_name: str) -> Record:
        return self.data.get(record_name.lower())

    def get_upcoming_birthdays(self):
        MAX_DAYS = 7
        current_date = datetime.today().date()
        max_date = current_date + timedelta(days=MAX_DAYS)
        records = list(self.data.values())

        upcoming_birthdays = []

        for record in records:
            name = record.name.value
            birthday = record.birthday.value
            bd_this_year = birthday.replace(year=current_date.year)
            bd_next_year = birthday.replace(year=current_date.year + 1)
            is_bd_next_year = bd_this_year < current_date
            upcoming_bd = bd_next_year if is_bd_next_year else bd_this_year

            is_bd_within_range = upcoming_bd >= current_date and upcoming_bd < max_date

            if is_bd_within_range:
                congratulation_date = upcoming_bd
                bd_weekday = upcoming_bd.weekday()
                weekend = [5, 6]
                is_bd_on_weekend = bd_weekday in weekend

                if is_bd_on_weekend:
                    additional_days_number = MAX_DAYS - bd_weekday
                    next_monday = upcoming_bd + timedelta(days=additional_days_number)
                    congratulation_date = next_monday

                congratulation_date_string = congratulation_date.strftime(
                    Birthday.DATE_FORMAT
                )
                upcoming_birthdays.append(
                    {"name": name, "congratulation_date": congratulation_date_string}
                )

        return upcoming_birthdays
