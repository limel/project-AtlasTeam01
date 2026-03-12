import pickle


class PickleSerializer:
    def __init__(self, filename: str, backup_class: type) -> None:
        self._filename = f"{filename}.pkl"
        self._backup_class = backup_class

    def save_data(self, data) -> None:
        with open(self._filename, "wb") as f:
            pickle.dump(data, f)

    def load_data(self):
        try:
            with open(self._filename, "rb") as f:
                return pickle.load(f)
        except (FileNotFoundError, pickle.UnpicklingError):
            return self._backup_class()
