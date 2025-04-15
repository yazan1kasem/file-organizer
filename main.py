#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
KI-basierte Dateiverwaltungsanwendung
-------------------------------------

Eine intelligente Anwendung zur Organisation, Analyse und Verwaltung von Dateien.
"""

import sys
import os
import logging
from PyQt6.QtWidgets import QApplication

# Konfiguration des Logging-Systems
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("file_organizer")


def setup_environment():
    """Richtet die Umgebung für die Anwendung ein."""
    # Erstelle Verzeichnisse, falls sie nicht existieren
    os.makedirs("plugins", exist_ok=True)
    os.makedirs("plugins/config", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    # Füge Projektverzeichnis zum Pfad hinzu
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    logger.info("Umgebung eingerichtet")


def main():
    """Hauptfunktion der Anwendung."""
    logger.info("Starte KI-basierte Dateiverwaltungsanwendung")

    # Richte Umgebung ein
    setup_environment()

    try:
        # Importiere Module
        from src.file_analyzer import FileAnalyzer
        from src.duplicate_detector import DuplicateDetector
        from src.file_manager import FileManager
        from src.smart_file_manager import SmartFileManager
        from src.plugin_system import PluginManager
        from src.ui.main_window import FileOrganizerUI

        # Initialisiere QApplication
        app = QApplication(sys.argv)

        # Initialisiere Kernmodule
        file_analyzer = FileAnalyzer()
        duplicate_detector = DuplicateDetector()
        file_manager = FileManager()
        smart_file_manager = SmartFileManager()

        # Initialisiere Plugin-System
        plugin_manager = PluginManager(["plugins"])

        # Erstelle Anwendungskontext
        app_context = {
            "file_analyzer": file_analyzer,
            "duplicate_detector": duplicate_detector,
            "file_manager": file_manager,
            "smart_file_manager": smart_file_manager,
            "plugin_manager": plugin_manager,
            "app_version": "0.1.0"
        }

        # Setze Anwendungskontext für Plugin-Manager
        plugin_manager.set_app_context(app_context)

        # Entdecke und registriere Plugins
        discovered_plugins = plugin_manager.discover_plugins()
        logger.info(f"Gefundene Plugins: {discovered_plugins}")

        for plugin_name in discovered_plugins:
            plugin_manager.register_plugin(plugin_name)

        # Erstelle Hauptfenster
        main_window = FileOrganizerUI()

        # Füge Hauptfenster zum Anwendungskontext hinzu
        app_context["main_window"] = main_window

        # Zeige Hauptfenster
        main_window.show()

        # Starte Ereignisschleife
        sys.exit(app.exec())

    except Exception as e:
        logger.error(f"Fehler beim Starten der Anwendung: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
