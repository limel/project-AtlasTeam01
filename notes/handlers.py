import questionary

from decorators import input_error

from .notes_book import Note, Notes
from helpers.command_helpers import ask_text, ask_title

@input_error
def add_note(notes: Notes) -> str:
    title = ask_text("Title: ")
    content = ask_text("Content: ")
    note = notes.add_note(Note(title=title, content=content))

    if note.title != title:
        return f"Note was successfully added as '{note.title}'"

    return "Note was successfully added"


@input_error
def show_note(notes: Notes) -> str:
    title = ask_title(notes, "Which note to show?")
    return str(notes.find_note(title))


@input_error
def edit_note_title(notes: Notes) -> str:
    title = ask_title(notes, "Which note to rename?")
    new_title = ask_text("New title: ")

    note = notes.edit_note_title(title, new_title)
    return f"Note title was successfully updated to '{note.title}'"


@input_error
def edit_note_content(notes: Notes) -> str:
    title = ask_title(notes, "Which note to edit?")
    note = notes.find_note(title)
    print(f"Current content: {note.content}")
    new_text = ask_text("New content: ")

    notes.edit_note(title, new_text)
    return "Note content was successfully updated"


@input_error
def delete_note(notes: Notes) -> str:
    title = ask_title(notes, "Which note to delete?")
    confirm = questionary.confirm(
        f"Are you sure you want to delete '{title}'?", default=False
    ).ask()

    if not confirm:
        return "Deletion cancelled"

    notes.delete_note(title)
    return "Note was successfully deleted"


def show_all_notes(notes: Notes) -> str:
    return str(notes)
