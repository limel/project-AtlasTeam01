import shlex

from colorama import Fore, Style, init

from .handlers import (
    add_note,
    delete_note,
    edit_note_content,
    edit_note_title,
    show_all_notes,
    show_note,
)
from .notes_book import Notes

init(autoreset=True)


def parse_notes_input(user_input: str) -> tuple[str, ...]:
    """
    Splits user input into command and arguments.
    Returns (command, *args). For empty input returns ("",).
    """

    parts = shlex.split(user_input)
    if not parts:
        return ("",)

    command, *args = parts
    command = command.strip().lower()
    return command, *args


def run_notes_menu(notes: Notes) -> None:
    print(Fore.CYAN + Style.BRIGHT + "Welcome to the Notes menu!")
    # TODO: add exit instruction in integration task
    print(
        Fore.YELLOW
        + "Commands: add-note, find-note, edit-note-title, "
        + "edit-note, delete-note, all-notes"
    )

    while True:
        user_input = input(
            Fore.GREEN + Style.BRIGHT + "Notes command: " + Style.RESET_ALL
        )
        try:
            command, *args = parse_notes_input(user_input)
        except ValueError:
            print("Invalid notes command. Check paired quotes in the title.")
            continue

        if not command:
            print("Enter a notes command.")
            continue

        # TODO: check "back" command in integration task
        if command in ("back", "exit", "close"):
            print("Exiting Notes menu.")
            break

        if command == "add-note":
            print(add_note(args, notes))
        elif command == "find-note":
            print(show_note(args, notes))
        elif command == "edit-note-title":
            print(edit_note_title(args, notes))
        elif command == "edit-note":
            print(edit_note_content(args, notes))
        elif command == "delete-note":
            print(delete_note(args, notes))
        elif command == "all-notes":
            print(show_all_notes(notes))
        else:
            print("Invalid notes command.")
