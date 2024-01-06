import pandas as pd
from pathlib import Path
from sqlalchemy import orm
from datetime import datetime

from kj_core.utils.runtime_manager import dec_runtime


class CoreDataClass:

    def __init__(self, data_id: int = None, data: pd.DataFrame = None, data_filepath: str = None,
                 datetime_added: datetime = None, datetime_last_edit: datetime = None):
        self.data_id = data_id
        self._data = None
        self.data = data
        self.data_filepath = data_filepath if data_filepath else None

        # For datetime_added and datetime_last_edit, using current datetime if not provided
        self.datetime_added = datetime_added if datetime_added is not None else datetime.now()
        self.datetime_last_edit = datetime_last_edit if datetime_last_edit is not None else datetime.now()

    @orm.reconstructor
    def _init_on_load(self):
        # Diese Methode wird vom SQLAlchemy ORM nach dem Laden einer Instanz aufgerufen
        self._data = None

    @property
    def data(self):
        if self._data is None and self.data_filepath:
            self.read_data_feather()
            if hasattr(self, 'validate_data'):  # Prüfen, ob validate_data existiert
                self.validate_data()  # validate_data aufrufen, wenn vorhanden
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = new_data

    @dec_runtime
    def read_data_feather(self):
        if self.data_filepath and Path(self.data_filepath).exists():
            # Lade die Daten mit Pandas
            self._data = pd.read_feather(Path(self.data_filepath))

    @dec_runtime
    def write_data_feather(self):
        # Überprüfen, ob ein Pfad für die Datei vorhanden ist
        if self.data_filepath:
            # Stellen Sie sicher, dass das Verzeichnis existiert
            Path(self.data_filepath).parent.mkdir(parents=True, exist_ok=True)
            # Speichere die Daten mit Pandas in ein Feather-Format
            self._data.to_feather(self.data_filepath)

    @dec_runtime
    def delete_data_feather(self):
        if self.data_filepath:
            Path(self.data_filepath).unlink()
