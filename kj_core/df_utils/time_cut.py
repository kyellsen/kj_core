import pandas as pd

from datetime import datetime
from typing import Union


from datetime import datetime
from typing import Union

def validate_time_format(time_str: str, additional_formats: list = None) -> Union[str, ValueError]:
    """
    Validates and converts an input time string to a specified format ("%Y-%m-%d %H:%M:%S.%f"),
    supporting additional custom formats.

    Parameters:
    -----------
    time_str : str
        The time string to validate and convert.
    additional_formats : list, optional
        A list of additional time string formats to try parsing.

    Returns:
    --------
    Union[str, ValueError]
        The time string converted to the specified format if validation is successful;
        otherwise, a ValueError.
    """
    target_format = "%Y-%m-%d %H:%M:%S.%f"
    known_formats = [
        "%Y-%m-%d %H:%M:%S.%f",  # With microseconds
        "%Y-%m-%d %H:%M:%S",     # Without microseconds
        "%Y-%m-%dT%H:%M:%S",     # ISO 8601 without microseconds
        "%Y-%m-%dT%H:%M:%S.%f"   # ISO 8601 with microseconds
    ]

    # Extend known formats with any additional formats provided
    if additional_formats:
        known_formats.extend(additional_formats)

    for fmt in known_formats:
        try:
            # Attempt to parse the time string using the current format
            parsed_time = datetime.strptime(time_str, fmt)
            # If successful, return the time string in the target format
            return parsed_time.strftime(target_format)
        except ValueError:
            # If parsing fails, continue to the next format
            continue

    # If none of the formats match, return a ValueError
    return ValueError(f"Time string '{time_str}' does not match any known formats.")


def time_cut_by_datetime_index(data: pd.DataFrame, start_time: str, end_time: str) -> pd.DataFrame:
    """
    Returns a Pandas DataFrame that is limited to the specified time range,
    using the DataFrame's datetime index.

    Parameters:
    -----------
    data : pandas DataFrame
        The original data frame with a datetime index.

    start_time : str
        Start time in the format 'yyyy-mm-dd hh:mm:ss'.

    end_time : str
        End time in the format 'yyyy-mm-dd hh:mm:ss'.

    Returns:
    --------
    pandas DataFrame
        A new Pandas DataFrame that contains only rows within the specified
        time range, maintaining the original datetime index.
    """
    # Stellen Sie sicher, dass der Index ein Datumszeit-Index ist
    if not isinstance(data.index, pd.DatetimeIndex):
        raise ValueError("DataFrame index must be of type DatetimeIndex.")

    # Begrenzen Sie die Daten auf den spezifizierten Zeitbereich
    data_limited = data.loc[start_time:end_time]

    return data_limited
