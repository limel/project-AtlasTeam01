# addressBook/handlers.py
from decorators import input_error

from .record import Record
from .address_book import AddressBook
from .fields import Phone, Email, Birthday

# --- Внутрішні допоміжні функції ---
def check_if_args_provided(args: list):
    if not args:
        raise ValueError("No arguments provided")


def get_record_or_error(name: str, book: AddressBook) -> Record:
    record = book.find(name)
    if record is None:
        raise ValueError(f"Contact {name} not found")
    return record


# --- CONTACT HANDLERS ---
@input_error
def add_contact(args: list, book: AddressBook):
    check_if_args_provided(args)
    name, *rest = args
    phone = rest[0] if rest else None

    record = book.find(name)
    if record is None:
        record = Record(name)
        if phone:
            record.add_phone(phone)
        book.add_record(record)
        return f"Contact {name} was successfully added"

    if phone:
        record.add_phone(phone)
        return f"Contact {name} updated with new phone"

    return "Contact already exists"

@input_error
def edit_contact(args: list, book: AddressBook):
    check_if_args_provided(args)
    name, *rest = args
    old_phone = rest[0] if rest else None
    new_phone = rest[1] if rest and len(rest) == 2 else None

    if not old_phone or not new_phone:
        raise ValueError("Missing command arguments")

    record = get_record_or_error(name, book)
    record.edit_phone(old_phone, new_phone)
    return f"The phone number was successfully updated from {old_phone} to {new_phone}"

@input_error
def find_contact(args: list, book: AddressBook):
    check_if_args_provided(args)
    name, *_ = args
    record = get_record_or_error(name, book)
    return str(record)

@input_error
def delete_contact(args: list, book: AddressBook):
    check_if_args_provided(args)
    name, *_ = args
    record = get_record_or_error(name, book)
    book.delete(record.name.value)
    return f"Contact {name} deleted"


# --- PHONE HANDLERS ---
@input_error
def show_phone(args: list, book: AddressBook):
    check_if_args_provided(args)
    name, *_ = args
    record = get_record_or_error(name, book)
    if not record.phones:
        return f"{record.name.value} - No phone numbers yet"
    return f"{record.name.value} - {', '.join(p.value for p in record.phones)}"

@input_error
def delete_phone(args: list, book: AddressBook):
    check_if_args_provided(args)
    if len(args) != 2:
        raise ValueError("Provide: name phone_to_delete")
    name, phone_to_delete = args
    record = get_record_or_error(name, book)
    record.delete_phone(phone_to_delete)
    return f"Phone {phone_to_delete} removed from contact {name}"


# --- EMAIL HANDLERS ---
@input_error
def add_email(args: list, book: AddressBook):
    check_if_args_provided(args)
    name, email = args
    record = get_record_or_error(name, book)
    record.add_email(email)
    return f"Email {email} added to contact {name}"

@input_error
def edit_email(args: list[str], book: AddressBook):
    check_if_args_provided(args)
    if len(args) != 3:
        raise ValueError("Provide: name old_email new_email")
    name, old_email, new_email = args
    record = get_record_or_error(name, book)
    record.edit_email(old_email, new_email)
    return f"Email updated from {old_email} to {new_email}"

@input_error
def show_email(args: list, book: AddressBook):
    check_if_args_provided(args)
    name, *_ = args
    record = get_record_or_error(name, book)
    if not record.emails:
        return "No emails found"
    return f"{record.name.value} - {', '.join(e.value for e in record.emails)}"

@input_error
def delete_email(args: list[str], book: AddressBook):
    check_if_args_provided(args)
    if len(args) != 2:
        raise ValueError("Provide: name email")
    name, email = args
    record = get_record_or_error(name, book)
    record.delete_email(email)
    return f"Email {email} removed from contact {name}"


# --- ADDRESS HANDLERS ---
@input_error
def add_address(args: list, book: AddressBook):
    check_if_args_provided(args)
    name, address = args
    record = get_record_or_error(name, book)

    if record.address is not None:
        return f"Address already exists for contact {name}"

    record.add_address(address)
    return f"Address '{address}' added to contact {name}"

@input_error
def edit_address(args: list, book: AddressBook):
    check_if_args_provided(args)
    if len(args) != 2:
        raise ValueError("Provide: name new_address")
    name, new_address = args
    record = get_record_or_error(name, book)
    record.add_address(new_address)
    return f"Address for {name} updated to '{new_address}'"

@input_error
def show_address(args: list, book: AddressBook):
    check_if_args_provided(args)
    name, *_ = args
    record = get_record_or_error(name, book)
    if not record.address:
        return f"{name} - Address not set"
    return f"{name} - {record.address.value}"

@input_error
def delete_address(args: list, book: AddressBook):
    check_if_args_provided(args)
    name, *_ = args
    record = get_record_or_error(name, book)
    record.delete_address()
    return f"Address for {name} deleted"


# --- BIRTHDAY HANDLERS ---
@input_error
def add_birthday(args: list, book: AddressBook):
    check_if_args_provided(args)
    name, birthday = args
    record = get_record_or_error(name, book)


    if record.birthday is not None:
        return f"Birthday already exists for contact {name}"

    record.add_birthday(birthday)
    return "Birthday has been successfully added"

@input_error
def edit_birthday(args: list, book: AddressBook):
    check_if_args_provided(args)
    if len(args) != 2:
        raise ValueError("Provide: name new_birthday")
    name, new_birthday = args
    record = get_record_or_error(name, book)
    record.add_birthday(new_birthday)
    return f"Birthday for {name} updated to {new_birthday}"

@input_error
def show_birthday(args: list, book: AddressBook):
    name, *_ = args
    record = get_record_or_error(name, book)
    if not record.birthday:
        return f"{name} - Birthday not set"
    return str(record.birthday)

@input_error
def delete_birthday(args: list, book: AddressBook):
    check_if_args_provided(args)
    name, *_ = args
    record = get_record_or_error(name, book)
    if not record.birthday:
        return f"{name} - Birthday not set"
    record.delete_birthday()
    return f"Birthday removed for contact {name}"

# --- GENERAL HANDLERS ---
@input_error
def show_all(book: AddressBook):
    records = [str(r) for r in book.values()]
    return "\n".join(records)

@input_error
def birthdays(book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        return "- empty"
    return "\n".join(f"{bd['name']} - {bd['congratulation_date']}" for bd in upcoming_birthdays)