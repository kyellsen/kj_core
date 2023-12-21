from typing import List, Optional, Union, Any
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from kj_core.utils.base import Base
from kj_core.utils.runtime_manager import dec_runtime

from pathlib import Path
import shutil

from ..core_config import CoreConfig
from .log_manager import get_logger
from ..classes.core_data_class import CoreDataClass

logger = get_logger(__name__)


class DatabaseManager:
    """
    Class for managing database connections and sessions. It handles the creation and
    duplication of SQLite database files and establishes connections to these databases.
    """

    def __init__(self, config: CoreConfig):
        """
        Initializes the DatabaseManager with configurations.

        :param config: Core configuration object containing database settings.
        """
        self.config = config

        self.database_directory = Path(config.database_directory)
        self.database_directory.mkdir(parents=True, exist_ok=True)

        self.db_name = None
        self.db_url = None
        self.engine = None
        self.session_factory = None
        self._session = None

    def duplicate(self, database_path: str) -> None:
        """
        Duplicates a database file from a source path to the database directory.

        :param database_path: Path of the source database file.
        :raises FileNotFoundError: If the source database file is not found.
        """
        source = Path(database_path)

        if not source.is_file():
            logger.error(f"Database file not found at {database_path}")
            raise FileNotFoundError(f"Database file not found at {database_path}")

        destination = self.database_directory / source.name
        shutil.copy(source, destination)
        self.db_name = source.name
        logger.info(f"Database {source.name} duplicated to {destination}")

    def connect(self, db_name: str) -> None:
        """
        Connects to a SQLite database located in the database directory. If the database does not exist,
        it creates a new one. It logs whether an existing database was connected or a new one was created.

        :param db_name: Name of the database file to connect to.
        :raises SQLAlchemyError: If there is an issue connecting to the database.
        """
        self.db_name = db_name
        db_file_path = self.database_directory / self.db_name

        # Check if database file exists and log accordingly
        if db_file_path.is_file():
            logger.info(f"Connecting to existing database at {db_file_path}")
        else:
            logger.info(f"Database {db_file_path} not found. Creating a new database.")

        try:
            self.engine = create_engine(f"sqlite:///{db_file_path}")
            Base.metadata.create_all(self.engine)
            self.session_factory = sessionmaker(bind=self.engine, autocommit=False)
            self._session = self.session_factory()  # Erstellen einer Session
            logger.info(f"Connected to the database at {db_file_path}")
        except SQLAlchemyError as e:
            logger.error(f"Error connecting to the database: {e}")
            raise

    def disconnect(self) -> None:
        """
        Closes the database connection and session properly, checking for unsaved changes.
        """
        if self._session:
            if self._session.dirty:
                self.ask_commit(self._session)

            self._session.close()
            self._session = None
            logger.info("Database session closed.")

        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed.")

    def commit(self):
        try:
            # # Erkennen von neuen, geänderten und gelöschten Instanzen
            # new_instances = self._session.new
            # dirty_instances = self._session.dirty
            # deleted_instances = self._session.deleted

            self._session.commit()
            logger.info("Transaction committed.")

            # # Nachdem der Commit erfolgreich war, verarbeiten Sie die Änderungen
            # self.process_instance_changes(new_instances, dirty_instances, deleted_instances)

        except Exception as e:
            logger.error(f"Error during commit: {e}")
            self._session.rollback()
            logger.info("Transaction rolled back due to an error.")
            raise

    # @staticmethod
    # @dec_runtime
    # def process_instance_changes(new_instances, dirty_instances, deleted_instances):
    #     logger.debug(f"Starting process_instance_changes")
    #
    #     # Loggen der neuen Instanzen
    #     if new_instances:
    #         logger.info(
    #             f"Processing new instances: {[instance for instance in new_instances if isinstance(instance, CoreDataClass)]}")
    #         for instance in new_instances:
    #             if isinstance(instance, CoreDataClass):
    #                 try:
    #                     instance.write_data_feather()
    #                     logger.debug(f"Data written to feather for new instance: {instance}")
    #                 except Exception as e:
    #                     logger.error(f"Error writing data to feather for new instance {instance}: {e}")
    #
    #     # Loggen der geänderten Instanzen
    #     if dirty_instances:
    #         logger.info(
    #             f"Processing dirty instances: {[instance for instance in dirty_instances if isinstance(instance, CoreDataClass)]}")
    #         for instance in dirty_instances:
    #             if isinstance(instance, CoreDataClass):
    #                 try:
    #                     instance.write_data_feather()
    #                     logger.debug(f"Data written to feather for dirty instance: {instance}")
    #                 except Exception as e:
    #                     logger.error(f"Error writing data to feather for dirty instance {instance}: {e}")
    #
    #     # Loggen der gelöschten Instanzen
    #     if deleted_instances:
    #         logger.info(
    #             f"Processing deleted instances: {[instance for instance in deleted_instances if isinstance(instance, CoreDataClass)]}")
    #         for instance in deleted_instances:
    #             if isinstance(instance, CoreDataClass):
    #                 try:
    #                     instance.delete_data_feather()
    #                     logger.debug(f"Data deleted from feather for instance: {instance}")
    #                 except Exception as e:
    #                     logger.error(f"Error deleting data from feather for instance {instance}: {e}")
    #
    #     logger.debug("Finished process_instance_changes")

    @property
    def session(self) -> Session:
        """
        Returns the same session instance for the lifetime of the DatabaseManager instance.
        """
        if not self._session:
            raise Exception("Database not connected or session not initialized.")
        return self._session

    @staticmethod
    def ask_commit(session):
        """
        Asks the user if they want to commit the changes.

        Args:
            session (Session): The session in which the changes were made.
        """
        commit = input("Do you want to commit? (True/False): ")
        if commit.lower() == 'true':
            try:
                session.commit()
                logger.info("Changes committed successfully to the database.")
            except Exception as e:
                session.rollback()
                logger.error(f"Error while committing to the database: {e}")
                raise e
        else:
            logger.warning("Changes were not committed to the database and discarded.")

    def load(self, class_name, ids: Optional[Union[int, List[int]]] = None) -> List[Any]:
        """
        Load instances of a specified class from a SQLite database using SQLAlchemy.

        Parameters
        ----------
        class_name : class
            The class of which instances are to be loaded.
        ids : int, list of int, or None, optional
            The primary keys of the instances to load. If ids is None, all instances are loaded.
            Default is None.

        Returns
        -------
        list of instances
            The loaded instances. If only one instance is loaded, it is returned inside a list.
            If no instances are found, an empty list is returned.
        """
        try:
            # Get the name of the primary key attribute (could be id, project_id, series_id, etc.)
            primary_key = inspect(class_name).primary_key[0].name

            if ids is None:
                logger.info(f"Loading all instances of '{class_name.__name__}'")
                objs = self.session.query(class_name).all()
            elif isinstance(ids, int):
                logger.info(f"Loading instance of '{class_name.__name__}' with primary key '{ids}'")
                instance = self.session.query(class_name).filter(getattr(class_name, primary_key) == ids).one_or_none()
                objs = [instance] if instance else []
            elif isinstance(ids, list):
                logger.info(f"Loading instances of '{class_name.__name__}' with primary keys '{ids}'")
                objs = self.session.query(class_name).filter(getattr(class_name, primary_key).in_(ids)).all()
            else:
                raise ValueError('Invalid type of ids. Must be int, list of int, or None.')

            if not objs:
                logger.warning(f"No instances of '{class_name.__name__}' with primary keys '{ids}' found")

            logger.info(f"Loading successful '{len(objs)}' instances of class {class_name.__name__}.")
            return objs
        except Exception as e:
            logger.error(f"Failed to load instances of '{class_name.__name__}' with primary keys '{ids}' from db. Error: '{e}'")
            raise
