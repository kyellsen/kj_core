from sqlalchemy import event, inspect
from typing import List, Type
from sqlalchemy.orm import Mapper
from sqlalchemy.engine import Connection
from sqlalchemy.ext.declarative import DeclarativeMeta

from kj_logger import get_logger

logger = get_logger(__name__)

from ..classes.core_data_class import CoreDataClass


class DataManager:
    def __init__(self, config):
        """
        Initialize a DataManager object.
        """
        self.config = config
        self.data_directory = config.data_directory
        self.data_directory.mkdir(parents=True, exist_ok=True)

        logger.info(f"{self} initialized! Code: 003")

    def __repr__(self) -> str:
        """
        Returns a detailed string representation of the DataManager instance.
        """
        return (
            f"<DataManager>\n"
            f"  Data Directory:     {self.data_directory}\n"
            f"  From Config:        {self.config.__class__.__name__}\n"
        )

    @staticmethod
    def get_new_filename(data_id: int, prefix: str = None,
                         file_extension: str = None) -> str:
        """
        Generates a DataFrame table name with optional prefix and extension.

        :param data_id: ID of the data to which the data belongs.
        :param prefix: Optional prefix for the file name.
        :param file_extension: Optional file extension.
        :return: New table name possibly including folder and prefix.
        """

        # Basisdateiname
        filename = f"id_{str(data_id).zfill(5)}"

        # Füge den Präfix hinzu, falls vorhanden
        if prefix:
            filename = f"{prefix}_{filename}"

        # Füge die Dateiendung hinzu
        if file_extension:
            filename = f"{filename}.{file_extension}"

        return str(filename)

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
            # Überprüfen, ob das 'data'-Attribut geändert wurde
            update = target.data_changed
            logger.debug(f"Update: {target}.data_changed = '{update}'")

            if update:
                target.data_changed = False
                try:
                    target.write_data_feather()
                    logger.debug(
                        f"Feather data updated for instance '{target.__class__.__name__}': {target.data_id}")
                except Exception as e:
                    logger.error(
                        f"Error writing data to feather for dirty instance '{target.__class__.__name__}': {target.data_id}: {e}")

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
        try:
            for class_model in class_models:
                event.listen(class_model, 'after_insert', self.after_insert_listener)
                event.listen(class_model, 'after_update', self.after_update_listener)
                event.listen(class_model, 'after_delete', self.after_delete_listener)
            logger.info(f"Successfully registered listeners: '{class_models}'")
        except Exception as e:
            logger.critical(f"Error in register_listeners: {e}")
