from pathlib import Path
from typing import Optional
from .utils.log_manager import get_logger

VALID_LOG_LEVELS = {"debug", "info", "warning", "error", "critical"}


class CoreConfig:
    """
    Class for managing the core configuration settings across multiple packages.
    Ensures that only one instance of the configuration is active at any time.
    """

    package_name = "kj_core"
    default_working_directory = r"C:\kyellsen\006_Packages\test_working_directory_core_config"
    default_log_level = "info"

    def __init__(self, working_directory: Optional[str] = None, log_level: Optional[str] = None) -> None:
        """
        Initializes the configuration settings. This method is executed only once.

        Parameters:
            working_directory (Optional[str]): The path to the working directory. Defaults to a predefined path.
            log_level (Optional[str]): The logging level. Defaults to 'info'.
        """
        self.working_directory = Path()
        self.log_level = str()

        self.set_working_directory(working_directory if working_directory is not None else self.default_working_directory)

        self.set_log_level(log_level if log_level is not None else self.default_log_level)
        self.save_logs_to_file = False

        self.log_directory = self.working_directory / "logs"
        self.plot_directory = self.working_directory / "plots"
        self.data_directory = self.working_directory / "data"
        self.database_directory = self.working_directory / "databases"

    def set_working_directory(self, directory: str) -> None:
        """
        Sets the working directory to the specified path.

        Parameters:
            directory (Path): The directory path to set as the working directory.
        """
        directory = Path(directory)
        logger = get_logger(__name__)
        try:
            if not directory.exists():
                directory.mkdir(parents=True)
                logger.info(f"The directory {directory} was successfully created.")
            else:
                logger.warning(f"The directory {directory} already exists.")

            self.working_directory = directory
            logger.info(f"Working directory set to {directory}!")

        except Exception as e:
            logger.error(f"Error while setting the working directory: {e}")

    def set_log_level(self, log_level: str) -> None:
        """
        Sets the logging level for the application.

        Parameters:
            log_level (str): The log level to set. Options are 'debug', 'info', 'warning', 'error', 'critical'.
        """
        logger = get_logger(__name__)
        if log_level.lower() not in VALID_LOG_LEVELS:
            logger.warning(f"Invalid log level: {log_level}. Using default: {self.log_level}.")
        self.log_level = log_level
