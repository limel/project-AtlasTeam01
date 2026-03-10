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

## Git ignore

The `.gitignore` file excludes local virtual environments, Python cache files, and tool caches so each team member can work locally without committing machine-specific files.
