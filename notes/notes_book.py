from datetime import datetime

from tabulate import tabulate


class Note:
    def __init__(self, title: str, content: str, note_id: int | None = None) -> None:
        self.note_id = note_id
        self.title = title.strip()
        self.content = content.strip()
        self.created_at = datetime.now()
        self.updated_at = self.created_at

        if not self.title:
            raise ValueError("Note title cannot be empty")

        if not self._contains_text(self.title):
            raise ValueError("Note title cannot contain only symbols")

        if not self.content:
            raise ValueError("Note content cannot be empty")

        if not self._contains_text(self.content):
            raise ValueError("Note content cannot contain only symbols")

    @staticmethod
    def _contains_text(value: str) -> bool:
        return any(character.isalnum() for character in value)

    def update_content(self, new_content: str) -> None:
        content = new_content.strip()
        if not content:
            raise ValueError("Note content cannot be empty")

        if not self._contains_text(content):
            raise ValueError("Note content cannot contain only symbols")

        self.content = content
        self.updated_at = datetime.now()

    def __str__(self) -> str:
        created_at = self.created_at.strftime("%d.%m.%Y %H:%M:%S")
        updated_at = self.updated_at.strftime("%d.%m.%Y %H:%M:%S")
        return (
            f"Title: {self.title}\n"
            f"Created: {created_at}\n"
            f"Updated: {updated_at}\n"
            f"Content: {self.content}"
        )


class Notes:
    TITLE_COLUMN_WIDTH = 20
    CONTENT_COLUMN_WIDTH = 50

    def __init__(self) -> None:
        self._notes: dict[int, Note] = {}
        self._next_id = 1

    def _generate_unique_title(self, title: str) -> str:
        normalized_title = title.strip()
        existing_titles = {note.title for note in self._notes.values()}

        if normalized_title not in existing_titles:
            return normalized_title

        suffix = 1
        generated_title = f"{normalized_title}_{suffix}"

        while generated_title in existing_titles:
            suffix += 1
            generated_title = f"{normalized_title}_{suffix}"

        return generated_title

    def add_note(self, note: Note) -> Note:
        note.title = self._generate_unique_title(note.title)
        note.note_id = self._next_id
        self._notes[note.note_id] = note
        self._next_id += 1
        return note

    def find_note(self, title: str) -> Note:
        normalized_title = title.strip()

        for note in self._notes.values():
            if note.title == normalized_title:
                return note

        raise ValueError(f"Note '{normalized_title}' not found")

    def edit_note(self, title: str, new_content: str) -> Note:
        note = self.find_note(title)
        note.update_content(new_content)
        return note

    def delete_note(self, title: str) -> Note:
        note = self.find_note(title)
        del self._notes[note.note_id]
        return note

    def __str__(self) -> str:
        if not self._notes:
            return (
                "You have no notes yet. "
                "Use 'add-note' command to create your first note."
            )

        rows = [
            [
                note.title,
                note.created_at.strftime("%d.%m.%Y %H:%M"),
                note.updated_at.strftime("%d.%m.%Y %H:%M"),
                note.content,
            ]
            for note in self._notes.values()
        ]

        return tabulate(
            rows,
            headers=["Title", "Created", "Updated", "Content"],
            tablefmt="grid",
            maxcolwidths=[
                self.TITLE_COLUMN_WIDTH,
                None,
                None,
                self.CONTENT_COLUMN_WIDTH,
            ],
        )
