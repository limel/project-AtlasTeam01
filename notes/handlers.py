from decorators import input_error

from .notes_book import Note, Notes


def require_args(args: list[str], count: int, usage: str) -> None:
    if len(args) < count:
        raise ValueError(f"Usage: {usage}")


@input_error
def add_note(args: list[str], notes: Notes) -> str:
    require_args(args, 2, 'add-note "title" content')

    title = args[0]
    content = " ".join(args[1:])
    note = notes.add_note(Note(title=title, content=content))

    # Titles may be normalized by truncation and duplicate suffixing.
    if note.title != title:
        return f"Note was successfully added as '{note.title}'"

    return "Note was successfully added"


@input_error
def show_note(args: list[str], notes: Notes) -> str:
    require_args(args, 1, 'find-note "title"')

    title = args[0]
    return str(notes.find_note(title))


@input_error
def edit_note_title(args: list[str], notes: Notes) -> str:
    require_args(args, 2, 'edit-note-title "title" "new title"')

    title = args[0]
    new_title = " ".join(args[1:]).strip()

    note = notes.edit_note_title(title, new_title)
    return f"Note title was successfully updated to '{note.title}'"


@input_error
def edit_note_content(args: list[str], notes: Notes) -> str:
    require_args(args, 2, 'edit-note "title" new content')

    title = args[0]
    new_text = " ".join(args[1:]).strip()

    notes.edit_note(title, new_text)
    return "Note content was successfully updated"


@input_error
def delete_note(args: list[str], notes: Notes) -> str:
    require_args(args, 1, 'delete-note "title"')

    title = args[0]
    notes.delete_note(title)
    return "Note was successfully deleted"


@input_error
def add_tag_to_note(args: list[str], notes: Notes) -> str:
    require_args(args, 2, 'add-tag "title" tag [tag ...]')

    title = args[0]
    tags = args[1:]
    note = notes.add_tag(title, tags)
    return f"Tags were successfully added to '{note.title}'"


@input_error
def get_notes_sorted_by_tag(args: list[str], notes: Notes) -> str:
    require_args(args, 1, "find-by-tag tag [tag ...]")

    return notes.format_notes(notes.sort_by_tag(args))


def show_all_notes(notes: Notes) -> str:
    return str(notes)
