import questionary

from .handlers import (
    add_note,
    add_tag_to_note,
    delete_note,
    edit_note_content,
    edit_note_title,
    get_notes_sorted_by_tag,
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
    questionary.Choice("Get notes sorted by tag", value="get-notes-sorted-by-tag"),
    questionary.Choice("Add tag to note", value="add-tag-to-note"),
    questionary.Choice("All notes", value="all-notes"),
    questionary.Separator(),
    questionary.Choice("Back to main menu", value="back"),
]

HANDLERS = {
    "add-note": add_note,
    "find-note": show_note,
    "get-notes-sorted-by-tag": get_notes_sorted_by_tag,
    "add-tag-to-note": add_tag_to_note,
    "edit-note-title": edit_note_title,
    "edit-note": edit_note_content,
    "delete-note": delete_note,
    "all-notes": show_all_notes,
}


NOTES_INSTRUCTIONS = """
Available commands:
  Add note            - Create a new note
  Find note           - Search for a note by title
  Edit title          - Rename a note
  Edit content        - Change note content
  Delete note         - Remove a note
  Add tag to note     - Add tags to an existing note
  Sort by tag         - Find notes by tags
  All notes           - Show all notes
"""


def run_notes_menu(notes: Notes) -> None:
    print(NOTES_INSTRUCTIONS)
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
