import logging
from datetime import datetime

LOG_LEVELS = {
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG,
}


class ColorfulFormatter(logging.Formatter):
    COLOR_CODES = {
        logging.CRITICAL: '\033[91m',  # Red
        logging.ERROR: '\033[91m',  # Red
        logging.WARNING: '\033[93m',  # Yellow
        logging.INFO: '\033[92m',  # Green
        logging.DEBUG: '\033[94m',  # Blue
    }

    RESET_CODE = '\033[0m'

    def format(self, record):
        color_code = self.COLOR_CODES.get(record.levelno, self.RESET_CODE)
        record.levelname = f"{color_code}{record.levelname}{self.RESET_CODE}"
        return super().format(record)


def configure_logger(config):
    SAVE_LOGS_TO_FILE = config.save_logs_to_file
    log_directory = config.log_directory
    if SAVE_LOGS_TO_FILE:
        log_directory.mkdir(parents=True, exist_ok=True)

    log_level = config.log_level
    log_level = LOG_LEVELS.get(log_level.lower(), logging.INFO)

    log_format = "%(asctime)s [%(levelname)s] %(name)s.%(funcName)s: %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColorfulFormatter(log_format, datefmt=date_format))

    handlers = [console_handler]

    if SAVE_LOGS_TO_FILE:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file = log_directory / f"{config.package_name}_log_{timestamp}.txt"
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))
        handlers.append(file_handler)

    logging.basicConfig(
        level=log_level,
        handlers=handlers,
    )


def get_logger(name):
    return logging.getLogger(name)
