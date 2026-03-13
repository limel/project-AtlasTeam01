# addressBook/handlers.py
import questionary
from tabulate import tabulate

from decorators import input_error

from .address_book import AddressBook
from .menu import run_edit_menu
from .record import Record
from helpers.command_helpers import ask_contact, ask_text

@input_error
def add_contact(book: AddressBook) -> str:
    name = ask_text("Contact name: ")
    phone = ask_text("Phone (or leave empty): ", required=False)

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
def delete_contact(book: AddressBook) -> str:
    record = ask_contact(book, "Which contact to delete?")
    name = record.name.value
    confirm = questionary.confirm(
        f"Are you sure you want to delete '{name}'?", default=False
    ).ask()
    if not confirm:
        return "Deletion cancelled"
    book.delete(name)
    return f"Contact {name} deleted"


@input_error
def edit_contact(book: AddressBook) -> str:
    record = ask_contact(book, "Which contact to edit?")
    return run_edit_menu(record)


@input_error
def show_all(book: AddressBook) -> str:
    if not book.data:
        return "No contacts yet"

    rows = []
    for record in book.values():
        phones = (
            "\n".join(p.value for p in record.phones) if record.phones else "- empty"
        )
        emails = (
            "\n".join(e.value for e in record.emails) if record.emails else "- empty"
        )
        birthday = str(record.birthday) if record.birthday else "- empty"
        address = record.address.value if record.address else "- empty"
        rows.append([record.name.value, phones, emails, birthday, address])

    return tabulate(
        rows,
        headers=["Name", "Phones", "Emails", "Birthday", "Address"],
        tablefmt="grid",
    )


@input_error
def birthdays(book: AddressBook) -> str:
    upcoming_birthdays = book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        return "No upcoming birthdays"
    return "\n".join(
        f"{bd['name']} - {bd['congratulation_date']}" for bd in upcoming_birthdays
    )
