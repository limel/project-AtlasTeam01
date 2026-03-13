import questionary

from addressBook.handlers import (
    add_contact,
    birthdays,
    delete_contact,
    edit_contact,
    show_all,
)
from book_serialization import load_data, save_data
from notes import Notes, run_notes_menu

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
    book = load_data()
    notes: Notes | None = None
    print("Welcome to the assistant bot!")

    while True:
        command = questionary.select(
            "Choose a command:",
            choices=MAIN_MENU_CHOICES,
        ).ask()

        if command is None or command == "exit":
            save_data(book)
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
