from decorators import input_error
from address_book import AddressBook, Record


def check_if_args_provided(args: list):
    if not len(args):
        raise ValueError("No arguments provided")


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
        return "Contact was successfully added"

    if phone:
        record.add_phone(phone)
        return "Contact was successfully updated"

    return "Contact already exists"


@input_error
def change_contact(args: list, book: AddressBook):
    check_if_args_provided(args)

    name, *rest = args
    old_phone = rest[0] if rest else None
    new_phone = rest[1] if rest and len(rest) == 2 else None

    if not old_phone or not new_phone:
        raise ValueError("Missing command arguments")

    book[name].edit_phone(old_phone, new_phone)
    return f"The phone number was successfully updated from {old_phone} to {new_phone}"


@input_error
def show_phone(args: list, book: AddressBook):
    check_if_args_provided(args)

    name, *_ = args
    record = book.find(name)
    return f"{record.name.value} - {', '.join(p.value for p in record.phones)}"


@input_error
def show_all(book: AddressBook):
    records = [str(r) for r in book.values()]
    return "\n".join(records)


@input_error
def add_birthday(args: list, book: AddressBook):
    check_if_args_provided(args)

    name, birthday = args
    book[name].add_birthday(birthday)
    return "Birthday has been successfully added"


@input_error
def show_birthday(args: list, book: AddressBook):
    name, *_ = args
    return book.find(name).birthday


@input_error
def birthdays(book: AddressBook):
    is_upcoming_bds_available = len(book.get_upcoming_birthdays()) > 0
    birthdays = [
        f"{birthday["name"]} - {birthday["congratulation_date"]}"
        for birthday in book.get_upcoming_birthdays()
    ]
    return (
        f"Upcoming birthdays:\n{'\n'.join(birthdays) if is_upcoming_bds_available else '- empty'}"
    )
