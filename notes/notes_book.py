from datetime import datetime

from tabulate import tabulate


class Note:
    MAX_TITLE_LENGTH = 80

    def __init__(self, title: str, content: str, note_id: int | None = None) -> None:
        self.note_id = note_id
        self.title = self._normalize_title(title)
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

    @classmethod
    def _normalize_title(cls, title: str) -> str:
        return title.strip()[: cls.MAX_TITLE_LENGTH].rstrip()

    def update_title(self, new_title: str) -> None:
        title = self._normalize_title(new_title)
        if not title:
            raise ValueError("Note title cannot be empty")

        if not self._contains_text(title):
            raise ValueError("Note title cannot contain only symbols")

        self.title = title
        self.updated_at = datetime.now()

    def update_content(self, new_content: str) -> None:
        content = new_content.strip()
        if not content:
            raise ValueError("Note content cannot be empty")

        if not self._contains_text(content):
            raise ValueError("Note content cannot contain only symbols")

        self.content = content
        self.updated_at = datetime.now()

    def __str__(self) -> str:
        return tabulate(
            [
                [
                    self.title,
                    self.created_at.strftime("%d.%m.%Y %H:%M"),
                    self.updated_at.strftime("%d.%m.%Y %H:%M"),
                    self.content,
                ]
            ],
            headers=["Title", "Created", "Updated", "Content"],
            tablefmt="grid",
            maxcolwidths=[20, None, None, 50],
        )


class Notes:
    TITLE_COLUMN_WIDTH = 20
    CONTENT_COLUMN_WIDTH = 50

    def __init__(self) -> None:
        self._notes: dict[int, Note] = {}
        self._next_id = 1

    @staticmethod
    def _normalize_title_key(title: str) -> str:
        return title.strip().casefold()

    def _generate_unique_title(
        self, title: str, excluded_note_id: int | None = None
    ) -> str:
        normalized_title = title.strip()
        existing_titles = {
            self._normalize_title_key(note.title)
            for note in self._notes.values()
            if note.note_id != excluded_note_id
        }

        if self._normalize_title_key(normalized_title) not in existing_titles:
            return normalized_title

        suffix = 1
        generated_title = self._build_suffixed_title(normalized_title, suffix)

        while self._normalize_title_key(generated_title) in existing_titles:
            suffix += 1
            generated_title = self._build_suffixed_title(normalized_title, suffix)

        return generated_title

    @staticmethod
    def _build_suffixed_title(title: str, suffix: int) -> str:
        suffix_text = f" ({suffix})"
        available_length = Note.MAX_TITLE_LENGTH - len(suffix_text)
        truncated_title = title[:available_length].rstrip()
        return f"{truncated_title}{suffix_text}"

    def add_note(self, note: Note) -> Note:
        note.title = self._generate_unique_title(note.title)
        note.note_id = self._next_id
        self._notes[note.note_id] = note
        self._next_id += 1
        return note

    def find_note(self, title: str) -> Note:
        normalized_title = title.strip()
        normalized_key = self._normalize_title_key(normalized_title)

        for note in self._notes.values():
            if self._normalize_title_key(note.title) == normalized_key:
                return note

        raise ValueError(f"Note '{normalized_title}' not found")

    def edit_note(self, title: str, new_content: str) -> Note:
        note = self.find_note(title)
        note.update_content(new_content)
        return note

    def edit_note_title(self, title: str, new_title: str) -> Note:
        note = self.find_note(title)
        unique_title = self._generate_unique_title(new_title, note.note_id)
        note.update_title(unique_title)
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
