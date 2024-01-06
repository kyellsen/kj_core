from pathlib import Path
from typing import Optional, Union, List
from typing import Callable

from .log_manager import get_logger

logger = get_logger(__name__)


def get_directory(directory: Union[str, Path]) -> Union[Path, None]:
    """
    Creates a folder at the specified path if it doesn't exist and returns the Path object.

    Args:
        directory (Union[str, Path]): The path to the folder.

    Returns:
        Union[Path, None]: The Path object representing the folder path, or None if an error occurred.
    """
    try:
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.critical(f"Failed to find or create folder, error: {e}")
        return None
    return directory


def validate_and_get_file_list(search_path: Path, file_type: Optional[str] = None) -> Optional[List[Path]]:
    """
    Searches for files in the given path and returns them as a list. If a file type is specified,
    it searches only for files of that type, otherwise, it searches for all files.

    :param search_path: The path in which to search.
    :param file_type: Optional. The type of files to search for (e.g., 'csv').
    :return: List of paths to the found files.
    """
    if file_type:
        file_type = file_type.lower()
        search_pattern = f'**/*.{file_type}'
    else:
        search_pattern = '**/*'

    files = list(search_path.glob(search_pattern))

    if not files:
        logger.warning(f"No files found in path: {search_path}")
        return None

    # Filter the files to include all case variations of the file type
    if file_type:
        files = [f for f in files if f.suffix.lower() == f'.{file_type}']

    logger.info(f"Found files: {[file.stem for file in files]}")
    return files


def extract_last_three_digits(file: Path) -> int:
    return int(file.stem[-3:])


def extract_sensor_id(files: Optional[List[Path]], id_extractor: Callable[[Path], int] = extract_last_three_digits) -> \
        Optional[List[int]]:
    """
    Extracts sensor IDs from the filenames using a provided extraction function and returns them as a list.
    Uses 'extract_last_three_digits' as the default method for extracting sensor IDs.

    :param files: List of file paths.
    :param id_extractor: A function that takes a Path object and returns an integer sensor ID.
    :return: List of sensor IDs, or None in case of an error.
    """
    if files is None:
        return None

    sensor_id_list = []
    for file in files:
        try:
            sensor_id = id_extractor(file)
            sensor_id_list.append(sensor_id)
        except Exception as e:
            logger.error(f"Failed to extract sensor ID from filename {file.name}. Error: {e}")
            return None

    logger.info(f"Extracted sensor IDs: {sensor_id_list}")
    return sensor_id_list
