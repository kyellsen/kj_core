import pandas as pd
from pathlib import Path
from sqlalchemy import orm

from kj_core.utils.runtime_manager import dec_runtime


class CoreDataClass:
    def __init__(self, data_id: int = None, data: pd.DataFrame = None, data_filepath: str = None):
        self.data_id = data_id
        self._data = None
        self.data = data
        self.data_filepath = data_filepath if data_filepath else None
        self._data_changed = True

    @orm.reconstructor
    def _init_on_load(self):
        # Diese Methode wird vom SQLAlchemy ORM nach dem Laden einer Instanz aufgerufen
        self._init()

    def _init(self):
        self._data = None
        self._data_changed = False

    @property
    def data(self):
        if self._data is None and self.data_filepath:
            self.read_data_feather()
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = new_data
        self._data_changed = True

    @dec_runtime
    def read_data_feather(self):
        if self.data_filepath and Path(self.data_filepath).exists():
            # Lade die Daten mit Pandas
            self._data = pd.read_feather(Path(self.data_filepath))

    @dec_runtime
    def write_data_feather(self):
        # Überprüfen, ob ein Pfad für die Datei vorhanden ist
        if self.data_filepath and self._data_changed:
            # Stellen Sie sicher, dass das Verzeichnis existiert
            Path(self.data_filepath).parent.mkdir(parents=True, exist_ok=True)
            # Speichere die Daten mit Pandas in ein Feather-Format
            self._data.to_feather(self.data_filepath)

            # Setze das Flag `_data_changed` zurück, da die Daten jetzt gespeichert wurden
            self._data_changed = False

    @dec_runtime
    def delete_data_feather(self):
        if self.data_filepath:
            Path(self.data_filepath).unlink()
