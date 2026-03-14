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

Apply Ruff auto-fixes before formatting:

```bash
ruff check . --fix
black .
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

## Notes commands

Enter the notes menu with:

```text
notes
```

Available notes commands:

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

Examples:

```text
add-note "Project plan" finish database schema
find-note "Project plan"
edit-note-title "Project plan" "Project plan v2"
edit-note "Project plan v2" update API section

add-tag "Project plan v2" task urgent
add-tag "Project plan v2" #important

find-by-tag task
find-by-tag #urgent

delete-note "Project plan v2"
```

Notes behavior:

- Titles can contain multiple words.
- Title matching is case-insensitive.
- Long titles are truncated to 80 characters.
- Duplicate titles receive a suffix like `(1)`.
- Tags are case-insensitive and duplicates are ignored.

## Git ignore

The `.gitignore` file excludes local virtual environments, Python cache files, and tool caches so each team member can work locally without committing machine-specific files.
