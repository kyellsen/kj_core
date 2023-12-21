from pathlib import Path
from sqlalchemy import event
from typing import List, Type
from sqlalchemy.orm import Mapper
from sqlalchemy.engine import Connection
from sqlalchemy.ext.declarative import DeclarativeMeta
from ..classes.core_data_class import CoreDataClass

from ..utils.log_manager import get_logger

logger = get_logger(__name__)


class DataManager:
    def __init__(self, config):
        """
        Initialize a DataManager object.
        """
        self.data_directory = config.data_directory
        self.data_directory.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def get_new_filename(measurement_id: int, folder_name: str = None, prefix: str = None,
                         file_extension: str = "feather") -> str:
        """
        Generates a TMS data frame table name with optional prefix and folder.

        :param measurement_id: ID of the measurement to which the data belongs.
        :param prefix: Optional prefix for the file name.
        :param folder_name: Optional folder name to prepend.
        :param file_extension: Optional file extension, default is '.feather'.
        :return: New table name possibly including folder and prefix.
        """

        # Basisdateiname
        filename = f"m_id_{str(measurement_id).zfill(3)}"

        # Füge den Präfix hinzu, falls vorhanden
        if prefix:
            filename = f"{prefix}_{filename}"

        # Füge die Dateiendung hinzu
        if file_extension:
            filename = f"{filename}.{file_extension}"

        # Füge den Ordnerpfad hinzu, falls vorhanden
        if folder_name:
            filename = f"{folder_name}/{filename}"

        return filename

    def get_new_filepath(self, measurement_id: int, folder_name: str = None, prefix: str = None,
                         file_extension: str = "feather") -> str:
        """
        Generates the full file path for a TMS data frame.

        :param measurement_id: ID of the measurement to which the data belongs.
        :param folder_name: Optional folder name to prepend.
        :param prefix: Optional prefix for the file name.
        :param file_extension: Optional file extension, default is '.feather'.
        :return: Full file path including the data directory.
        """
        filename = self.get_new_filename(measurement_id, folder_name, prefix, file_extension)
        return str(self.data_directory / filename)

    @staticmethod
    def after_insert_listener(mapper: Mapper, connection: Connection, target: DeclarativeMeta):
        """Listener, der nach dem Einfügen einer neuen Instanz aufgerufen wird."""
        if isinstance(target, CoreDataClass):
            try:
                target.write_data_feather()
                logger.debug(f"Feather data written for new instance {target}")
            except Exception as e:
                logger.error(f"Error writing data to feather for new instance {target}: {e}")

    @staticmethod
    def after_update_listener(mapper: Mapper, connection: Connection, target: DeclarativeMeta):
        """Listener, der nach dem Aktualisieren einer Instanz aufgerufen wird."""
        if isinstance(target, CoreDataClass):
            try:
                target.write_data_feather()
                logger.debug(f"Feather data updated for instance {target}")
            except Exception as e:
                logger.error(f"Error writing data to feather for dirty instance {target}: {e}")

    @staticmethod
    def after_delete_listener(mapper: Mapper, connection: Connection, target: DeclarativeMeta):
        """Listener, der vor dem Löschen einer Instanz aufgerufen wird."""
        if isinstance(target, CoreDataClass):
            try:
                target.delete_data_feather()
                logger.debug(f"Feather data deleted for instance {target}")
            except Exception as e:
                logger.error(f"Error deleting data from feather for instance {target}: {e}")

    def register_listeners(self, class_models: List[Type[DeclarativeMeta]]):
        """
        Registriert Listener für after_insert, after_update und after_delete Ereignisse
        für eine Liste von SQLAlchemy Modellklassen.

        :param class_models: Eine Liste von SQLAlchemy Modellklassen.
        """
        for class_model in class_models:
            event.listen(class_model, 'after_insert', self.after_insert_listener)
            event.listen(class_model, 'after_update', self.after_update_listener)
            event.listen(class_model, 'after_delete', self.after_delete_listener)
