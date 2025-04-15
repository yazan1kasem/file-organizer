# Installation und Einrichtungsanleitung

Diese Anleitung führt Sie durch die Installation und Einrichtung der KI-basierten Dateiverwaltungsanwendung.

## Systemvoraussetzungen

Bevor Sie beginnen, stellen Sie sicher, dass Ihr System die folgenden Anforderungen erfüllt:

- **Betriebssystem**: Windows 10/11, macOS 10.15+, oder Linux (Ubuntu 20.04+, Fedora 34+, etc.)
- **Python**: Version 3.8 oder höher
- **Arbeitsspeicher**: Mindestens 4 GB RAM
- **Festplattenspeicher**: Mindestens 500 MB freier Speicherplatz
- **Bildschirmauflösung**: Mindestens 1280x720 Pixel

## Installation

### Schritt 1: Python installieren

Falls Python noch nicht auf Ihrem System installiert ist:

#### Windows
1. Besuchen Sie [python.org](https://www.python.org/downloads/)
2. Laden Sie die neueste Python-Version herunter (mindestens 3.8)
3. Führen Sie das Installationsprogramm aus
4. **Wichtig**: Aktivieren Sie die Option "Add Python to PATH"
5. Klicken Sie auf "Install Now"

#### macOS
1. Besuchen Sie [python.org](https://www.python.org/downloads/)
2. Laden Sie die neueste Python-Version herunter (mindestens 3.8)
3. Führen Sie das Installationsprogramm aus
4. Folgen Sie den Anweisungen des Installationsassistenten

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

#### Linux (Fedora)
```bash
sudo dnf install python3 python3-pip python3-virtualenv
```

### Schritt 2: Anwendung herunterladen

1. Laden Sie das Anwendungspaket von der offiziellen Website oder dem Repository herunter
2. Entpacken Sie die Datei in ein Verzeichnis Ihrer Wahl

Alternativ können Sie das Repository klonen, wenn Sie Git installiert haben:
```bash
git clone https://github.com/fileorganizer/file-organizer.git
cd file-organizer
```

### Schritt 3: Virtuelle Umgebung erstellen (empfohlen)

Eine virtuelle Umgebung hilft, Konflikte zwischen Paketversionen zu vermeiden.

#### Windows
```bash
cd file-organizer
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux
```bash
cd file-organizer
python3 -m venv venv
source venv/bin/activate
```

### Schritt 4: Abhängigkeiten installieren

Installieren Sie alle erforderlichen Pakete mit pip:

```bash
pip install -r requirements.txt
```

Dies installiert alle notwendigen Bibliotheken wie PyQt6, Pillow, PyYAML und andere Abhängigkeiten.

### Schritt 5: Anwendung starten

Nachdem alle Abhängigkeiten installiert sind, können Sie die Anwendung starten:

#### Windows
```bash
python main.py
```

#### macOS/Linux
```bash
python3 main.py
```

## Erste Einrichtung

Beim ersten Start der Anwendung werden Sie durch einen Einrichtungsassistenten geführt:

1. **Sprache auswählen**: Wählen Sie Ihre bevorzugte Sprache aus der Liste
2. **Erscheinungsbild**: Wählen Sie zwischen Hell- und Dunkel-Modus
3. **Standardverzeichnis**: Wählen Sie das Standardverzeichnis für den Datei-Browser
4. **Plugin-Einstellungen**: Aktivieren oder deaktivieren Sie die verfügbaren Plugins

## Konfiguration

### Anwendungseinstellungen

Die Anwendungseinstellungen werden in der Datei `config.yaml` im Anwendungsverzeichnis gespeichert. Sie können diese Datei direkt bearbeiten oder die Einstellungen über die Benutzeroberfläche ändern.

Wichtige Einstellungen:
- `language`: Sprache der Benutzeroberfläche
- `theme`: Erscheinungsbild (light/dark)
- `default_directory`: Standardverzeichnis für den Datei-Browser
- `plugins`: Liste der aktivierten Plugins
- `file_associations`: Zuordnungen von Dateitypen zu Aktionen

### Plugin-Verzeichnis

Plugins werden im Verzeichnis `plugins` gespeichert. Um ein neues Plugin hinzuzufügen:

1. Platzieren Sie die Plugin-Datei (`.py` oder `.yaml`) im Verzeichnis `plugins`
2. Starten Sie die Anwendung neu oder klicken Sie auf "Plugins aktualisieren"
3. Aktivieren Sie das neue Plugin in den Einstellungen

## Fehlerbehebung

### Die Anwendung startet nicht

**Problem**: Python-Version ist zu alt
**Lösung**: Installieren Sie Python 3.8 oder höher

**Problem**: Fehlende Abhängigkeiten
**Lösung**: Führen Sie `pip install -r requirements.txt` aus

**Problem**: PyQt6 kann nicht installiert werden
**Lösung**: Installieren Sie die erforderlichen Systembibliotheken:
- Ubuntu/Debian: `sudo apt install python3-pyqt6 libxcb-xinerama0`
- Fedora: `sudo dnf install python3-qt6`
- Windows: Stellen Sie sicher, dass Microsoft Visual C++ Redistributable installiert ist

### Plugins werden nicht geladen

**Problem**: Plugin-Verzeichnis wird nicht gefunden
**Lösung**: Stellen Sie sicher, dass das Verzeichnis `plugins` im Anwendungsverzeichnis existiert

**Problem**: Plugin-Format ist ungültig
**Lösung**: Überprüfen Sie, ob das Plugin die richtige Struktur hat und alle erforderlichen Methoden implementiert

### Dateien können nicht analysiert werden

**Problem**: Fehlende Berechtigungen
**Lösung**: Stellen Sie sicher, dass die Anwendung Leserechte für die Dateien hat

**Problem**: Nicht unterstützter Dateityp
**Lösung**: Überprüfen Sie, ob der Dateityp von der Anwendung unterstützt wird

## Aktualisierung

Um die Anwendung zu aktualisieren:

1. Laden Sie die neueste Version herunter
2. Sichern Sie Ihre Konfigurationsdatei `config.yaml` und das Verzeichnis `plugins`
3. Installieren Sie die neue Version
4. Kopieren Sie Ihre gesicherte Konfigurationsdatei und Plugins zurück

## Deinstallation

Um die Anwendung zu deinstallieren:

1. Löschen Sie das Anwendungsverzeichnis
2. Optional: Entfernen Sie die virtuelle Umgebung

## Weitere Ressourcen

- **Benutzerhandbuch**: Ausführliche Informationen zur Verwendung der Anwendung finden Sie im Benutzerhandbuch (`docs/user_manual.md`)
- **Entwicklerdokumentation**: Informationen zur Erweiterung der Anwendung finden Sie in der Entwicklerdokumentation (`docs/developer_docs.md`)
- **Online-Support**: Besuchen Sie unsere Website für weitere Unterstützung: [support.fileorganizer.com](https://support.fileorganizer.com)
