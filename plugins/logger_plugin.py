import logging
import os
import sys
from src.plugin_system import PluginInterface

# Füge Projektverzeichnis zum Pfad hinzu
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Konfiguration des Logging-Systems
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("example_plugin")


class LoggerPlugin(PluginInterface):
    """
    Ein einfaches Plugin zum Loggen von Nachrichten.
    """

    def __init__(self):
        self.name = "LoggerPlugin"
        self.description = "Ein einfaches Plugin zum Loggen von Nachrichten"
        self.version = "0.1.0"
        self.author = "Manus"
        self.logger = logger

    def initialize(self, app_context):
        """
        Initialisiert das Plugin.

        Args:
            app_context (dict): Anwendungskontext.

        Returns:
            bool: True, wenn die Initialisierung erfolgreich war, sonst False.
        """
        self.app_context = app_context
        self.logger.info(f"Logger-Plugin initialisiert mit Kontext: {app_context}")
        return True

    def get_info(self):
        """
        Gibt Informationen über das Plugin zurück.

        Returns:
            dict: Plugin-Informationen.
        """
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "author": self.author
        }

    def execute(self, message="Keine Nachricht angegeben", level="info"):
        """
        Führt die Hauptfunktion des Plugins aus.

        Args:
            message (str): Zu loggende Nachricht.
            level (str): Log-Level (debug, info, warning, error, critical).

        Returns:
            bool: True, wenn das Logging erfolgreich war, sonst False.
        """
        return self.log_message(message, level)

    def log_message(self, message, level="info"):
        """
        Loggt eine Nachricht mit dem angegebenen Level.

        Args:
            message (str): Zu loggende Nachricht.
            level (str): Log-Level (debug, info, warning, error, critical).

        Returns:
            bool: True, wenn das Logging erfolgreich war, sonst False.
        """
        try:
            if level == "debug":
                self.logger.debug(message)
            elif level == "info":
                self.logger.info(message)
            elif level == "warning":
                self.logger.warning(message)
            elif level == "error":
                self.logger.error(message)
            elif level == "critical":
                self.logger.critical(message)
            else:
                self.logger.info(message)

            return True
        except Exception as e:
            self.logger.error(f"Fehler beim Loggen: {e}")
            return False

    def log_debug(self, message):
        """
        Loggt eine Debug-Nachricht.

        Args:
            message (str): Zu loggende Nachricht.

        Returns:
            bool: True, wenn das Logging erfolgreich war, sonst False.
        """
        return self.log_message(message, "debug")

    def log_info(self, message):
        """
        Loggt eine Info-Nachricht.

        Args:
            message (str): Zu loggende Nachricht.

        Returns:
            bool: True, wenn das Logging erfolgreich war, sonst False.
        """
        return self.log_message(message, "info")

    def log_warning(self, message):
        """
        Loggt eine Warnung.

        Args:
            message (str): Zu loggende Nachricht.

        Returns:
            bool: True, wenn das Logging erfolgreich war, sonst False.
        """
        return self.log_message(message, "warning")

    def log_error(self, message):
        """
        Loggt einen Fehler.

        Args:
            message (str): Zu loggende Nachricht.

        Returns:
            bool: True, wenn das Logging erfolgreich war, sonst False.
        """
        return self.log_message(message, "error")

    def log_critical(self, message):
        """
        Loggt einen kritischen Fehler.

        Args:
            message (str): Zu loggende Nachricht.

        Returns:
            bool: True, wenn das Logging erfolgreich war, sonst False.
        """
        return self.log_message(message, "critical")

    def cleanup(self):
        """
        Bereinigt Ressourcen, die vom Plugin verwendet werden.

        Returns:
            bool: True, wenn die Bereinigung erfolgreich war, sonst False.
        """
        self.logger.info("Logger-Plugin bereinigt")
        return True


# Wenn das Skript direkt ausgeführt wird
if __name__ == "__main__":
    # Erstelle Plugin-Instanz
    plugin = LoggerPlugin()

    # Teste Plugin
    plugin.initialize({})
    plugin.log_info("Test-Info-Nachricht")
    plugin.log_warning("Test-Warnung")
    plugin.log_error("Test-Fehler")
    plugin.cleanup()
