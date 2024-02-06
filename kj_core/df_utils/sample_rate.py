import pandas as pd
from typing import Union


def calc_sample_rate(data: Union[pd.DataFrame, pd.Series]) -> float:
    """
    Calculate the sample rate of a pandas DataFrame or Series with a DatetimeIndex.

    Parameters:
        data (Union[pd.DataFrame, pd.Series]): The data with a DatetimeIndex.

    Returns:
        float: The sample rate in Hz (samples per second).

    Raises:
        ValueError: If data does not have a DatetimeIndex.
    """
    # Verify the data has a DatetimeIndex
    if not isinstance(data.index, pd.DatetimeIndex):
        raise ValueError("Data must have a DatetimeIndex.")

    # Calculate the differences between consecutive timestamps
    time_deltas = data.index.to_series().diff().dt.total_seconds()

    # Compute the average period between samples in seconds
    average_period_seconds = time_deltas.mean()

    # Guard against division by zero when calculating sample rate
    if average_period_seconds <= 0:
        raise ValueError("Cannot calculate sample rate with invalid average period.")

    # Calculate and return sample rate in Hz
    sample_rate_hz = 1 / average_period_seconds

    return sample_rate_hz
