from typing import Optional
from ..utils.base import Base
from ..utils.log_manager import get_logger
from kj_core import CoreConfig, DataManager, DatabaseManager, PlotManager

logger = get_logger(__name__)


class CoreBaseClass(Base):
    """
    Core base class providing basic functionality for managing different components.

    This class is intended to be used as a base class for more specific implementations
    that require a CoreConfig configuration and optional DataManager, DatabaseManager, and PlotManager components.

    Attributes:
        CONFIG (CoreConfig): Configuration object.
        DATA_MANAGER (Optional[DataManager]): An optional data manager component.
        DATABASE_MANAGER (Optional[DatabaseManager]): An optional database manager component.
        PLOT_MANAGER (Optional[PlotManager]): An optional plot manager component.
    """

    __abstract__ = True

    def __init__(self, config: CoreConfig, data_manager: Optional[DataManager] = None,
                 database_manager: Optional[DatabaseManager] = None, plot_manager: Optional[PlotManager] = None):
        """
        Initialize the CoreBaseClass with required CoreConfig configuration and optional manager components.

        Args:
            config (CoreConfig): A required CoreConfig configuration object.
            data_manager (Optional[DataManager]): An optional data manager. Default is None.
            database_manager (Optional[DatabaseManager]): An optional database manager. Default is None.
            plot_manager (Optional[PlotManager]): An optional plot manager. Default is None.

        Raises:
            ValueError: If 'config' is None, indicating improper initialization.
        """
        super().__init__()
        if config is None:
            raise ValueError("Config is None. The package has not been properly initialized. "
                             "Please call the setup function with a valid configuration.")

        self.CONFIG = config

        if data_manager is not None:
            self.DATA_MANAGER = data_manager
        if database_manager is not None:
            self.DATABASE_MANAGER = database_manager
        if plot_manager is not None:
            self.PLOT_MANAGER = plot_manager


