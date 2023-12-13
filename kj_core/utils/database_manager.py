from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from kj_core.utils.base import Base

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

    def __init__(self, config: CoreConfig):  # , base: declarative_base
        """
        Initializes the DatabaseManager with configurations.

        :param config: Core configuration object containing database settings.
        """
        self.config = config
        # self.Base = base

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
            # Erkennen von neuen, geänderten und gelöschten Instanzen
            new_instances = self._session.new
            dirty_instances = self._session.dirty
            deleted_instances = self._session.deleted

            self._session.commit()
            logger.info("Transaction committed.")

            # Nachdem der Commit erfolgreich war, verarbeiten Sie die Änderungen
            self.process_instance_changes(new_instances, dirty_instances, deleted_instances)

        except Exception as e:
            logger.error(f"Error during commit: {e}")
            self._session.rollback()
            logger.info("Transaction rolled back due to an error.")
            raise

    @staticmethod
    def process_instance_changes(new_instances, dirty_instances, deleted_instances):
        for instance in new_instances:
            if isinstance(instance, CoreDataClass):
                instance.write_data_file()  # oder eine andere relevante Methode
        for instance in dirty_instances:
            if isinstance(instance, CoreDataClass):
                instance.write_data_file()
        for instance in deleted_instances:
            if isinstance(instance, CoreDataClass):
                instance.delete_data_file()

    def get_session(self) -> Session:
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
