# Atlas team project - 01

## Development setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install project dependencies:

```bash
pip install -r requirements.txt
```

Install the project itself as a package:

```bash
pip install .
```

The shared formatting and linting configuration is stored in `pyproject.toml`.

Run the tools from the repository root:

```bash
ruff check .
black .
```


# Atlas team project - 01

---

## For Users

### Installation & Usage

1. Install the package:
	```bash
	pip install .
	```
2. Activate your virtual environment (if used):
	```bash
	source .venv/bin/activate
	```
3. Run the bot from any directory:
	```bash
	atlas-assistant
	```

### Contacts menu

Enter the contacts menu:
```text
contacts
```
Available commands:
```text
add-contact
edit-contact
delete-contact
search-contacts
show-all
birthdays
back
```

### Notes menu

Enter the notes menu:
```text
notes
```
Available commands:
```text
add-note "title" content
find-note "title"
edit-note-title "title" new title
edit-note "title" new content
delete-note "title"
add-tag "title" tag [tag ...]
find-by-tag tag [tag ...]
all-notes
back
```

#### Features
- Contacts: add, edit, delete, search, birthdays, show all.
- Notes: add, edit, delete, tag, search by tag/title.
- Case-insensitive search, duplicate handling, and truncation for long titles.

---

## For Developers

### Development setup

1. Create and activate a virtual environment:
	```bash
	python3 -m venv .venv
	source .venv/bin/activate
	```
2. Install dependencies:
	```bash
	pip install -r requirements.txt
	```
3. Install the project as a package:
	```bash
	pip install .
	```

### Formatting & Linting

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

### Running in development mode

Start the bot from the repository root:
```bash
python main.py
```

### .gitignore

The `.gitignore` file excludes local virtual environments, Python cache files, and tool caches so each team member can work locally without committing machine-specific files.
