import shlex

from colorama import Fore, Style, init
from addressBook.address_book import AddressBook
from addressBook.handlers import (
    add_address,
    add_birthday,
    add_contact,
    add_email,
    birthdays,
    delete_address,
    delete_birthday,
    delete_contact,
    delete_email,
    delete_phone,
    edit_address,
    edit_birthday,
    edit_contact,
    edit_email,
    find_contact,
    show_address,
    show_all,
    show_birthday,
    show_email,
    show_phone,
)
from decorators import input_error
from notes import Notes, run_notes_menu
from store.serializer import PickleSerializer

serializer = PickleSerializer("book", AddressBook)

init(autoreset=True)


@input_error
def parse_input(user_input: str):
    parts = shlex.split(user_input)
    if not parts:
        return ("",)

    command, *args = parts
    command = command.strip().lower()

    if args:
        args[0] = args[0].strip().title()
    return command, *args


def main() -> None:
    book = serializer.load_data()
    notes: Notes | None = None

    print(Fore.CYAN + Style.BRIGHT + "Welcome to the assistant bot!")
    print(
        Fore.YELLOW
        + "Commands: add, change, find, delete, phone, add-email, add-address,\n"
        + "add-birthday, birthdays, all, notes, exit"
    )

    while True:
        user_input = input(
            Fore.GREEN + Style.BRIGHT + "Enter a command: " + Style.RESET_ALL
        )

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            serializer.save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(edit_contact(args, book))

        elif command == "find":
            print(find_contact(args, book))

        elif command == "delete":
            print(delete_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "delete-phone":
            print(delete_phone(args, book))

        elif command == "add-email":
            print(add_email(args, book))

        elif command == "email":
            print(show_email(args, book))

        elif command == "edit-email":
            print(edit_email(args, book))

        elif command == "delete-email":
            print(delete_email(args, book))

        elif command == "add-address":
            print(add_address(args, book))

        elif command == "show-address":
            print(show_address(args, book))

        elif command == "edit-address":
            print(edit_address(args, book))

        elif command == "delete-address":
            print(delete_address(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "edit-birthday":
            print(edit_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "delete-birthday":
            print(delete_birthday(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "birthdays":
            print(birthdays(book))

        # TODO: add correct command in integration task
        elif command == "notes":
            if notes is None:
                notes = Notes()

            run_notes_menu(notes)

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
