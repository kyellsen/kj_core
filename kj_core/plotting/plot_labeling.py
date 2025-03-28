from typing import Dict
from slugify import slugify


def get_axis_label(
    key: str,
    data_dict: Dict[str, Dict[str, str]]
) -> str:
    """
    Returns formatted axis label using metadata from data_dict.
    """
    einheit = data_dict[key].get("Einheit", key)
    zeichen = data_dict[key].get("Zeichen", key)
    deutsch = data_dict[key].get("Deutsch", key)
    return f"{deutsch} {zeichen} [{einheit}]" if einheit != "-" else f"{deutsch} {zeichen}"


def get_plot_title(
    x_key: str,
    y_key: str,
    data_dict: Dict[str, Dict[str, str]],
    prefix: str = "Regression"
) -> str:
    """
    Returns formatted plot title using metadata from data_dict.
    """
    x_label = data_dict[x_key].get("Deutsch", x_key)
    x_symbol = data_dict[x_key].get("Zeichen", x_key)
    y_label = data_dict[y_key].get("Deutsch", y_key)
    y_symbol = data_dict[y_key].get("Zeichen", y_key)
    return f"{prefix}: {y_label} ({y_symbol}) vs. {x_label} ({x_symbol})"


def get_legend_title(
    key: str,
    data_dict: Dict[str, Dict[str, str]]
) -> str:
    """
    Returns the legend label using the 'Deutsch' field.
    """
    return data_dict[key].get("Deutsch", key)


def get_filename(
    x_key: str,
    y_key: str,
    prefix: str = "plot"
) -> str:
    """
    Returns standardized slugified filename based on axis keys.
    """
    raw_name = f"{prefix}_{y_key}_vs_{x_key}"
    return slugify(raw_name, separator="_")
