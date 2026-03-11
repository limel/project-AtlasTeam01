import questionary

from decorators import input_error

from .notes_book import Note, Notes


def _ask_text(prompt: str, required: bool = True) -> str:
    value = questionary.text(prompt).ask()
    if value is None:
        raise KeyboardInterrupt
    value = value.strip()
    if required and not value:
        raise ValueError(f"{prompt.rstrip(': ')} cannot be empty")
    return value


def _get_note_titles(notes: Notes) -> list[str]:
    return [note.title for note in notes._notes.values()]


def _ask_title(notes: Notes, prompt: str = "Select note:") -> str:
    titles = _get_note_titles(notes)
    if not titles:
        raise ValueError("You have no notes yet")
    return questionary.select(prompt, choices=titles).ask()


@input_error
def add_note(notes: Notes) -> str:
    title = _ask_text("Title: ")
    content = _ask_text("Content: ")
    note = notes.add_note(Note(title=title, content=content))

    if note.title != title:
        return f"Note was successfully added as '{note.title}'"

    return "Note was successfully added"


@input_error
def show_note(notes: Notes) -> str:
    title = _ask_title(notes, "Which note to show?")
    return str(notes.find_note(title))


@input_error
def edit_note_title(notes: Notes) -> str:
    title = _ask_title(notes, "Which note to rename?")
    new_title = _ask_text("New title: ")

    note = notes.edit_note_title(title, new_title)
    return f"Note title was successfully updated to '{note.title}'"


@input_error
def edit_note_content(notes: Notes) -> str:
    title = _ask_title(notes, "Which note to edit?")
    note = notes.find_note(title)
    print(f"Current content: {note.content}")
    new_text = _ask_text("New content: ")

    notes.edit_note(title, new_text)
    return "Note content was successfully updated"


@input_error
def delete_note(notes: Notes) -> str:
    title = _ask_title(notes, "Which note to delete?")
    confirm = questionary.confirm(
        f"Are you sure you want to delete '{title}'?", default=False
    ).ask()

    if not confirm:
        return "Deletion cancelled"

    notes.delete_note(title)
    return "Note was successfully deleted"


def show_all_notes(notes: Notes) -> str:
    return str(notes)
