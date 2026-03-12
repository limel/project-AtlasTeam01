from book_serialization import load_data, save_data
from colorama import Fore, Style, init

from addressBook.handlers import (
    add_contact,
    edit_contact,
    find_contact,
    delete_contact,
    show_phone,
    delete_phone,
    add_email,
    edit_email,
    show_email,
    delete_email,
    add_address,
    edit_address,
    show_address,
    delete_address,
    add_birthday,
    edit_birthday,
    show_birthday,
    delete_birthday,
    show_all,
    birthdays
)
import shlex
from decorators import input_error
from notes import Notes, run_notes_menu

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
    book = load_data()
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
            save_data(book)
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
