import pandas as pd
from pathlib import Path


class CoreDataClass:
    def __init__(self, data_id=None, data: pd.DataFrame = None, data_filepath: str = None):
        self.data_id = data_id
        self._data = data
        self.data_filepath = Path(data_filepath) if data_filepath else None
        self._data_changed = False


    @property
    def data(self):
        if self._data is None and self.data_filepath:
            self.read_data_file()
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = new_data
        self._data_changed = True

    def read_data_file(self):
        if self.data_filepath and self.data_filepath.exists():
            # Lade die Daten mit Pandas
            self._data = pd.read_feather(self.data_filepath)

    def write_data_file(self):
        if self._data_changed and self.data_filepath:
            # Speichere die Daten mit Pandas in ein Feather-Format
            self._data.to_feather(self.data_filepath)

            # Setze das Flag `_data_changed` zurück, da die Daten jetzt gespeichert wurden
            self._data_changed = False

    def delete_data_file(self):
        if self.data_filepath and self.data_filepath.exists():
            self.data_filepath.unlink()
