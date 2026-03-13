from datetime import datetime

from tabulate import tabulate


class Note:
    MAX_TITLE_LENGTH = 80

    def __init__(
        self,
        title: str,
        content: str,
        note_id: int | None = None,
        tags: list[str] | None = None,
    ) -> None:
        self.note_id = note_id
        self.title = self._normalize_title(title)
        self.content = content.strip()
        self.tags = self._normalize_tags(tags or [])
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

    @staticmethod
    def _normalize_tags(tags: list[str]) -> list[str]:
        # Use a list for order and a set for uniqueness.
        normalized_tags: list[str] = []
        unique_tags: set[str] = set()

        for tag in tags:
            normalized_tag = tag.strip().casefold()
            if not normalized_tag or normalized_tag in unique_tags:
                continue

            if not Note._contains_text(normalized_tag):
                raise ValueError("Tag cannot contain only symbols")

            unique_tags.add(normalized_tag)
            normalized_tags.append(normalized_tag)

        return normalized_tags

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

    def add_tags(self, tags: list[str]) -> None:
        new_tags = self._normalize_tags(tags)
        if not new_tags:
            raise ValueError("At least one valid tag must be provided")

        existing_tags = self.tags
        tags_to_add = [tag for tag in new_tags if tag not in existing_tags]

        if not tags_to_add:
            raise ValueError("All provided tags already exist in this note")

        self.tags.extend(tags_to_add)
        self.updated_at = datetime.now()

    def __str__(self) -> str:
        return tabulate(
            [
                [
                    self.title,
                    ", ".join(self.tags) if self.tags else "-",
                    self.created_at.strftime("%d.%m.%Y %H:%M"),
                    self.updated_at.strftime("%d.%m.%Y %H:%M"),
                    self.content,
                ]
            ],
            headers=["Title", "Tags", "Created", "Updated", "Content"],
            tablefmt="grid",
            maxcolwidths=[20, 20, None, None, 50],
        )


class Notes:
    TITLE_COLUMN_WIDTH = 20
    TAGS_COLUMN_WIDTH = 20
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

    @staticmethod
    def _parse_tags(tags: list[str]) -> list[str]:
        parsed_tags: list[str] = []

        for tag in tags:
            parsed_tags.extend(part.strip().lstrip("#") for part in tag.split(","))

        return parsed_tags

    def add_tag(self, title: str, tags: list[str]) -> Note:
        note = self.find_note(title)
        note.add_tags(self._parse_tags(tags))
        return note

    def sort_by_tag(self, tags: list[str]) -> list[Note]:
        normalized_tags = Note._normalize_tags(self._parse_tags(tags))
        if not normalized_tags:
            raise ValueError("At least one valid tag must be provided")

        matching_notes = [
            note
            for note in self._notes.values()
            if all(tag in note.tags for tag in normalized_tags)
        ]

        return sorted(matching_notes, key=lambda note: note.title.casefold())

    def format_notes(self, notes: list[Note]) -> str:
        if not notes:
            return "No notes found for the provided tag filters."

        rows = [
            [
                note.title,
                ", ".join(note.tags) if note.tags else "-",
                note.created_at.strftime("%d.%m.%Y %H:%M"),
                note.updated_at.strftime("%d.%m.%Y %H:%M"),
                note.content,
            ]
            for note in notes
        ]

        return tabulate(
            rows,
            headers=["Title", "Tags", "Created", "Updated", "Content"],
            tablefmt="grid",
            maxcolwidths=[
                self.TITLE_COLUMN_WIDTH,
                self.TAGS_COLUMN_WIDTH,
                None,
                None,
                self.CONTENT_COLUMN_WIDTH,
            ],
        )

    def __str__(self) -> str:
        if not self._notes:
            return (
                "You have no notes yet. "
                "Use 'add-note' command to create your first note."
            )

        return self.format_notes(list(self._notes.values()))
