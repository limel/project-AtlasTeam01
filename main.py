from book_serialization import load_data, save_data

from addressBook.handlers import (
    add_contact,
    change_contact,
    delete_contact,
    find_contact,
    show_phone,
    add_email,
    show_email,
    edit_email,
    delete_email,
    add_address,
    show_address,
    edit_address,
    show_all,
    add_birthday,
    show_birthday,
    birthdays
)
# from addressBook.address_book import AddressBook
import shlex
from decorators import input_error
from notes import Notes, run_notes_menu


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
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
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
            print(change_contact(args, book))

        elif command == "find":
            print(find_contact(args, book))

        elif command == "delete":
            print(delete_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

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

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

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
