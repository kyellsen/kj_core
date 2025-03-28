from pathlib import Path
from typing import Optional

from kj_logger import get_logger

logger = get_logger(__name__)


class CoreConfig:
    """
    Class for managing the core configuration settings across multiple packages.
    Ensures that only one instance of the configuration is active at any time.
    """

    package_name = "kj_core"
    default_working_directory = r"C:\kyellsen\006_Packages\test_working_directory_core_config"

    def __init__(self, working_directory: Optional[str] = None) -> None:
        """
        Initializes the configuration settings. This method is executed only once.

        Parameters:
            working_directory (Optional[str]): The path to the working directory. Defaults to a predefined path.
        """
        self.working_directory = Path()
        self.set_working_directory(
            working_directory if working_directory is not None else self.default_working_directory)

        self.plot_directory = self.working_directory / "plots"
        self.data_directory = self.working_directory / "data"
        self.database_directory = self.working_directory / "databases"
        logger.info(f"{self} initialized! Code: 001")

    def __repr__(self) -> str:
        """
        Returns a detailed string representation of the CoreConfig instance.
        """
        return (
            f"<CoreConfig>\n"
            f"  Package:            {self.package_name}\n"
            f"  Working Directory:  {self.working_directory}\n"
            f"  Plot Directory:     {self.plot_directory}\n"
            f"  Data Directory:     {self.data_directory}\n"
            f"  Database Directory: {self.database_directory}\n"
        )

    def set_working_directory(self, directory: str) -> None:
        """
        Sets the working directory to the specified path.

        Parameters:
            directory (Path): The directory path to set as the working directory.
        """
        directory = Path(directory)

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


