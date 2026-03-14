import questionary
from questionary import Choice


def ask_text(prompt: str, required: bool = True, default: str = "") -> str:
    value = questionary.text(prompt, default=default).ask()
    if value is None:
        raise ValueError("Input cancelled by user")
    value = value.strip()
    if required and not value:
        raise ValueError(f"{prompt.rstrip(': ')} cannot be empty")
    return value


def ask_select(items: list[Choice], prompt: str, empty_msg: str) -> str:
    if not items:
        raise ValueError(empty_msg)

    value = questionary.select(prompt, choices=items).ask()
    if value is None:
        raise ValueError("Selection cancelled by user")
    return value


def ask_contact(book, prompt: str = "Select contact:"):
    choices = [
        Choice(
            title=f"{rec.name.value}\n{(' ' * 3)}(Phones: {', '.join(p.value for p in rec.phones) or 'N/A'})",
            value=str(rec._id),
        )
        for rec in book.values()
    ]
    id = ask_select(choices, prompt, "No contacts yet")
    return book.find_by_id(id)


def ask_title(notes, prompt: str = "Select note:") -> str:
    titles = notes.titles

    if not titles:
        raise ValueError("You have no notes yet")
    value = questionary.select(prompt, choices=titles).ask()
    if value is None:
        raise ValueError("Selection cancelled by user")
    return value
