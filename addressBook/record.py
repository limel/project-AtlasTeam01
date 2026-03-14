# addressBook/record.py
from .fields import Address, Birthday, Email, Name, Phone


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.emails: list[Email] = []
        self.address: Address | None = None
        self.birthday: Birthday | None = None

    # ---------- PHONE ----------
    def add_phone(self, new_phone: str):
        if any(p.value == new_phone for p in self.phones):
            raise ValueError(f"The phone number {new_phone} already exists")
        self.phones.append(Phone(new_phone))

    def edit_phone(self, old_phone: str, new_phone: str):
        phone = next((p for p in self.phones if p.value == old_phone), None)
        if not phone:
            raise ValueError(f"Phone {old_phone} not found")
        self.phones[self.phones.index(phone)] = Phone(new_phone)

    def delete_phone(self, phone_to_remove: str):
        phone = next((p for p in self.phones if p.value == phone_to_remove), None)
        if not phone:
            raise ValueError(f"Phone {phone_to_remove} not found")
        self.phones.remove(phone)

    # ---------- EMAIL ----------
    def add_email(self, new_email: str):
        if any(e.value == new_email for e in self.emails):
            raise ValueError("Email already exists")
        self.emails.append(Email(new_email))

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

    # ---------- ADDRESS ----------
    def add_address(self, address: str):
        self.address = Address(address)

    def delete_address(self):
        if not self.address:
            raise ValueError("Address not set")
        self.address = None

    # ---------- BIRTHDAY ----------
    def add_birthday(self, date: str):
        self.birthday = Birthday(date)

    def delete_birthday(self):
        if not self.birthday:
            raise ValueError("Birthday not set")
        self.birthday = None

    # ---------- STR for Record ----------
    def __str__(self):
        phones = ", ".join(p.value for p in self.phones) if self.phones else "- empty"
        emails = ", ".join(e.value for e in self.emails) if self.emails else "- empty"
        birthday = str(self.birthday) if self.birthday else "- empty"
        address = self.address.value if self.address else "- empty"
        return (
            f"Name: {self.name.value}\n"
            f"Phones: {phones}\n"
            f"Emails: {emails}\n"
            f"Birthday: {birthday}\n"
            f"Address: {address}"
        )
