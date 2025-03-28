from typing import Dict

from typing import Dict

def get_label_from_dict(key: str, data_dict: Dict[str, Dict[str, str]],
                        template: str = "{Deutsch}", full: bool = False) -> str:
    """
    Gibt eine formatierte Beschriftung für einen Variablennamen zurück,
    basierend auf einem Daten-Dokumentations-Dictionary.

    Parameters:
        key (str): Variablenname im Datensatz (z. B. "release_force_target").
        data_dict (dict): Dokumentations-Wörterbuch mit Einträgen zu den Variablen.
        template (str): Formatstring mit Platzhaltern wie "{Deutsch}", "{Zeichen}", "{Einheit}" etc.
        full_format (bool): Wenn True, wird das Template automatisch auf
                            "{Deutsch} {Zeichen} [{Einheit}]" gesetzt (überschreibt `template`).

    Returns:
        str: Formatierte Beschriftung oder Platzhalter falls key/Eintrag fehlt.
    """
    try:
        eintrag = data_dict[key]
        if full:
            template = "{Deutsch} {Zeichen} [{Einheit}]"
        return template.format(**eintrag)
    except KeyError:
        return f"[Unbekannt: {key}]"
    except Exception as e:
        return f"[Fehler bei {key}: {e}]"
