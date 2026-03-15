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


def ask_select(items, prompt: str, empty_msg: str) -> str:
    """
    Generic selection prompt for lists of Choice or strings.
    Returns the selected value or raises ValueError if cancelled.
    """
    if not items:
        raise ValueError(empty_msg)
    value = questionary.select(prompt, choices=items).ask()
    if value is None:
        raise ValueError("Selection cancelled by user")
    return value


def ask_contact(book, prompt: str = "Select contact:"):
    """
    Prompts user to select a contact or go back.
    Returns the contact object or None if cancelled.
    """
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
    choices.append(Choice(title="Back to contact menu", value=None))
    user_choice = ask_select(choices, prompt, "No contacts yet")
    if user_choice is None:
        return None
    return book.find_by_id(user_choice)


def ask_title(notes, prompt: str = "Select note:") -> str:
    """
    Prompts user to select a note title.
    Returns the selected title or raises ValueError if cancelled.
    """
    return ask_select(notes.titles, prompt, "You have no notes yet")
