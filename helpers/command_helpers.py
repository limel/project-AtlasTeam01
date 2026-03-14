import questionary
from questionary import Choice


def ask_text(
    prompt: str,
    required: bool = True,
    default: str = "",
    validator=None,
) -> str:

    def validate(text: str):
        text = text.strip()

        if required and not text:
            return f"{prompt.rstrip(': ')} cannot be empty"

        if validator and text:
            try:
                validator(text)
            except ValueError as e:
                return str(e)

        return True

    value = questionary.text(
        prompt,
        default=default,
        validate=validate,
    ).ask()

    if value is None:
        raise ValueError("Input cancelled by user")

    return value.strip()


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
            title=(
                f"{rec.name.value}\n"
                f"{' ' * 3}(Phones: "
                f"{', '.join(p.value for p in rec.phones) or 'N/A'})"
            ),
            value=str(rec._id),
        )
        for rec in book.values()
    ]
    choices.append(questionary.Separator())
    choices.append(Choice(title="Back to contact menu", value="back"))
    contact_id = ask_select(choices, prompt, "No contacts yet")

    if contact_id == "back":
        return None
    return book.find_by_id(contact_id)


def ask_title(notes, prompt: str = "Select note:") -> str:
    titles = notes.titles

    if not titles:
        raise ValueError("You have no notes yet")
    value = questionary.select(prompt, choices=titles).ask()
    if value is None:
        raise ValueError("Selection cancelled by user")
    return value
