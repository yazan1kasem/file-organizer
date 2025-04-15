# Entwicklerdokumentation: KI-basierte Dateiverwaltungsanwendung

## Systemarchitektur

Die KI-basierte Dateiverwaltungsanwendung ist modular aufgebaut und folgt dem Prinzip der Trennung von Zuständigkeiten. Die Architektur besteht aus mehreren Hauptkomponenten:

### Kernmodule

- **FileAnalyzer**: Analysiert verschiedene Dateitypen und extrahiert Metadaten und Inhaltsvorschauen.
- **DuplicateDetector**: Erkennt Duplikate und ähnliche Dateien basierend auf verschiedenen Vergleichsmethoden.
- **FileManager**: Verwaltet grundlegende Dateioperationen wie Kopieren, Verschieben und Löschen.
- **SmartFileManager**: Implementiert intelligente Dateimanagement-Funktionen wie automatische Gruppierung und Aufräumvorschläge.

### Benutzeroberfläche

- **MainWindow**: Hauptfenster der Anwendung mit Dateiexplorer und Tab-Bereich.
- **FilePreview**: Komponente zur Vorschau verschiedener Dateitypen.
- **DuplicateFinder**: Oberfläche für die Duplikatsuche und -verwaltung.
- **FileOrganizer**: Oberfläche für die intelligente Dateiorganisation.

### Plugin-System

- **PluginInterface**: Basisklasse für alle Plugins.
- **PluginManager**: Verwaltet die Erkennung, Registrierung und Ausführung von Plugins.
- **WorkflowPlugin**: Spezielle Plugin-Implementierung für YAML-Workflows.

## Technologiestack

Die Anwendung verwendet folgende Technologien:

- **Python 3.8+**: Hauptprogrammiersprache
- **PyQt6**: Framework für die Benutzeroberfläche
- **PyYAML**: Für die Verarbeitung von YAML-Dateien
- **Pillow**: Für die Bildverarbeitung
- **python-magic**: Für die Dateityperkennung
- **chardet**: Für die Zeichensatzerkennung
- **numpy**: Für numerische Berechnungen
- **pytest**: Für Tests

## Modulbeschreibungen

### FileAnalyzer

Der `FileAnalyzer` ist verantwortlich für die Analyse verschiedener Dateitypen. Er erkennt den Dateityp und extrahiert relevante Informationen.

#### Hauptmethoden

```python
def get_file_info(self, file_path):
    """
    Gibt grundlegende Informationen über eine Datei zurück.
    
    Args:
        file_path (str): Pfad zur Datei.
        
    Returns:
        dict: Dateiinformationen.
    """
```

```python
def analyze_file(self, file_path):
    """
    Analysiert eine Datei und gibt detaillierte Informationen zurück.
    
    Args:
        file_path (str): Pfad zur Datei.
        
    Returns:
        dict: Analyseergebnisse.
    """
```

#### Unterstützte Dateitypen

Der `FileAnalyzer` unterstützt folgende Dateitypen:

- **Text**: .txt, .md, .csv, .json, .xml, ...
- **Bild**: .jpg, .jpeg, .png, .gif, .bmp, .svg, ...
- **Video**: .mp4, .mkv, .mov, .avi, ...
- **Audio**: .mp3, .wav, .flac, .m4a, ...
- **Dokument**: .pdf, .docx, .odt, ...
- **Code**: .py, .js, .html, .css, .java, ...
- **Tabelle**: .xlsx, .ods, ...
- **Archiv**: .zip, .rar, .7z, .tar.gz, ...
- **Konfiguration**: .yaml, .ini, .env, ...

### DuplicateDetector

Der `DuplicateDetector` ist für die Erkennung von Duplikaten und ähnlichen Dateien zuständig.

#### Hauptmethoden

```python
def are_files_identical(self, file_path1, file_path2):
    """
    Prüft, ob zwei Dateien identisch sind.
    
    Args:
        file_path1 (str): Pfad zur ersten Datei.
        file_path2 (str): Pfad zur zweiten Datei.
        
    Returns:
        bool: True, wenn die Dateien identisch sind, sonst False.
    """
```

```python
def find_duplicates(self, directory, recursive=True):
    """
    Findet Duplikate in einem Verzeichnis.
    
    Args:
        directory (str): Zu durchsuchendes Verzeichnis.
        recursive (bool): Ob Unterverzeichnisse einbezogen werden sollen.
        
    Returns:
        list: Liste von Duplikatgruppen.
    """
```

```python
def find_similar_files(self, directory, similarity_threshold=0.8, recursive=True):
    """
    Findet ähnliche Dateien in einem Verzeichnis.
    
    Args:
        directory (str): Zu durchsuchendes Verzeichnis.
        similarity_threshold (float): Schwellenwert für die Ähnlichkeit (0.0 bis 1.0).
        recursive (bool): Ob Unterverzeichnisse einbezogen werden sollen.
        
    Returns:
        list: Liste von Gruppen ähnlicher Dateien.
    """
```

### SmartFileManager

Der `SmartFileManager` implementiert intelligente Dateimanagement-Funktionen.

#### Hauptmethoden

```python
def analyze_directory_structure(self, directory_path):
    """
    Analysiert die Struktur eines Verzeichnisses und gibt Statistiken zurück.
    
    Args:
        directory_path (str): Pfad zum zu analysierenden Verzeichnis.
        
    Returns:
        dict: Statistiken über die Verzeichnisstruktur.
    """
```

```python
def generate_cleanup_suggestions(self, directory_path):
    """
    Generiert Vorschläge zum Aufräumen eines Verzeichnisses.
    
    Args:
        directory_path (str): Pfad zum zu analysierenden Verzeichnis.
        
    Returns:
        dict: Aufräumvorschläge.
    """
```

```python
def group_files_by_similarity(self, directory_path, similarity_threshold=0.7, max_files=1000):
    """
    Gruppiert Dateien nach Ähnlichkeit.
    
    Args:
        directory_path (str): Pfad zum zu analysierenden Verzeichnis.
        similarity_threshold (float): Schwellenwert für die Ähnlichkeit (0.0 bis 1.0).
        max_files (int): Maximale Anzahl zu analysierender Dateien.
        
    Returns:
        dict: Gruppierte Dateien nach Ähnlichkeit.
    """
```

```python
def auto_organize_directory(self, directory_path, target_directory=None, organization_method="by_type", move_files=False):
    """
    Organisiert ein Verzeichnis automatisch basierend auf einer Methode.
    
    Args:
        directory_path (str): Pfad zum zu organisierenden Verzeichnis.
        target_directory (str, optional): Zielverzeichnis für die organisierten Dateien.
        organization_method (str): Organisationsmethode ("by_type", "by_date", "by_size", "by_content").
        move_files (bool): Ob Dateien verschoben oder kopiert werden sollen.
        
    Returns:
        dict: Ergebnis der Organisationsoperation.
    """
```

### PluginSystem

Das Plugin-System ermöglicht die Erweiterung der Anwendung durch Plugins und Workflows.

#### PluginInterface

```python
class PluginInterface:
    """
    Basisklasse für alle Plugins.
    Alle Plugins müssen diese Klasse erweitern und die erforderlichen Methoden implementieren.
    """
    
    def initialize(self, app_context):
        """
        Initialisiert das Plugin mit dem Anwendungskontext.
        
        Args:
            app_context (dict): Anwendungskontext mit Referenzen zu wichtigen Objekten.
            
        Returns:
            bool: True, wenn die Initialisierung erfolgreich war, sonst False.
        """
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
    
    def execute(self, *args, **kwargs):
        """
        Führt die Hauptfunktion des Plugins aus.
        
        Returns:
            Any: Ergebnis der Plugin-Ausführung.
        """
        raise NotImplementedError("Die execute-Methode muss implementiert werden")
    
    def cleanup(self):
        """
        Bereinigt Ressourcen, die vom Plugin verwendet werden.
        
        Returns:
            bool: True, wenn die Bereinigung erfolgreich war, sonst False.
        """
        return True
```

#### PluginManager

```python
class PluginManager:
    """
    Verwaltet die Erkennung, Registrierung und Ausführung von Plugins.
    """
    
    def discover_plugins(self):
        """
        Sucht nach verfügbaren Plugins in den Plugin-Verzeichnissen.
        
        Returns:
            list: Liste der gefundenen Plugin-Namen.
        """
    
    def load_plugin(self, plugin_name):
        """
        Lädt ein Plugin anhand seines Namens.
        
        Args:
            plugin_name (str): Name des zu ladenden Plugins.
            
        Returns:
            PluginInterface: Plugin-Instanz oder None, wenn das Plugin nicht geladen werden konnte.
        """
    
    def register_plugin(self, plugin_name):
        """
        Registriert ein Plugin anhand seines Namens.
        
        Args:
            plugin_name (str): Name des zu registrierenden Plugins.
            
        Returns:
            bool: True, wenn das Plugin erfolgreich registriert wurde, sonst False.
        """
    
    def execute_plugin(self, plugin_name, *args, **kwargs):
        """
        Führt ein Plugin aus.
        
        Args:
            plugin_name (str): Name des auszuführenden Plugins.
            *args: Positionsargumente für das Plugin.
            **kwargs: Schlüsselwortargumente für das Plugin.
            
        Returns:
            Any: Ergebnis der Plugin-Ausführung oder None, wenn das Plugin nicht ausgeführt werden konnte.
        """
```

## YAML-Workflows

YAML-Workflows ermöglichen die Definition komplexer Arbeitsabläufe ohne Programmierung.

### Struktur eines Workflows

```yaml
name: Beispiel-Workflow
description: Ein einfacher Workflow zur Demonstration des YAML-Workflow-Systems
version: 0.1.0
author: Entwickler

variables:
  source_dir: ""
  target_dir: ""
  file_types: [".txt", ".md", ".pdf"]

steps:
  - name: Verzeichnisse prüfen
    type: condition
    condition: os.path.exists($source_dir) and os.path.exists($target_dir)
    if_steps:
      - name: Verzeichnisse erstellen
        type: file_operation
        operation: create_dir
        path: $target_dir + "/organisiert"
    else_steps:
      - name: Fehler ausgeben
        type: plugin_call
        plugin: logger_plugin
        method: log_error
        args: ["Quell- oder Zielverzeichnis existiert nicht"]

  - name: Dateien organisieren
    type: loop
    loop_type: for_each
    items: os.listdir($source_dir)
    item_var: filename
    steps:
      - name: Datei prüfen
        type: condition
        condition: any(filename.endswith(ext) for ext in $file_types)
        if_steps:
          - name: Datei kopieren
            type: file_operation
            operation: copy
            source: os.path.join($source_dir, $filename)
            target: os.path.join($target_dir, "organisiert", $filename)

output:
  - processed_files
```

### Unterstützte Schritttypen

- **file_operation**: Führt Dateioperationen aus (copy, move, delete, create_dir).
- **plugin_call**: Ruft ein Plugin auf.
- **condition**: Führt Schritte basierend auf einer Bedingung aus.
- **loop**: Führt Schritte mehrfach aus (for_each, while).

## Eigene Plugins entwickeln

### Erstellen eines Python-Plugins

Um ein eigenes Plugin zu erstellen, müssen Sie die `PluginInterface`-Klasse erweitern:

```python
from src.plugin_system import PluginInterface

class MyPlugin(PluginInterface):
    def __init__(self):
        super().__init__()
        self.name = "MyPlugin"
        self.description = "Mein eigenes Plugin"
        self.version = "0.1.0"
        self.author = "Ich"
    
    def initialize(self, app_context):
        self.app_context = app_context
        return True
    
    def execute(self, *args, **kwargs):
        # Implementieren Sie hier Ihre Plugin-Logik
        return {"status": "success", "result": "Plugin ausgeführt"}
    
    def cleanup(self):
        return True
```

Speichern Sie diese Datei als `my_plugin.py` im Verzeichnis `plugins`.

### Erstellen eines YAML-Workflows

Um einen eigenen Workflow zu erstellen, erstellen Sie eine YAML-Datei mit der oben beschriebenen Struktur und speichern Sie sie im Verzeichnis `plugins` mit der Erweiterung `.yaml` oder `.yml`.

## Hooks verwenden

Hooks ermöglichen es Plugins, auf Ereignisse in der Anwendung zu reagieren.

### Registrieren eines Hooks

```python
def my_hook_callback(file_path, *args, **kwargs):
    print(f"Datei wurde geöffnet: {file_path}")
    return True

# In Ihrem Plugin
def initialize(self, app_context):
    self.app_context = app_context
    plugin_manager = app_context.get("plugin_manager")
    if plugin_manager:
        plugin_manager.register_hook("file_opened", my_hook_callback)
    return True
```

### Auslösen eines Hooks

```python
# In der Hauptanwendung
def open_file(self, file_path):
    # Datei öffnen
    # ...
    
    # Hook auslösen
    self.plugin_manager.trigger_hook("file_opened", file_path)
```

## Testen

Die Anwendung verwendet `pytest` für Tests. Die Tests sind in mehrere Kategorien unterteilt:

- **Unit-Tests**: Testen einzelne Komponenten isoliert.
- **Integrationstests**: Testen das Zusammenspiel mehrerer Komponenten.
- **UI-Tests**: Testen die Benutzeroberfläche.
- **Dateityp-Tests**: Testen die Unterstützung verschiedener Dateitypen.

### Ausführen der Tests

```bash
# Alle Tests ausführen
pytest

# Bestimmte Testkategorie ausführen
pytest tests/test_core_modules.py
pytest tests/test_plugin_system.py
pytest tests/test_file_types.py
pytest tests/test_integration.py
```

## Projektstruktur

```
file_organizer/
├── docs/                   # Dokumentation
│   ├── architecture.md     # Architekturübersicht
│   ├── requirements.md     # Anforderungen
│   ├── user_manual.md      # Benutzerhandbuch
│   └── developer_docs.md   # Entwicklerdokumentation
├── plugins/                # Plugin-Verzeichnis
│   ├── example_workflow.yaml  # Beispiel-Workflow
│   └── logger_plugin.py    # Beispiel-Plugin
├── src/                    # Quellcode
│   ├── file_analyzer.py    # Dateianalyse
│   ├── duplicate_detector.py  # Duplikaterkennung
│   ├── file_manager.py     # Dateiverwaltung
│   ├── smart_file_manager.py  # Intelligente Dateiverwaltung
│   ├── plugin_system.py    # Plugin-System
│   └── ui/                 # Benutzeroberfläche
│       ├── main_window.py  # Hauptfenster
│       ├── file_preview.py  # Dateivorschau
│       ├── duplicate_finder.py  # Duplikatsuche
│       └── file_organizer.py  # Dateiorganisation
├── tests/                  # Tests
│   ├── test_core_modules.py  # Tests für Kernmodule
│   ├── test_plugin_system.py  # Tests für Plugin-System
│   ├── test_file_types.py  # Tests für Dateitypen
│   └── test_integration.py  # Integrationstests
├── main.py                 # Hauptprogramm
├── pyproject.toml          # Projektdefinition
└── README.md               # Projektübersicht
```

## Erweiterungsmöglichkeiten

Die Anwendung wurde mit Erweiterbarkeit im Sinn entwickelt. Hier sind einige Möglichkeiten, wie die Anwendung erweitert werden kann:

### Unterstützung für neue Dateitypen

Um Unterstützung für einen neuen Dateityp hinzuzufügen:

1. Erweitern Sie die `get_file_type`-Methode in `FileAnalyzer`, um den neuen Dateityp zu erkennen.
2. Implementieren Sie eine spezifische Analysemethode für den neuen Dateityp.
3. Erweitern Sie die Vorschaukomponente, um den neuen Dateityp anzuzeigen.

### Neue Organisationsmethoden

Um eine neue Organisationsmethode hinzuzufügen:

1. Implementieren Sie eine neue Methode in `SmartFileManager` (z.B. `_organize_by_custom_method`).
2. Erweitern Sie die `auto_organize_directory`-Methode, um die neue Methode zu unterstützen.
3. Aktualisieren Sie die UI, um die neue Methode anzuzeigen.

### KI-Integration

Die Anwendung ist vorbereitet für die Integration von KI-Funktionen:

1. Erstellen Sie ein Plugin, das eine KI-API (z.B. OpenAI, Hugging Face) verwendet.
2. Implementieren Sie Funktionen wie Inhaltsanalyse, Bildklassifizierung oder Textextraktion.
3. Integrieren Sie die KI-Funktionen in die bestehenden Module.

## Bekannte Einschränkungen

- Die Anwendung unterstützt derzeit keine Vorschau für alle Dateitypen.
- Die Ähnlichkeitserkennung für Bilder ist rudimentär und könnte verbessert werden.
- Die Leistung kann bei sehr großen Verzeichnissen beeinträchtigt sein.
- Die Anwendung ist nicht für die Verwaltung von Netzwerkressourcen optimiert.

## Fehlerbehebung für Entwickler

### Debugging

Die Anwendung verwendet das Python-Logging-System für Debugging-Informationen:

```python
import logging

# Logger konfigurieren
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Logger erstellen
logger = logging.getLogger("my_module")

# Logging verwenden
logger.debug("Debug-Nachricht")
logger.info("Info-Nachricht")
logger.warning("Warnung")
logger.error("Fehler")
```

### Häufige Entwicklungsprobleme

#### Plugin wird nicht erkannt

- Stellen Sie sicher, dass das Plugin im richtigen Verzeichnis liegt.
- Überprüfen Sie, ob das Plugin die `PluginInterface`-Klasse korrekt erweitert.
- Prüfen Sie, ob die erforderlichen Methoden implementiert sind.

#### UI-Elemente werden nicht angezeigt

- Überprüfen Sie die Layout-Hierarchie.
- Stellen Sie sicher, dass Widgets zum Layout hinzugefügt wurden.
- Prüfen Sie, ob Widgets sichtbar sind (`setVisible(True)`).

#### Tests schlagen fehl

- Überprüfen Sie die Testumgebung (temporäre Dateien, Berechtigungen).
- Stellen Sie sicher, dass alle Abhängigkeiten installiert sind.
- Prüfen Sie, ob die getesteten Module korrekt importiert werden.

## Beitragen zum Projekt

Wir freuen uns über Beiträge zum Projekt! Hier sind einige Richtlinien:

1. Forken Sie das Repository.
2. Erstellen Sie einen Feature-Branch (`git checkout -b feature/meine-funktion`).
3. Committen Sie Ihre Änderungen (`git commit -am 'Neue Funktion: XYZ'`).
4. Pushen Sie den Branch (`git push origin feature/meine-funktion`).
5. Erstellen Sie einen Pull Request.

### Codierungsrichtlinien

- Folgen Sie PEP 8 für Python-Code.
- Schreiben Sie Docstrings für alle Klassen und Methoden.
- Fügen Sie Tests für neue Funktionen hinzu.
- Halten Sie die Abhängigkeiten minimal.

## Lizenz

Diese Anwendung wird unter der MIT-Lizenz veröffentlicht. Weitere Informationen finden Sie in der LICENSE-Datei im Anwendungsverzeichnis.
