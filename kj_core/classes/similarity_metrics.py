from typing import List, Dict, Tuple, Optional
import pandas as pd
import numpy as np
from scipy.stats import pearsonr
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from dataclasses import dataclass


@dataclass
class SimilarityMetrics:
    pearson_r: float
    p_value: float
    r2: float
    mse: float
    rmse: float
    mae: float

    def to_dict(self) -> Dict[str, float]:
        return self.__dict__

    @classmethod
    def calc(cls, series1: pd.Series, series2: pd.Series) -> "SimilarityMetrics":
        if series1.isnull().any() or series2.isnull().any():
            raise ValueError("Input series must not contain NaN values.")

        pearson_r, p_value = pearsonr(series1, series2)
        r2 = r2_score(series1, series2)
        mse = mean_squared_error(series1, series2)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(series1, series2)

        return cls(pearson_r, p_value, r2, mse, rmse, mae)

    def check_thresholds(self, metrics_warning: Dict[str, Tuple[Optional[float], Optional[float]]]) -> List[str]:
        """
        Check if metrics exceed the provided warning thresholds.

        Args:
            metrics_warning (Dict[str, Tuple[Optional[float], Optional[float]]]):
                Dictionary where each key is a metric name, and its value is a tuple (lower_threshold, upper_threshold).
                If a metric is outside this range, it returns a list of warnings.

        Returns:
            List[str]: List of warning messages for metrics outside of threshold range.
        """
        warnings = []
        for metric, (lower_threshold, upper_threshold) in metrics_warning.items():
            metric_value = getattr(self, metric, 0)
            if (lower_threshold is not None and metric_value < lower_threshold) or \
               (upper_threshold is not None and metric_value > upper_threshold):
                warnings.append(f"Metric '{metric}' value {metric_value} outside of threshold range {lower_threshold}-{upper_threshold}")
        return warnings

