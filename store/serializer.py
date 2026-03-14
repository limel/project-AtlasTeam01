import pickle
from pathlib import Path


class PickleSerializer:

    DATA_DIR = None

    @staticmethod
    def _find_data_dir() -> Path:
        for path in Path(__file__).resolve().parents:
            if (path / "pyproject.toml").exists():
                return path / "store"
        return Path.cwd() / "store"

    DATA_DIR = _find_data_dir()

    def __init__(self, filename: str, backup_class: type) -> None:
        self._filename = self.DATA_DIR / f"{filename}.pkl"
        self._backup_class = backup_class

    def save_data(self, data) -> None:
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(self._filename, "wb") as f:
            pickle.dump(data, f)

    def load_data(self):
        try:
            with open(self._filename, "rb") as f:
                return pickle.load(f)
        except (FileNotFoundError, pickle.UnpicklingError):
            return self._backup_class()
