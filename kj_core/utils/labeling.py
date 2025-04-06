from typing import List, Tuple, Dict
import pandas as pd


def get_label_from_dict(key: str, data_dict: Dict[str, Dict[str, str]],
                        template: str = "{Deutsch}",
                        use_full: bool = False,
                        use_axes: bool = False,
                        use_titel: bool = False) -> str:
    """
    Gibt eine formatierte Beschriftung für einen Variablennamen zurück,
    basierend auf einem Daten-Dokumentations-Dictionary.

    Parameters:
        key (str): Variablenname im Datensatz (z. B. "release_force_target").
        data_dict (Dict[str, Dict[str, str]]): Dokumentations-Wörterbuch mit Einträgen zu den Variablen.
        template (str): Standard-Formatstring mit Platzhaltern wie "{Deutsch}", "{Zeichen}", "{Einheit}" etc.
        use_full (bool): Falls True, wird das Template auf "{Deutsch} {Zeichen} [{Einheit}]" gesetzt.
        use_axes (bool): Falls True, wird das Template auf "{Zeichen} [{Einheit}]" gesetzt.
        use_titel (bool): Falls True, wird das Template auf "{Deutsch} {Zeichen}" gesetzt.

    Returns:
        str: Formatierte Beschriftung oder einen Platzhalter, falls der Schlüssel fehlt.
    """
    try:
        eintrag = data_dict[key]
        # Prioritätsreihenfolge der Templates: use_full > use_axes > use_titel > übergebenes template
        if use_full:
            chosen_template = "{Deutsch} {Zeichen} [{Einheit}]"
        elif use_axes:
            chosen_template = "{Zeichen} [{Einheit}]"
        elif use_titel:
            chosen_template = "{Deutsch} {Zeichen}"
        else:
            chosen_template = template

        return chosen_template.format(**eintrag)
    except KeyError:
        return f"[Unbekannt: {key}]"
    except Exception as e:
        return f"[Fehler bei {key}: {e}]"

def get_color_dict(
    df: pd.DataFrame,
    variable: str,
    color_palette: List[Tuple[float, float, float]]
) -> Dict[str, Tuple[float, float, float]]:
    """
    Weist den Kategorien der angegebenen Spalte (variable) Farben aus der übergebenen Farbpalette zu.

    Parameter:
      df (pd.DataFrame): DataFrame, der die Daten enthält.
      variable (str): Name der Spalte, die als kategorische Variable vorliegt.
      color_palette (List[Tuple[float, float, float]]): Liste von Farben, aus der die Zuordnung erfolgt.
           Jede Farbe ist als RGB-Tupel (drei Float-Werte) repräsentiert.

    Rückgabe:
      Dict[str, Tuple[float, float, float]]: Ein Dictionary, in dem jeder Kategorie die entsprechende Farbe zugeordnet wird.
    """
    # Abrufen der Kategorien der gegebenen Spalte
    categories = df[variable].cat.categories
    print(categories)

    # Zuordnen der Farben aus der Palette an die Kategorien
    color_dict = {category: color for category, color in zip(categories, color_palette[:len(categories)])}

    return color_dict
