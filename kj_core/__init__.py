from .core_config import CoreConfig
from .utils import log_manager
from .utils.log_manager import get_logger
from .utils.database_manager import DatabaseManager
from .utils.data_manager import DataManager
from .utils.plot_manager import PlotManager

logger = get_logger(__name__)

logger.info(f"Setup {CoreConfig.package_name} package!")
