import pickle
from collections.abc import Callable


def pickle_serializer(filename: str, backup_class: type) -> tuple[Callable, Callable]:
    pickle_filename = f"{filename}.pkl"

    def save_data(data):
        with open(pickle_filename, "wb") as f:
            pickle.dump(data, f)

    def load_data():
        try:
            with open(pickle_filename, "rb") as f:
                return pickle.load(f)
        except (FileNotFoundError, pickle.UnpicklingError):
            return backup_class()

    return save_data, load_data
