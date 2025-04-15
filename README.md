# File Organizer – KI-basierte Datei-Management-Anwendung in Python

<p align="center">
  <img src="https://github.com/user-attachments/assets/1f9d91ab-e2ca-400f-ad46-93c20f741000" alt="Hauptansicht der App" width="600"/>
</p>
<p align="center"><em>Abbildung: Hauptansicht der Anwendung</em></p>

## Projektbeschreibung

File Organizer ist eine KI-gestützte Anwendung zur automatisierten Organisation von Dateien in lokalen Verzeichnissen. Die Software analysiert sowohl Inhalte als auch Metadaten und ermöglicht eine intelligente Umbenennung, Klassifikation und Duplikaterkennung. Ziel ist es, unstrukturierte Dateisysteme effizient zu organisieren – mit Fokus auf Produktivität, Übersichtlichkeit und Automatisierung.

> Hinweis: Die Anwendung befindet sich derzeit in der Testphase. Ein leistungsfähiges System ist erforderlich, um die lokale KI (basierend auf LLaMA 3) zuverlässig auszuführen.

## Hauptfunktionen

- **Inhaltsbasierte Umbenennung**  
  Die Anwendung liest Datei-Inhalte (z. B. Titel, Text, Metadaten) aus und erzeugt semantisch sinnvolle und strukturierte Dateinamen.

- **Automatische Kategorisierung**  
  Dateien werden intelligent in passende Unterordner sortiert – beispielsweise „Dokumente“, „Bilder“, „Verträge“, „Code“ usw.

<p align="center">
  <img src="https://github.com/user-attachments/assets/677476e1-e3a2-4869-b8d2-ced50fd52850" alt="Dateikategorisierung" width="600"/>
</p>
<p align="center"><em>Abbildung: Intelligente Dateikategorisierung</em></p>

- **Duplikaterkennung und Löschung**  
  Mehrfache Dateien werden durch Hashing und Inhaltsvergleich identifiziert und können je nach Einstellung automatisch oder manuell entfernt werden.

- **Individuelle Anpassbarkeit**  
  Unterstützt benutzerdefinierte Regeln zur Umbenennung, Dateiauswahl und Sortierung. Auch Ausschlusslisten können definiert werden.

## Technologischer Stack

- Programmiersprache: Python 3.x  
- Benutzeroberfläche: PyQt6  
- KI-Modell: Meta LLaMA 3.1 (8B)

## Ausführung

1. Repository klonen  
   ```bash
   git clone https://github.com/yazan1kasem/file-organizer.git
   cd file-organizer
   ```

2. Abhängigkeiten installieren  
   ```bash
   pip install -r requirements.txt
   ```

3. Anwendung starten  
   ```bash
   python main.py
   ```

## Lizenz

Dieses Projekt wurde zu Lern-, Analyse- und Demonstrationszwecken entwickelt. Eine nicht-kommerzielle Nutzung ist gestattet. Für eine kommerzielle Nutzung ist die ausdrückliche Zustimmung des Autors erforderlich.
