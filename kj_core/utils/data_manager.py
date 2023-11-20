from ..utils.log_manager import get_logger

logger = get_logger(__name__)


class DataManager:
    def __init__(self, config):
        """
        Initialize a DataManager object.
        """
        self.data_directory = config.data_directory
        self.data_directory.mkdir(parents=True, exist_ok=True)
