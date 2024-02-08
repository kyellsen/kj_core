import os

# Liste der Tabellennamen
# Use: SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;
table_names = [
    "AntiAbrasionHose",
    "Brand",
    "Cable",
    "Color",
    "ElongationProperties",
    "EndConnection",
    "ExpansionInsert",
    "FiberType",
    "MaterialAdd",
    "MaterialType",
    "Measurement",
    "Producer",
    "Series",
    "ShockAbsorber",
    "Sling",
    "System"
]


def create_python_files(names):
    for name in names:
        # Umwandlung von CamelCase in snake_case
        snake_case_name = ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_') + '.py'

        # Erstellung der Datei
        with open(snake_case_name, 'w') as f:
            # Hier könntest du initialen Inhalt hinzufügen, falls gewünscht
            f.write("# Initialer Inhalt fuer " + name + "\n")


if __name__ == "__main__":
    create_python_files(table_names)
