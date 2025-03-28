# Mein Paket

    ==================  KJ-CORE HELP  ==================

    Überblick:
      Dieses Paket beinhaltet Kernfunktionalitäten rund um:
      - Konfiguration (CoreConfig)
      - Datenbankverwaltung (DatabaseManager)
      - Datenverwaltung (DataManager)
      - Plot-Erstellung (PlotManager)
      - Diverse Hilfsfunktionen in 'utils' (z. B. path_utils, latex_export, runtime_manager).

    Typische Anwendung:
      1. CoreConfig instanzieren:
         from kj_core import CoreConfig
         config = CoreConfig()
         # Legt Arbeitsverzeichnisse, Plot- und Daten-Ordner fest

      2. DatabaseManager instanzieren:
         from kj_core import DatabaseManager
         db_manager = DatabaseManager(config)
         # Verbindet sich mit SQLite, kümmert sich um Session-Handling

      3. DataManager nutzen:
         from kj_core import DataManager
         data_manager = DataManager(config)
         # Lädt, speichert, verwaltet Daten

      4. PlotManager für Visualisierungen:
         from kj_core import PlotManager
         plot_manager = PlotManager(config)
         # Erstellt Standard-Plots mit matplotlib, seaborn oder Plotly

    Hilfsfunktionen (utils):
      - path_utils.get_directory(...) legt automatisch Ordner an.
      - latex_export: Erzeugt LaTeX-Code für Tabellen, Labels usw.
      - runtime_manager.dec_runtime(...) kann zur Laufzeitanalyse genutzt werden.

    Installation und Abhängigkeiten:
      - Stelle sicher, dass alle benötigten Pakete installiert sind
        (z. B. sqlalchemy, matplotlib, seaborn, plotly, slugify).
      - Integriere die 'kj_core'-Module in dein Projekt oder installiere
        sie als eigenes Package mit setup.py/pyproject.toml.

    ==================  ENDE DER HILFE  ==================