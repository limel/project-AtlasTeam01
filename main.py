import questionary

from addressBook.address_book import AddressBook
from addressBook.menu import run_contacts_menu
from notes import Notes, run_notes_menu
from store.serializer import PickleSerializer

book_serializer = PickleSerializer("address_book", AddressBook)
notes_serializer = PickleSerializer("notes", Notes)

MAIN_MENU_CHOICES = [
    questionary.Choice("Contacts", value="contacts"),
    questionary.Choice("Notes", value="notes"),
    questionary.Separator(),
    questionary.Choice("Exit", value="exit"),
]


def main() -> None:
    book = book_serializer.load_data()
    notes = notes_serializer.load_data()
    print("Welcome to the assistant bot! You can manage your contacts and notes here.")

    while True:
        command = questionary.select(
            "Choose a mode:",
            choices=MAIN_MENU_CHOICES,
        ).ask()

        if command is None or command == "exit":
            book_serializer.save_data(book)
            notes_serializer.save_data(notes)
            print("Good bye!")
            break

        if command == "contacts":
            run_contacts_menu(book)
        elif command == "notes":
            run_notes_menu(notes)


if __name__ == "__main__":
    main()
