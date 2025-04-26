from pathlib import Path
from slugify import slugify
import pandas as pd
from typing import Optional, List


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
    \\begin{{table}}[h!]
        \\centering
        {caption_text}
        \\begin{{adjustbox}}{{max width=\\linewidth, max height=0.9\\textheight}}
        {latex_string}
        \\end{{adjustbox}}
        \\label{{tab:{label_clean}}}
    \\end{{table}}
    """


def generate_grouped_latex_tables(df_latex: pd.DataFrame, caption: str, column_format: str, group_by: str, latex_export_directory: Path) -> None:
    """
    Generate grouped LaTeX tables for each unique value in a specified column of a DataFrame.

    Parameters:
        df_latex (pd.DataFrame): The DataFrame with already formatted columns.
        caption (str): The caption for the LaTeX tables.
        column_format (str): The format for the LaTeX tables.
        group_by (str): The column name to group by.
        latex_export_directory (Path): The directory to save the LaTeX tables.

    Returns:
        None
    """
    try:
        # DataFrame grouped by specified column
        grouped = df_latex.groupby(group_by, observed=True)

        # LaTeX tables to be combined in a single file
        combined_tables = []

        for group, group_df in grouped:
            # Drop the group_by column
            group_df = group_df.drop(columns=[group_by])

            # Format 'id' column as string if it exists
            if 'ID' in group_df.columns:
                group_df['ID'] = group_df['ID'].astype(str)

            # Calculate statistics
            mean_row = group_df.mean(numeric_only=True).rename('Mean')
            median_row = group_df.median(numeric_only=True).rename('Median')
            sd_row = group_df.std(numeric_only=True).rename('SD')

            # Combine stats with original DataFrame
            stats_df = pd.concat([group_df, mean_row.to_frame().T, median_row.to_frame().T, sd_row.to_frame().T])

            # Generate LaTeX string from DataFrame
            df_latex_string = stats_df.to_latex(
                index=True,
                escape=False,
                column_format=column_format,
                float_format="{:0.2f}".format
            )

            # Create caption and label for the group
            caption_text = create_caption(caption, f"{caption} für {slugify(str(group), separator=' ')}")
            label_clean = create_label(caption=caption, additional_label=str(group))

            # Generate LaTeX table
            latex_table = generate_latex_table(df_latex_string, caption_text, label_clean)

            combined_tables.append(latex_table)

        # Combine all tables and save to a single file
        if combined_tables:
            final_output = "\n\n".join(combined_tables)
            file_name = create_label(caption) + ".tex"
            save_to_file(final_output, latex_export_directory / file_name)

    except Exception as e:
        print(f"Error generating grouped LaTeX tables: {e}")


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

import pandas as pd
from typing import List, Optional


def grouped_describe(
    df: pd.DataFrame,
    group_by: str,
    cols: Optional[List[str]] = None,
    stats: Optional[List[str]] = None,
    include_overall: bool = False,
    overall_label: str = "Alle",
    stats_label: str = "Statistik",
) -> pd.DataFrame:
    """
    Gruppiertes `describe()` mit Original‑Gruppenreihenfolge
    + optionaler Gesamtzeile und frei benennbarer Statistik‑Ebene.

    Gibt einen DataFrame zurück mit
        Index 0 : Gruppen (Reihenfolge wie im DF bzw. Categorical)
        Index 1 : <stats_label> (count, mean, …)
        Spalten : Variablen
    """
    # --- Grundchecks -------------------------------------------------------
    if group_by not in df.columns:
        raise KeyError(f"Gruppierungs‑Spalte '{group_by}' fehlt.")

    if cols is None:
        cols = df.select_dtypes("number").columns.tolist()

    if stats is None:                   # Standard‑Kennzahlen von describe()
        stats = ["count", "mean", "std", "min",
                 "25%", "50%", "75%", "max"]

    # --- Beschreibende Statistik ------------------------------------------
    g_desc = (
        df.groupby(group_by, sort=False, dropna=False, observed=False)[cols]
          .describe()
    )

    g_fmt = (
        g_desc.swaplevel(axis=1)             # (stat, var)
               .stack(level=0, future_stack=True)               # 'stat' → Zeilen‑Index
    )
    g_fmt.index.set_names([group_by, stats_label], inplace=True)

    # nur angeforderte Kennzahlen & Reihenfolge sichern
    g_fmt = g_fmt.loc[pd.IndexSlice[:, stats], :]

    parts = [g_fmt]

    # --- Gesamtzeile -------------------------------------------------------
    if include_overall:
        overall = (
            df[cols].describe()
              .loc[stats]
        )
        overall.index.name = stats_label
        overall.index = pd.MultiIndex.from_product(
            [[overall_label], overall.index],
            names=[group_by, stats_label],
        )
        parts.append(overall)

    result = pd.concat(parts)

    # --- Endgültige Reihenfolge festnageln --------------------------------
    # 1) Gruppenreihenfolge: ordered‑Categorical → Kategorien,
    #    sonst First‑Appearance‑Reihenfolge
    if isinstance(df[group_by], pd.CategoricalDtype) and \
       df[group_by].cat.ordered:
        group_order = df[group_by].cat.categories.tolist()
    else:
        group_order = df[group_by].drop_duplicates().tolist()

    if include_overall:
        group_order += [overall_label]

    # 2) Vollständiger MultiIndex
    full_index = pd.MultiIndex.from_product(
        [group_order, stats],
        names=[group_by, stats_label],
    )
    return result.reindex(full_index)



