import questionary

from book_serialization import load_data, save_data
from command_handlers import (
    add_birthday,
    add_contact,
    birthdays,
    change_contact,
    show_all,
    show_birthday,
    show_phone,
)
from notes import Notes, run_notes_menu

MAIN_MENU_CHOICES = [
    questionary.Choice("Hello", value="hello"),
    questionary.Choice("Add contact", value="add"),
    questionary.Choice("Change phone", value="change"),
    questionary.Choice("Show phone", value="phone"),
    questionary.Choice("Show all contacts", value="all"),
    questionary.Choice("Add birthday", value="add-birthday"),
    questionary.Choice("Show birthday", value="show-birthday"),
    questionary.Choice("Upcoming birthdays", value="birthdays"),
    questionary.Choice("Notes", value="notes"),
    questionary.Separator(),
    questionary.Choice("Exit", value="exit"),
]


def ask_text(prompt: str) -> str:
    value = questionary.text(prompt).ask()
    if value is None:
        raise KeyboardInterrupt
    return value.strip()


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

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            name = ask_text("Contact name: ")
            phone = ask_text("Phone (or leave empty): ")
            args = [name, phone] if phone else [name]
            print(add_contact(args, book))

        elif command == "change":
            name = ask_text("Contact name: ")
            old_phone = ask_text("Old phone: ")
            new_phone = ask_text("New phone: ")
            print(change_contact([name, old_phone, new_phone], book))

        elif command == "phone":
            name = ask_text("Contact name: ")
            print(show_phone([name], book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            name = ask_text("Contact name: ")
            birthday = ask_text("Birthday (DD.MM.YYYY): ")
            print(add_birthday([name, birthday], book))

        elif command == "show-birthday":
            name = ask_text("Contact name: ")
            print(show_birthday([name], book))

        elif command == "birthdays":
            print(birthdays(book))

        elif command == "notes":
            if notes is None:
                notes = Notes()
            run_notes_menu(notes)


if __name__ == "__main__":
    main()
