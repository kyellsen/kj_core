from typing import List, Dict, Tuple, Optional
import pandas as pd
import numpy as np
from scipy.stats import pearsonr
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from dataclasses import dataclass

@dataclass
class SimilarityMetrics:
    pearson_r: float  # Pearson correlation coefficient
    p_value: float  # p-value of the Pearson correlation
    r2: float  # R-squared, coefficient of determination
    mse: float  # Mean Squared Error
    rmse: float  # Root Mean Squared Error
    nrmse: float  # Normalized RMSE (Normalized Root Mean Squared Error)
    cv: float  # Coefficient of Variation
    mae: float  # Mean Absolute Error
    nmae: float  # Normalized MAE (Normalized Mean Absolute Error)

    def to_dict(self) -> Dict[str, float]:
        """
        Convert the SimilarityMetrics dataclass to a dictionary.

        Returns:
            Dict[str, float]: A dictionary representation of the SimilarityMetrics.
        """
        return self.__dict__

    @classmethod
    def calc(cls, series1: pd.Series, series2: pd.Series) -> "SimilarityMetrics":
        """
        Calculate similarity metrics between two pandas Series.

        Args:
            series1 (pd.Series): The first series of values.
            series2 (pd.Series): The second series of values.

        Returns:
            SimilarityMetrics: An instance of the SimilarityMetrics dataclass containing all the calculated metrics.

        Raises:
            ValueError: If either of the input series contains NaN values.
        """
        if series1.isnull().any() or series2.isnull().any():
            raise ValueError("Input series must not contain NaN values.")

        pearson_r, p_value = pearsonr(series1, series2)
        r2 = r2_score(series1, series2)
        mse = mean_squared_error(series1, series2)
        rmse = np.sqrt(mse)
        nrmse = rmse / (series1.max() - series1.min())
        cv = rmse / series1.mean()
        mae = mean_absolute_error(series1, series2)
        nmae = mae / (series1.max() - series1.min())

        return cls(pearson_r, p_value, r2, mse, rmse, nrmse, cv, mae, nmae)

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
                warnings.append(f"Metric '{metric}' value {metric_value:.4f} outside of threshold range {lower_threshold}-{upper_threshold}")
        return warnings
