import questionary


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


def ask_select(items: list[str], prompt: str, empty_msg: str) -> str:
    if not items:
        raise ValueError(empty_msg)
    if len(items) == 1:
        return items[0]
    value = questionary.select(prompt, choices=items).ask()
    if value is None:
        raise ValueError("Selection cancelled by user")
    return value


def ask_contact(book, prompt: str = "Select contact:"):
    names = list(book.data.keys())
    name = ask_select(names, prompt, "No contacts yet")
    return book.find(name)


def ask_title(notes, prompt: str = "Select note:") -> str:
    titles = notes.titles

    if not titles:
        raise ValueError("You have no notes yet")
    value = questionary.select(prompt, choices=titles).ask()
    if value is None:
        raise ValueError("Selection cancelled by user")
    return value
