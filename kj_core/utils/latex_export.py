from pathlib import Path
from slugify import slugify
import pandas as pd
from typing import Optional


def create_caption(caption: str, caption_long: str = None) -> str:
    """
    Create a LaTeX caption string using short and optional long form.

    Parameters:
        caption (str): The short caption for the table.
        caption_long (str, optional): The long caption for the table. Defaults to None.

    Returns:
        str: The LaTeX caption string.
    """
    if caption_long:
        return f"\\caption[{caption}]{{{caption_long}}}"
    return f"\\caption{{{caption}}}"


def create_label(caption: str, additional_label: str = None) -> str:
    """
    Create a LaTeX label string, optionally extended with an additional label.

    Parameters:
        caption (str): The short caption for the table.
        additional_label (str, optional): Additional text to append to the label. Defaults to None.

    Returns:
        str: The LaTeX label string.
    """
    label_clean = slugify(caption, separator="_")
    if additional_label:
        additional_label_clean = slugify(additional_label, separator="_")
        return f"{label_clean}_{additional_label_clean}"
    return label_clean


def generate_latex_table(latex_string: str, caption_text: str, label_clean: str) -> str:
    """
    Generate a LaTeX table string with the provided content, captions, and label.

    Parameters:
        latex_string (str): The LaTeX string of the table.
        caption_text (str): The LaTeX caption string.
        label_clean (str): The LaTeX label string.

    Returns:
        str: The complete LaTeX table string.
    """
    return f"""
    \\begin{{table}}[h]
        \\centering
        {caption_text}
        \\begin{{adjustbox}}{{max width=\\linewidth, max height=\\textheight}}
        {latex_string}
        \\end{{adjustbox}}
        \\label{{tab:{label_clean}}}
    \\end{{table}}
    """


def save_to_file(content: str, file_path: Path) -> None:
    """
    Save the given content to a specified file.

    Parameters:
        content (str): The content to save.
        file_path (Path): The file path where the content should be saved.

    Returns:
        None
    """
    file_path.write_text(content.strip(), encoding="utf-8")
    print(f"Content saved to: {file_path}")


def save_latex_table(latex_string: str, caption: str, latex_export_directory: Path, caption_long: str = None,
                     additional_label: str = None) -> None:
    """
    Save a LaTeX table to the specified directory.

    Parameters:
        latex_string (str): The LaTeX string of the table.
        caption (str): The short caption for the table.
        latex_export_directory (Path): Path object for the export directory.
        caption_long (str, optional): The long caption for the table. Defaults to None.
        additional_label (str, optional): Additional text to append to the label. Defaults to None.

    Returns:
        None
    """
    try:
        label_clean = create_label(caption, additional_label)
        caption_text = create_caption(caption, caption_long)
        latex_table = generate_latex_table(latex_string, caption_text, label_clean)
        latex_path = latex_export_directory / f"{label_clean}.tex"
        save_to_file(latex_table, latex_path)
    except Exception as e:
        print(f"Error saving LaTeX table: {e}")


def build_data_dict_df(
    data_dict: dict,
    keys: Optional[list[str]] = None,
    index_name: str = "Variable",
    escape_index: bool = False,
    select_latex_fields: bool = False
) -> pd.DataFrame:
    """
    Build a structured DataFrame from a nested dictionary, optionally formatted for LaTeX output.

    Parameters:
        data_dict (dict): Nested dictionary with field information.
        keys (list[str], optional): Keys to extract. Defaults to all keys in data_dict.
        index_name (str): Name of the column where the dictionary keys are stored. Default: "Variable".
        escape_index (bool): If True and `select_latex_fields=True`, escapes underscores in index for LaTeX.
        select_latex_fields (bool): If True, filters and reorders columns for LaTeX-ready output.

    Returns:
        pd.DataFrame: Structured DataFrame.

    Raises:
        ValueError: For missing fields or invalid input structures.
    """
    if not isinstance(data_dict, dict):
        raise ValueError("Input must be a dictionary.")

    try:
        if keys is None:
            keys = list(data_dict.keys())

        missing_keys = [k for k in keys if k not in data_dict]
        if missing_keys:
            raise ValueError(f"Keys not found in data_dict: {missing_keys}")

        filtered_dict = {k: data_dict[k] for k in keys}
        df = pd.DataFrame.from_dict(filtered_dict, orient="index")

        # Insert key column with optional LaTeX escaping
        index_values = [
            k.replace("_", "\\_") if escape_index and select_latex_fields else k
            for k in df.index
        ]
        df[index_name] = index_values

        # Reorder columns to place index_name first
        df.reset_index(drop=True, inplace=True)
        cols = [index_name] + [col for col in df.columns if col != index_name]
        df = df[cols]

        # If LaTeX export is selected, validate and reduce columns
        if select_latex_fields:
            required_fields = ["Zeichen", index_name, "Deutsch", "Einheit", "Beschreibung"]
            missing_fields = [f for f in required_fields if f not in df.columns]
            if missing_fields:
                raise ValueError(f"Missing fields for LaTeX export: {missing_fields}")
            df = df[required_fields]

        return df

    except Exception as e:
        raise ValueError(f"Failed to build DataFrame: {e}")

