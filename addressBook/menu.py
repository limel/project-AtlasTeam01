# addressBook/menu.py
import questionary

from decorators import input_error

from helpers.command_helpers import ask_select, ask_text
from .record import Record

EDIT_MENU_CHOICES = [
    questionary.Choice("Add phone", value="add-phone"),
    questionary.Choice("Change phone", value="change-phone"),
    questionary.Choice("Delete phone", value="delete-phone"),
    questionary.Choice("Add email", value="add-email"),
    questionary.Choice("Edit email", value="edit-email"),
    questionary.Choice("Delete email", value="delete-email"),
    questionary.Choice("Set address", value="set-address"),
    questionary.Choice("Delete address", value="delete-address"),
    questionary.Choice("Set birthday", value="set-birthday"),
    questionary.Choice("Delete birthday", value="delete-birthday"),
    questionary.Separator(),
    questionary.Choice("Back", value="back"),
]

# --- Edit sub-handlers ---


def _handle_add_phone(record: Record) -> str:
    phone = ask_text("Phone: ")
    record.add_phone(phone)
    return f"Phone {phone} added"


def _handle_change_phone(record: Record) -> str:
    phones = [p.value for p in record.phones]
    old = ask_select(phones, "Which phone to change?", "No phone numbers to change")
    new = ask_text("New phone: ", default=old)
    record.edit_phone(old, new)
    return f"Phone updated from {old} to {new}"


def _handle_delete_phone(record: Record) -> str:
    phones = [p.value for p in record.phones]
    phone = ask_select(phones, "Which phone to delete?", "No phone numbers to delete")
    record.delete_phone(phone)
    return f"Phone {phone} removed"


def _handle_add_email(record: Record) -> str:
    email = ask_text("Email: ")
    record.add_email(email)
    return f"Email {email} added"


def _handle_edit_email(record: Record) -> str:
    emails = [e.value for e in record.emails]
    old = ask_select(emails, "Which email to edit?", "No emails to edit")
    new = ask_text("New email: ", default=old)
    record.edit_email(old, new)
    return f"Email updated from {old} to {new}"


def _handle_delete_email(record: Record) -> str:
    emails = [e.value for e in record.emails]
    email = ask_select(emails, "Which email to delete?", "No emails to delete")
    record.delete_email(email)
    return f"Email {email} removed"


def _handle_set_address(record: Record) -> str:
    current = record.address.value if record.address else ""
    address = ask_text("Address: ", default=current)
    record.add_address(address)
    return f"Address set to '{address}'"


def _handle_delete_address(record: Record) -> str:
    record.delete_address()
    return "Address deleted"


def _handle_set_birthday(record: Record) -> str:
    current = str(record.birthday) if record.birthday else ""
    birthday = ask_text("Birthday (DD.MM.YYYY): ", default=current)
    record.add_birthday(birthday)
    return f"Birthday set to {birthday}"


def _handle_delete_birthday(record: Record) -> str:
    record.delete_birthday()
    return "Birthday deleted"


EDIT_HANDLERS = {
    "add-phone": _handle_add_phone,
    "change-phone": _handle_change_phone,
    "delete-phone": _handle_delete_phone,
    "add-email": _handle_add_email,
    "edit-email": _handle_edit_email,
    "delete-email": _handle_delete_email,
    "set-address": _handle_set_address,
    "delete-address": _handle_delete_address,
    "set-birthday": _handle_set_birthday,
    "delete-birthday": _handle_delete_birthday,
}


@input_error
def run_edit_menu(record: Record) -> str:
    print(f"\n{record}\n")

    command = questionary.select(
        f"Edit {record.name.value}:",
        choices=EDIT_MENU_CHOICES,
    ).ask()

    if command is None or command == "back":
        return "Back to main menu"

    handler = EDIT_HANDLERS.get(command)
    if handler:
        return handler(record)
    return "Unknown command"
