from address_book import AddressBook, Record
from decorators import input_error


def check_if_args_provided(args: list):
    if not len(args):
        raise ValueError("No arguments provided")

def get_record_or_error(name: str, book: AddressBook) -> Record:
    record = book.find(name)

    if record is None:
        raise ValueError("Contact not found")

    return record

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
        return f"Contact to {name} was successfully updated"

    return f"Contact already exists"


@input_error
def change_contact(args: list, book: AddressBook):
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

@input_error
def show_phone(args: list, book: AddressBook):
    check_if_args_provided(args)

    name, *_ = args
    record = get_record_or_error(name, book)

    if not record.phones:
        return f"{record.name.value} - No phone numbers yet"

    return f"{record.name.value} - {', '.join(p.value for p in record.phones)}"

@input_error
def add_email(args: list, book: AddressBook):
    check_if_args_provided(args)

    name, email = args
    record = get_record_or_error(name, book)
    record.add_email(email)

    return f"Email {email} added to contact {name}"

@input_error
def show_email(args: list, book: AddressBook):
    check_if_args_provided(args)

    name, *_ = args
    record = get_record_or_error(name, book)

    if not record.emails:
        return "No emails found"

    return f"{record.name.value} - {', '.join(e.value for e in record.emails)}"

@input_error
def edit_email(args: list[str], book: AddressBook) -> str:
    check_if_args_provided(args)

    if len(args) != 3:
        raise ValueError("Provide: name old_email new_email")

    name, old_email, new_email = args

    record = get_record_or_error(name, book)

    record.edit_email(old_email, new_email)

    return f"Email updated from {old_email} to {new_email}"

@input_error
def delete_email(args: list[str], book: AddressBook) -> str:
    check_if_args_provided(args)

    if len(args) != 2:
        raise ValueError("Provide: name email")

    name, email = args

    record = get_record_or_error(name, book)

    record.delete_email(email)

    return f"Email {email} removed from contact {name}"

@input_error
def show_all(book: AddressBook):
    records = [str(r) for r in book.values()]
    return "\n".join(records)


@input_error
def add_birthday(args: list, book: AddressBook):
    check_if_args_provided(args)

    name, birthday = args
    record = get_record_or_error(name, book)
    record.add_birthday(birthday)
    return "Birthday has been successfully added"


@input_error
def show_birthday(args: list, book: AddressBook):
    name, *_ = args
    record = get_record_or_error(name, book)
    return record.birthday


@input_error
def birthdays(book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays()
    birthdays = [
        f"{birthday['name']} - {birthday['congratulation_date']}"
        for birthday in upcoming_birthdays
    ]
    birthday_list = "\n".join(birthdays) if birthdays else "- empty"
    return f"Upcoming birthdays:\n{birthday_list}"
