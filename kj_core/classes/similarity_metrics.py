from typing import Dict, Union
import pandas as pd
import numpy as np
from scipy.stats import pearsonr
from sklearn.metrics import mean_squared_error, mean_absolute_error
from dataclasses import dataclass


# Assuming logger is defined earlier in the script
# logger = logging.getLogger(__name__)

@dataclass
class SimilarityMetrics:
    pearson_r: float
    p_value: float
    rmse: float
    mae: float

    def to_dict(self) -> Dict:
        return self.__dict__


def calculate_similarity_metrics(series1: pd.Series, series2: pd.Series) -> SimilarityMetrics:
    """
    Calculates similarity metrics between two time series, handling NaN values.

    Parameters:
    - series1 (pd.Series): First time series.
    - series2 (pd.Series): Second time series.

    Returns:
    - SimilarityMetrics: An object containing the Pearson correlation coefficient,
      p-value, Root Mean Square Error, and Mean Absolute Error.

    Raises:
    - ValueError: If either series contains NaN values.
    """
    if series1.isnull().any() or series2.isnull().any():
        raise ValueError("Input series must not contain NaN values.")

    pearson_r, p_value = pearsonr(series1, series2)
    rmse = np.sqrt(mean_squared_error(series1, series2))
    mae = mean_absolute_error(series1, series2)

    return SimilarityMetrics(pearson_r, p_value, rmse, mae)
