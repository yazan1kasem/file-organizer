# Plugin-Entwicklungsanleitung

Diese Anleitung erklärt, wie Sie eigene Plugins für die KI-basierte Dateiverwaltungsanwendung entwickeln können.

## Einführung

Das Plugin-System der Anwendung ermöglicht es Ihnen, die Funktionalität zu erweitern, ohne den Kerncode zu ändern. Es gibt zwei Arten von Plugins:

1. **Python-Plugins**: Vollständige Plugins, die in Python geschrieben sind
2. **YAML-Workflows**: Einfachere Plugins, die als YAML-Dateien definiert werden

## Python-Plugins entwickeln

### Grundstruktur

Ein Python-Plugin ist eine Klasse, die von `PluginInterface` erbt. Hier ist ein Grundgerüst:

```python
from src.plugin_system import PluginInterface

class MyPlugin(PluginInterface):
    def __init__(self):
        super().__init__()
        self.name = "MyPlugin"
        self.description = "Beschreibung meines Plugins"
        self.version = "0.1.0"
        self.author = "Ihr Name"
    
    def initialize(self, app_context):
        """
        Wird beim Laden des Plugins aufgerufen.
        
        Args:
            app_context (dict): Anwendungskontext mit Referenzen zu wichtigen Objekten.
            
        Returns:
            bool: True, wenn die Initialisierung erfolgreich war, sonst False.
        """
        self.app_context = app_context
        return True
    
    def execute(self, *args, **kwargs):
        """
        Hauptmethode des Plugins, wird aufgerufen, wenn das Plugin ausgeführt wird.
        
        Returns:
            Any: Ergebnis der Plugin-Ausführung.
        """
        # Implementieren Sie hier Ihre Plugin-Logik
        return {"status": "success", "message": "Plugin ausgeführt"}
    
    def cleanup(self):
        """
        Wird beim Entladen des Plugins aufgerufen.
        
        Returns:
            bool: True, wenn die Bereinigung erfolgreich war, sonst False.
        """
        # Bereinigen Sie hier Ressourcen
        return True
```

### Speicherort

Speichern Sie Ihre Plugin-Datei im Verzeichnis `plugins` mit der Erweiterung `.py`. Der Dateiname (ohne Erweiterung) wird als Plugin-Name verwendet.

### Anwendungskontext

Der Anwendungskontext (`app_context`) enthält Referenzen zu wichtigen Objekten der Anwendung:

- `app_context["plugin_manager"]`: Referenz zum Plugin-Manager
- `app_context["file_analyzer"]`: Referenz zum FileAnalyzer
- `app_context["duplicate_detector"]`: Referenz zum DuplicateDetector
- `app_context["file_manager"]`: Referenz zum FileManager
- `app_context["smart_file_manager"]`: Referenz zum SmartFileManager
- `app_context["main_window"]`: Referenz zum Hauptfenster (wenn verfügbar)

### Beispiel: Dateistatistik-Plugin

Hier ist ein Beispiel für ein Plugin, das Statistiken über Dateien in einem Verzeichnis sammelt:

```python
from src.plugin_system import PluginInterface
import os
from collections import defaultdict

class FileStatisticsPlugin(PluginInterface):
    def __init__(self):
        super().__init__()
        self.name = "FileStatisticsPlugin"
        self.description = "Sammelt Statistiken über Dateien in einem Verzeichnis"
        self.version = "0.1.0"
        self.author = "Plugin-Entwickler"
    
    def initialize(self, app_context):
        self.app_context = app_context
        self.file_analyzer = app_context.get("file_analyzer")
        return self.file_analyzer is not None
    
    def execute(self, directory_path, recursive=False):
        """
        Sammelt Statistiken über Dateien in einem Verzeichnis.
        
        Args:
            directory_path (str): Pfad zum zu analysierenden Verzeichnis.
            recursive (bool): Ob Unterverzeichnisse einbezogen werden sollen.
            
        Returns:
            dict: Statistiken über die Dateien.
        """
        if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
            return {"error": f"Verzeichnis existiert nicht: {directory_path}"}
        
        statistics = {
            "total_files": 0,
            "total_size": 0,
            "file_types": defaultdict(int),
            "largest_file": {"path": "", "size": 0},
            "newest_file": {"path": "", "timestamp": 0}
        }
        
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Überspringe symbolische Links
                if os.path.islink(file_path):
                    continue
                
                try:
                    # Dateiinformationen abrufen
                    file_stat = os.stat(file_path)
                    file_size = file_stat.st_size
                    file_mtime = file_stat.st_mtime
                    
                    # Dateityp bestimmen
                    if self.file_analyzer:
                        file_info = self.file_analyzer.get_file_info(file_path)
                        file_type = file_info.get("file_type", "unknown")
                    else:
                        _, ext = os.path.splitext(file_path)
                        file_type = ext.lower() if ext else "unknown"
                    
                    # Statistiken aktualisieren
                    statistics["total_files"] += 1
                    statistics["total_size"] += file_size
                    statistics["file_types"][file_type] += 1
                    
                    # Größte Datei
                    if file_size > statistics["largest_file"]["size"]:
                        statistics["largest_file"] = {"path": file_path, "size": file_size}
                    
                    # Neueste Datei
                    if file_mtime > statistics["newest_file"]["timestamp"]:
                        statistics["newest_file"] = {"path": file_path, "timestamp": file_mtime}
                
                except Exception as e:
                    print(f"Fehler bei der Analyse von {file_path}: {e}")
            
            # Wenn nicht rekursiv, nach dem ersten Verzeichnis abbrechen
            if not recursive:
                break
        
        # Formatiere Ergebnisse
        statistics["total_size_formatted"] = self._format_size(statistics["total_size"])
        statistics["largest_file"]["size_formatted"] = self._format_size(statistics["largest_file"]["size"])
        
        from datetime import datetime
        if statistics["newest_file"]["timestamp"] > 0:
            statistics["newest_file"]["date"] = datetime.fromtimestamp(
                statistics["newest_file"]["timestamp"]
            ).strftime("%Y-%m-%d %H:%M:%S")
        
        return statistics
    
    def _format_size(self, size_bytes):
        """
        Formatiert eine Größe in Bytes in eine lesbare Form.
        
        Args:
            size_bytes (int): Größe in Bytes.
            
        Returns:
            str: Formatierte Größe.
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024 or unit == 'TB':
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
    
    def cleanup(self):
        self.file_analyzer = None
        return True
```

## YAML-Workflows entwickeln

YAML-Workflows sind einfacher zu erstellen als Python-Plugins und erfordern keine Programmierkenntnisse.

### Grundstruktur

Ein YAML-Workflow hat folgende Struktur:

```yaml
name: Mein Workflow
description: Beschreibung meines Workflows
version: 0.1.0
author: Ihr Name

variables:
  variable1: "Standardwert"
  variable2: 42
  variable3: [1, 2, 3]

steps:
  - name: Erster Schritt
    type: plugin_call
    plugin: plugin_name
    method: execute
    args: ["Argument 1"]
    kwargs:
      param1: "Wert 1"
      param2: $variable1

  - name: Zweiter Schritt
    type: condition
    condition: $variable2 > 10
    if_steps:
      - name: Wenn-Schritt
        type: file_operation
        operation: create_dir
        path: "/pfad/zum/verzeichnis"
    else_steps:
      - name: Sonst-Schritt
        type: plugin_call
        plugin: logger_plugin
        method: log_warning
        args: ["Variable2 ist nicht größer als 10"]

output:
  - variable1
  - variable2
```

### Speicherort

Speichern Sie Ihre Workflow-Datei im Verzeichnis `plugins` mit der Erweiterung `.yaml` oder `.yml`. Der Dateiname (ohne Erweiterung) wird als Workflow-Name verwendet.

### Variablen

Variablen werden im Abschnitt `variables` definiert und können in Schritten mit dem Präfix `$` referenziert werden.

### Schritttypen

#### file_operation

Führt Dateioperationen aus:

```yaml
- name: Datei kopieren
  type: file_operation
  operation: copy
  source: "/pfad/zur/quelldatei"
  target: "/pfad/zur/zieldatei"
```

Unterstützte Operationen:
- `copy`: Kopiert eine Datei
- `move`: Verschiebt eine Datei
- `delete`: Löscht eine Datei oder ein Verzeichnis
- `create_dir`: Erstellt ein Verzeichnis

#### plugin_call

Ruft ein Plugin auf:

```yaml
- name: Plugin aufrufen
  type: plugin_call
  plugin: plugin_name
  method: execute
  args: ["Argument 1", "Argument 2"]
  kwargs:
    param1: "Wert 1"
    param2: $variable1
  output_var: result_variable
```

#### condition

Führt Schritte basierend auf einer Bedingung aus:

```yaml
- name: Bedingung prüfen
  type: condition
  condition: os.path.exists($file_path) and $variable2 > 10
  if_steps:
    - name: Wenn-Schritt
      type: file_operation
      operation: create_dir
      path: "/pfad/zum/verzeichnis"
  else_steps:
    - name: Sonst-Schritt
      type: plugin_call
      plugin: logger_plugin
      method: log_warning
      args: ["Bedingung nicht erfüllt"]
```

#### loop

Führt Schritte mehrfach aus:

```yaml
- name: Schleife über Dateien
  type: loop
  loop_type: for_each
  items: os.listdir($directory)
  item_var: filename
  steps:
    - name: Datei verarbeiten
      type: plugin_call
      plugin: file_processor
      method: process_file
      args: ["$filename"]
```

Unterstützte Schleifentypen:
- `for_each`: Iteriert über eine Liste
- `while`: Führt Schritte aus, solange eine Bedingung erfüllt ist

### Beispiel: Backup-Workflow

Hier ist ein Beispiel für einen Workflow, der Dateien sichert:

```yaml
name: Backup-Workflow
description: Sichert wichtige Dateien in ein Backup-Verzeichnis
version: 0.1.0
author: Workflow-Entwickler

variables:
  source_dir: ""
  backup_dir: ""
  file_extensions: [".txt", ".docx", ".xlsx", ".pdf"]
  max_backups: 5

steps:
  - name: Verzeichnisse prüfen
    type: condition
    condition: os.path.exists($source_dir) and os.path.isdir($source_dir)
    if_steps:
      - name: Backup-Verzeichnis erstellen
        type: file_operation
        operation: create_dir
        path: $backup_dir
    else_steps:
      - name: Fehler ausgeben
        type: plugin_call
        plugin: logger_plugin
        method: log_error
        args: ["Quellverzeichnis existiert nicht oder ist kein Verzeichnis"]

  - name: Backup-Zeitstempel erstellen
    type: plugin_call
    plugin: logger_plugin
    method: execute
    args: ["Erstelle Backup mit Zeitstempel"]
    kwargs:
      level: "info"
    output_var: log_result

  - name: Dateien sichern
    type: loop
    loop_type: for_each
    items: [f for f in os.listdir($source_dir) if any(f.endswith(ext) for ext in $file_extensions)]
    item_var: filename
    steps:
      - name: Datei kopieren
        type: file_operation
        operation: copy
        source: os.path.join($source_dir, $filename)
        target: os.path.join($backup_dir, $filename)

  - name: Alte Backups bereinigen
    type: plugin_call
    plugin: file_cleaner
    method: clean_old_backups
    args: [$backup_dir]
    kwargs:
      max_backups: $max_backups

output:
  - log_result
```

## Hooks verwenden

Hooks ermöglichen es Plugins, auf Ereignisse in der Anwendung zu reagieren.

### In Python-Plugins

```python
def initialize(self, app_context):
    self.app_context = app_context
    plugin_manager = app_context.get("plugin_manager")
    
    if plugin_manager:
        # Hook registrieren
        plugin_manager.register_hook("file_opened", self.on_file_opened)
        plugin_manager.register_hook("file_saved", self.on_file_saved)
    
    return True

def on_file_opened(self, file_path):
    print(f"Datei geöffnet: {file_path}")
    return True

def on_file_saved(self, file_path):
    print(f"Datei gespeichert: {file_path}")
    return True

def cleanup(self):
    plugin_manager = self.app_context.get("plugin_manager")
    
    if plugin_manager:
        # Hooks entfernen
        plugin_manager.unregister_hook("file_opened", self.on_file_opened)
        plugin_manager.unregister_hook("file_saved", self.on_file_saved)
    
    return True
```

### Verfügbare Hooks

Die Anwendung bietet folgende Hooks:

- `file_opened`: Wird ausgelöst, wenn eine Datei geöffnet wird
- `file_saved`: Wird ausgelöst, wenn eine Datei gespeichert wird
- `file_deleted`: Wird ausgelöst, wenn eine Datei gelöscht wird
- `file_moved`: Wird ausgelöst, wenn eine Datei verschoben wird
- `directory_changed`: Wird ausgelöst, wenn das aktuelle Verzeichnis geändert wird
- `analysis_completed`: Wird ausgelöst, wenn eine Dateianalyse abgeschlossen ist
- `duplicates_found`: Wird ausgelöst, wenn Duplikate gefunden wurden
- `organization_completed`: Wird ausgelöst, wenn eine Dateiorganisation abgeschlossen ist

## Benutzeroberfläche erweitern

Plugins können auch die Benutzeroberfläche erweitern.

### Menüeinträge hinzufügen

```python
def initialize(self, app_context):
    self.app_context = app_context
    main_window = app_context.get("main_window")
    
    if main_window:
        # Menüeintrag hinzufügen
        main_window.add_plugin_menu_item(
            "Mein Plugin",
            "Aktion ausführen",
            self.execute
        )
    
    return True
```

### Eigene Dialoge erstellen

```python
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class MyPluginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mein Plugin-Dialog")
        self.setMinimumSize(400, 300)
        
        layout = QVBoxLayout(self)
        
        label = QLabel("Dies ist ein Dialog meines Plugins")
        layout.addWidget(label)
        
        button = QPushButton("OK")
        button.clicked.connect(self.accept)
        layout.addWidget(button)

def execute(self, *args, **kwargs):
    main_window = self.app_context.get("main_window")
    
    if main_window:
        dialog = MyPluginDialog(main_window)
        result = dialog.exec()
        
        if result == QDialog.DialogCode.Accepted:
            return {"status": "success", "message": "Dialog akzeptiert"}
        else:
            return {"status": "cancelled", "message": "Dialog abgebrochen"}
    
    return {"status": "error", "message": "Hauptfenster nicht verfügbar"}
```

## Tipps und Best Practices

### Fehlerbehandlung

Fangen Sie Ausnahmen ab und geben Sie aussagekräftige Fehlermeldungen zurück:

```python
def execute(self, *args, **kwargs):
    try:
        # Plugin-Logik
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

### Logging

Verwenden Sie das Logging-System für Debugging-Informationen:

```python
import logging

def initialize(self, app_context):
    self.app_context = app_context
    self.logger = logging.getLogger(f"plugin.{self.name}")
    self.logger.info(f"Plugin {self.name} initialisiert")
    return True

def execute(self, *args, **kwargs):
    self.logger.debug(f"Plugin {self.name} ausgeführt mit Argumenten: {args}, {kwargs}")
    # Plugin-Logik
    return {"status": "success"}
```

### Konfiguration

Speichern Sie Plugin-Konfigurationen in einer separaten Datei:

```python
import json
import os

def initialize(self, app_context):
    self.app_context = app_context
    
    # Konfigurationsdatei laden
    config_path = os.path.join("plugins", "config", f"{self.name}.json")
    
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"Fehler beim Laden der Konfiguration: {e}")
            self.config = {}
    else:
        self.config = {}
    
    return True

def save_config(self):
    config_dir = os.path.join("plugins", "config")
    os.makedirs(config_dir, exist_ok=True)
    
    config_path = os.path.join(config_dir, f"{self.name}.json")
    
    try:
        with open(config_path, "w") as f:
            json.dump(self.config, f, indent=2)
        return True
    except Exception as e:
        print(f"Fehler beim Speichern der Konfiguration: {e}")
        return False
```

### Ressourcen freigeben

Stellen Sie sicher, dass alle Ressourcen in der `cleanup`-Methode freigegeben werden:

```python
def cleanup(self):
    # Dateien schließen
    if hasattr(self, "file") and self.file:
        self.file.close()
    
    # Verbindungen trennen
    if hasattr(self, "connection") and self.connection:
        self.connection.close()
    
    # Temporäre Dateien löschen
    if hasattr(self, "temp_files"):
        for temp_file in self.temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    return True
```

## Testen von Plugins

### Manuelles Testen

1. Platzieren Sie Ihr Plugin im Verzeichnis `plugins`
2. Starten Sie die Anwendung
3. Überprüfen Sie, ob Ihr Plugin in der Plugin-Liste erscheint
4. Aktivieren Sie Ihr Plugin
5. Testen Sie die Funktionalität

### Automatisiertes Testen

Erstellen Sie Testfälle für Ihr Plugin:

```python
import unittest
from src.plugin_system import PluginManager

class TestMyPlugin(unittest.TestCase):
    def setUp(self):
        self.plugin_manager = PluginManager(["plugins"])
        self.plugin_manager.set_app_context({})
        self.plugin_manager.register_plugin("my_plugin")
        self.plugin = self.plugin_manager.get_plugin("my_plugin")
    
    def tearDown(self):
        self.plugin_manager.unregister_plugin("my_plugin")
    
    def test_plugin_initialization(self):
        self.assertIsNotNone(self.plugin)
        self.assertEqual(self.plugin.name, "MyPlugin")
    
    def test_plugin_execution(self):
        result = self.plugin.execute("test")
        self.assertEqual(result["status"], "success")

if __name__ == "__main__":
    unittest.main()
```

## Veröffentlichen von Plugins

Wenn Sie Ihr Plugin mit anderen teilen möchten:

1. Erstellen Sie eine Readme-Datei mit Beschreibung, Installation und Verwendung
2. Stellen Sie sicher, dass alle Abhängigkeiten dokumentiert sind
3. Testen Sie Ihr Plugin gründlich
4. Veröffentlichen Sie Ihr Plugin in einem Repository oder auf einer Plugin-Plattform

## Häufige Probleme und Lösungen

### Plugin wird nicht erkannt

**Problem**: Das Plugin erscheint nicht in der Plugin-Liste.
**Lösung**: 
- Überprüfen Sie, ob die Datei im richtigen Verzeichnis liegt
- Stellen Sie sicher, dass die Datei die richtige Erweiterung hat (.py oder .yaml/.yml)
- Überprüfen Sie, ob die Klasse von `PluginInterface` erbt
- Prüfen Sie die Konsolenausgabe auf Fehlermeldungen

### Plugin kann nicht initialisiert werden

**Problem**: Das Plugin wird erkannt, kann aber nicht initialisiert werden.
**Lösung**:
- Überprüfen Sie die `initialize`-Methode
- Stellen Sie sicher, dass alle erforderlichen Abhängigkeiten installiert sind
- Prüfen Sie, ob der Anwendungskontext korrekt verwendet wird

### Plugin-Ausführung schlägt fehl

**Problem**: Die `execute`-Methode wirft eine Ausnahme.
**Lösung**:
- Fügen Sie Fehlerbehandlung hinzu
- Überprüfen Sie die Argumente und Parameter
- Prüfen Sie, ob alle erforderlichen Ressourcen verfügbar sind

## Ressourcen

- **Entwicklerdokumentation**: Ausführliche Informationen zur Anwendungsarchitektur finden Sie in der Entwicklerdokumentation (`docs/developer_docs.md`)
- **Beispiel-Plugins**: Im Verzeichnis `plugins` finden Sie Beispiel-Plugins, die als Referenz dienen können
- **API-Dokumentation**: Die API-Dokumentation der Anwendung finden Sie in der Entwicklerdokumentation
