from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from ..core_config import CoreConfig

from ..utils.log_manager import get_logger

logger = get_logger(__name__)

class DatabaseManager:
    """
    A class for managing database connections and sessions.
    """

    def __init__(self, config: CoreConfig):
        """
        Constructor of the DatabaseManager class.
        """
        self.config = config
        self.engine = create_engine(f'sqlite:///{self.config.database_path}', echo=self.config.log_level == 'debug')
        self.session_factory = sessionmaker(bind=self.engine)
        self.current_session = None

    def connect(self):
        """
        Establishes a connection to the database.
        """
        try:
            # In the case of SQLite, connect is not strictly necessary as it will connect on demand
            # but we can still try to make a connection here for the sake of checking.
            connection = self.engine.connect()
            connection.close()  # immediately close the connection
            logger.info("Database connection established.")
        except SQLAlchemyError as e:
            logger.error(f"Error establishing a database connection: {e}")
            raise

    def disconnect(self):
        """
        Closes the database connection.
        """
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed.")

    def open_session(self):
        """
        Opens a new session if one does not currently exist.
        """
        if self.current_session is None or self.current_session.is_closed():
            self.current_session = self.session_factory()
            logger.info("New database session opened.")
        return self.current_session

    def get_session(self) -> Session:
        """
        Retrieves the current session or opens a new one if necessary.
        """
        return self.open_session()

    def close_session(self):
        """
        Closes the current session.
        """
        if self.current_session and not self.current_session.is_closed():
            self.current_session.close()
            logger.info("Database session closed.")
            self.current_session = None

    def commit(self):
        """
        Commits the current session.
        """
        if self.current_session and not self.current_session.is_closed():
            try:
                self.current_session.commit()
                logger.info("Session committed.")
            except SQLAlchemyError as e:
                self.current_session.rollback()
                logger.error(f"Error committing the session: {e}")
                raise

    @staticmethod
    def ask_commit(session):
        """
        Asks the user if they want to commit the changes.

        Args:
            session (Session): The session in which the changes were made.
        """
        # START GUI MODIFICATION
        commit = input("Do you want to commit? (True/False): ")
        # END GUI MODIFICATION
        if commit.lower() == 'true':
            try:
                session.commit()
                logger.info("Changes committed successfully to the database.")
            except Exception as e:
                session.rollback()
                logger.error("Error while committing to the database: ", e)
                raise e
        else:
            logger.warning("Changes were not committed to the database and discarded.")
