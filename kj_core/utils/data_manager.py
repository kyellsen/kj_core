from pathlib import Path

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

