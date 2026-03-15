# Atlas Team Assistant

Educational CLI assistant for managing contacts and notes.

The assistant allows you to store contacts and notes, search them, and view upcoming birthdays directly from the terminal.

## Installation

1. Clone the repository and install the project:
   ```bash
   git clone <repository-url>
   ```
2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install the package:
   ```bash
   pip install .
   ```

## Running the Assistant

There are two ways to run the bot.

1. Run from the repository (development)

Use this mode while developing the project.
```bash
python main.py
```

2. Run as an installed CLI command

After installation, the assistant can be started from any directory:
```bash
atlas-assistant
```
If the project was installed into a virtual environment, make sure the environment is activated before running the command.

After starting the assistant you will see the main menu.

Example commands:

```text
contacts
notes
exit
```

The project supports two usage modes.

```text
contacts
notes
```

## Contacts Menu

| Command | Description |
|--------|-------------|
| add-contact | Create a new contact |
| edit-contact | Edit an existing contact |
| delete-contact | Remove a contact |
| search-contacts | Search contacts by name |
| show-all | Display all saved contacts |
| birthdays | Show upcoming birthdays |
| back | Return to the main menu |

## Notes Menu

| Command | Description |
|--------|-------------|
| add-note | Create a new note |
| find-note | Search for a note by title |
| edit-title | Rename a note |
| edit-content | Change note content |
| delete-note | Remove a note |
| add-tag-to-note | Add tags to an existing note |
| sort-by-tag | Find notes by tags |
| all-notes  | Show all notes |
| back | Return to the main menu |

# Data Storage
The assistant stores data locally using pickle serialization.

Two files are created automatically:
```text
store/address_book.pkl
store/notes.pkl
```
These files contain saved contacts and notes.
---

## Project Structure

Example project layout:

```text
atlas-team-assistant/
│
├── addressBook/
├── helpers/
├── notes/
├── store/
├── main.py
├── decorators.py
├── pyproject.toml
└── README.md
```

## Formatting & Linting

The shared formatting and linting configuration is stored in `pyproject.toml`.

Run from the repository root:

```bash
ruff check .
black .
```

Apply Ruff auto-fixes before formatting:

```bash
ruff check . --fix
black .
```

### .gitignore

The `.gitignore` file excludes local virtual environments, Python cache files, and tool caches so each team member can work locally without committing machine-specific files.

