# addressBook/handlers.py
import questionary
from tabulate import tabulate

from decorators import input_error
from helpers.command_helpers import ask_contact, ask_text

from .address_book import AddressBook
from .fields import Phone
from .menu import run_edit_menu
from .record import Record
from .utils import match_record, record_to_row


@input_error
def add_contact(book: AddressBook) -> str:
    name = ask_text("Contact name: ")
    phone = ask_text("Phone (or leave empty): ", required=False, validator=Phone)

    record = Record(name)
    if phone:
        record.add_phone(phone)
    book.add_record(record)
    return f"Contact {name} was successfully added"


@input_error
def delete_contact(book: AddressBook) -> str:
    record = ask_contact(book, "Which contact to delete?")
    if record is None:
        return "Deletion cancelled"
    name = record.name.value
    confirm = questionary.confirm(
        f"Are you sure you want to delete '{name}'?", default=False
    ).ask()
    if not confirm:
        return "Deletion cancelled"
    book.delete(str(record._id))
    return f"Contact {name} deleted"


@input_error
def edit_contact(book: AddressBook) -> str:
    record = ask_contact(book, "Which contact to edit?")
    if record is None:
        return "Edit cancelled"
    return run_edit_menu(record)


@input_error
def search_contacts(book: AddressBook) -> str:
    field = questionary.select(
        "Filter by:",
        choices=[
            questionary.Choice("Name", value="name"),
            questionary.Choice("Phone", value="phone"),
            questionary.Choice("Email", value="email"),
            questionary.Choice("Address", value="address"),
            questionary.Choice("Birthday", value="birthday"),
        ],
    ).ask()

    if field is None:
        return "Search cancelled"

    pattern = ask_text("Enter search value (partial OK): ").lower()
    if not pattern:
        return "Empty search, cancelled"

    matched = [r for r in book.values() if match_record(r, field, pattern)]

    if not matched:
        return "No contacts found"

    rows = [record_to_row(r) for r in matched]

    return tabulate(
        rows,
        headers=["Name", "Phones", "Emails", "Birthday", "Address"],
        tablefmt="grid",
    )


@input_error
def show_all(book: AddressBook) -> str:
    if not book.data:
        return "No contacts yet"

    rows = [record_to_row(r) for r in book.values()]

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
