import questionary

from addressBook.address_book import AddressBook

from addressBook.handlers import (
    add_contact,
    birthdays,
    delete_contact,
    edit_contact,
    show_all,
)
from notes import Notes, run_notes_menu
from store.serializer import PickleSerializer

book_serializer = PickleSerializer("address_book", AddressBook)
notes_serializer = PickleSerializer("notes", Notes)

MAIN_MENU_CHOICES = [
    questionary.Choice("Add contact", value="add"),
    questionary.Choice("Edit contact", value="edit"),
    questionary.Choice("Delete contact", value="delete"),
    questionary.Choice("Show all contacts", value="all"),
    questionary.Choice("Upcoming birthdays", value="birthdays"),
    questionary.Choice("Notes", value="notes"),
    questionary.Separator(),
    questionary.Choice("Exit", value="exit"),
]

HANDLERS = {
    "add": add_contact,
    "edit": edit_contact,
    "delete": delete_contact,
    "all": show_all,
    "birthdays": birthdays,
}


def main() -> None:
    book = book_serializer.load_data()
    notes = notes_serializer.load_data()
    print("Welcome to the assistant bot!")

    while True:
        command = questionary.select(
            "Choose a command:",
            choices=MAIN_MENU_CHOICES,
        ).ask()

        if command is None or command == "exit":
            book_serializer.save_data(book)
            notes_serializer.save_data(notes)
            print("Good bye!")
            break

        if command == "notes":
            if notes is None:
                notes = Notes()
            run_notes_menu(notes)
            continue

        handler = HANDLERS.get(command)
        if handler:
            print(handler(book))


if __name__ == "__main__":
    main()
