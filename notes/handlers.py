from decorators import input_error

from .notes_book import Note, Notes


def require_args(args: list[str], count: int) -> None:
    if len(args) < count:
        raise ValueError("Not enough arguments provided")


@input_error
def add_note(args: list[str], notes: Notes) -> str:
    require_args(args, 2)

    title = args[0]
    content = " ".join(args[1:])
    note = notes.add_note(Note(title=title, content=content))

    # Duplicate titles are suffixed as "title_1", "title_2", and so on.
    if note.title != title:
        return f"Note was successfully added as '{note.title}'"

    return "Note was successfully added"


@input_error
def show_note(args: list[str], notes: Notes) -> str:
    require_args(args, 1)

    title = args[0]
    return str(notes.find_note(title))


@input_error
def edit_note(args: list[str], notes: Notes) -> str:
    require_args(args, 2)

    title = args[0]
    new_text = " ".join(args[1:]).strip()

    if not new_text:
        raise ValueError("Missing new note content")

    notes.edit_note(title, new_text)
    return "Note was successfully updated"


@input_error
def delete_note(args: list[str], notes: Notes) -> str:
    require_args(args, 1)

    title = args[0]
    notes.delete_note(title)
    return "Note was successfully deleted"


def show_all_notes(notes: Notes) -> str:
    return str(notes)
