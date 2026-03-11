import questionary

from .handlers import (
    add_note,
    delete_note,
    edit_note_content,
    edit_note_title,
    show_all_notes,
    show_note,
)
from .notes_book import Notes

NOTES_MENU_CHOICES = [
    questionary.Choice("Add note", value="add-note"),
    questionary.Choice("Find note", value="find-note"),
    questionary.Choice("Edit title", value="edit-note-title"),
    questionary.Choice("Edit content", value="edit-note"),
    questionary.Choice("Delete note", value="delete-note"),
    questionary.Choice("All notes", value="all-notes"),
    questionary.Separator(),
    questionary.Choice("Back to main menu", value="back"),
]

HANDLERS = {
    "add-note": add_note,
    "find-note": show_note,
    "edit-note-title": edit_note_title,
    "edit-note": edit_note_content,
    "delete-note": delete_note,
    "all-notes": show_all_notes,
}


def run_notes_menu(notes: Notes) -> None:
    command = None
    while command != "back":
        command = questionary.select(
            "Notes menu:",
            choices=NOTES_MENU_CHOICES,
        ).ask()

        if command is None:
            break

        handler = HANDLERS.get(command)
        if handler:
            print(handler(notes))
