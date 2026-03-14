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

## Usage

The project supports two usage modes.

### 1. Run from the repository

Use this mode during development. Start the assistant bot from the repository root:

```bash
python main.py
```

### 2. Run as an installed package

Use this mode if you want to launch the bot from any directory. First install the project:

```bash
pip install .
```

The bot CLI command to run it from any directory is:

```bash
atlas-assistant
```

If you installed it into a virtual environment, make sure that environment is activated before running the command.


## Notes menu

Enter the notes menu:
```text
notes
```
Available commands:
```text
add-note
edit-note
delete-note
find-note
add-tag
find-by-tag
show-all-notes
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
