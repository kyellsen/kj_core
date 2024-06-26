import pandas as pd
from pathlib import Path
from sqlalchemy import orm
from datetime import datetime
from typing import Optional

from kj_logger import get_logger

logger = get_logger(__name__)

from kj_core.utils.runtime_manager import dec_runtime


class CoreDataClass:

    def __init__(self, data_id: int = None, data: pd.DataFrame = None, data_filepath: str = None,
                 data_changed: bool = False, datetime_added: datetime = None, datetime_last_edit: datetime = None):
        self.data_id = data_id
        self._data = None
        self.data = data
        self.data_filepath = data_filepath if data_filepath else None
        self.data_changed = data_changed

        # For datetime_added and datetime_last_edit, using current datetime if not provided
        self.datetime_added = datetime_added if datetime_added is not None else datetime.now()
        self.datetime_last_edit = datetime_last_edit if datetime_last_edit is not None else datetime.now()

    @orm.reconstructor
    def _init_on_load(self):
        # Diese Methode wird vom SQLAlchemy ORM nach dem Laden einer Instanz aufgerufen
        self._data = None

    @property
    def data(self) -> Optional[pd.DataFrame]:
        """Gets the data."""
        if self._data is None and self.data_filepath:
            self.read_data_feather()
            if hasattr(self, 'validate_data'):  # Prüfen, ob validate_data existiert
                self.validate_data()  # validate_data aufrufen, wenn vorhanden
        return self._data

    @data.setter
    def data(self, new_data: Optional[pd.DataFrame]) -> None:
        """
        Sets new data to the object, marking it as changed if it differs from the current data.

        Parameters:
            new_data (Optional[pd.DataFrame]): The new data to be set. Can be None.

        Raises:
            ValueError: If new_data is neither a pandas DataFrame nor None.
        """
        if new_data is not None and not isinstance(new_data, pd.DataFrame):
            raise ValueError(f"Provided data must be a pandas DataFrame or None, not type: {type(new_data)}")

        if self._data is None and new_data is None:
            logger.debug("@data.setter: No update required as both current and new data are None.")
        elif self._data is None or not self._data.equals(new_data):
            self._data = new_data
            self.datetime_last_edit = datetime.now()
            self.data_changed = True
            logger.debug(
                f"@data.setter: {self.__class__.__name__}._data updated and marked as changed: data_changed = '{self.data_changed}'")
        else:
            logger.debug("@data.setter: No data update required as the provided data is identical to the current data.")

    # @dec_runtime
    def read_data_feather(self) -> Optional[pd.DataFrame]:
        """
        Reads data from a feather file specified in the `data_filepath` attribute.

        This method attempts to read a DataFrame from a feather file. If `data_filepath`
        is not set or the file cannot be read, appropriate errors are logged.

        Returns:
            Optional[pd.DataFrame]: A pandas DataFrame if the file is successfully read,
                                    or None if there's an error or if `data_filepath` is not set.
        """
        try:
            # Checking if data_filepath is set and file exists
            file_path = Path(self.data_filepath)
            if not file_path.exists():
                logger.error(f"File does not exist at path: {self.data_filepath}")
                return None

            # Reading data from feather file
            self._data = pd.read_feather(file_path)
            logger.debug(f"Data successfully read from {self.data_filepath}")
            return self._data

        except TypeError:
            logger.error("Data file path is not set.")
        except (FileNotFoundError, pd.errors.EmptyDataError) as e:
            logger.error(f"Error with file at {self.data_filepath}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error reading data from {self.data_filepath}: {e}")

        return None

    # @dec_runtime
    def write_data_feather(self) -> None:
        """
        Writes the DataFrame stored in self._data to a feather file at self.data_filepath.

        This method creates the necessary directories and writes the DataFrame to a feather file.
        If self.data_filepath is not set, the method logs an error.

        Returns:
            None
        """
        try:
            if not self.data_filepath:
                raise ValueError("Data file path is not set.")

            # Ensure the directory exists
            Path(self.data_filepath).parent.mkdir(parents=True, exist_ok=True)

            # Save the data to a Feather file
            self._data.to_feather(self.data_filepath)
            logger.debug(f"Data successfully written to {self.data_filepath}")

        except ValueError as e:
            logger.error(e)
        except Exception as e:
            logger.error(f"Unexpected error when writing data to {self.data_filepath}: {e}")

    # @dec_runtime
    def delete_data_feather(self) -> None:
        """
        Deletes the feather file located at self.data_filepath.

        This method removes the feather file if it exists.
        If self.data_filepath is not set, the method logs an error.

        Returns:
            None
        """
        try:
            if not self.data_filepath:
                raise ValueError("Data file path is not set.")

            file_path = Path(self.data_filepath)

            if file_path.exists():
                file_path.unlink()
                logger.debug(f"Data file successfully deleted at {self.data_filepath}")
            else:
                logger.warning(f"No file to delete at {self.data_filepath}")

        except ValueError as e:
            logger.error(e)
        except Exception as e:
            logger.error(f"Unexpected error when deleting data file at {self.data_filepath}: {e}")

    @property
    def datetime_start(self):
        if self.data is not None:
            return self.data.index.min()
        return None

    @property
    def datetime_end(self):
        if self.data is not None:
            return self.data.index.max()
        return None

    @property
    def duration(self):
        if self.datetime_start and self.datetime_end:
            return (self.datetime_end - self.datetime_start).total_seconds()
        return None

    @property
    def length(self):
        if self.data is not None:
            return len(self.data)
        return None
