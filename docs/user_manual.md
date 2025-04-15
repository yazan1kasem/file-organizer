# Benutzerhandbuch: KI-basierte Dateiverwaltungsanwendung

## Einführung

Willkommen zur KI-basierten Dateiverwaltungsanwendung! Diese Software wurde entwickelt, um Ihnen bei der Organisation, Analyse und Verwaltung Ihrer Dateien zu helfen. Mit Hilfe intelligenter Algorithmen kann die Anwendung Dateien verschiedener Typen verstehen, Vorschläge zur Organisation machen und Ihnen helfen, Ordnung in Ihrem digitalen Leben zu schaffen.

## Installation

### Systemvoraussetzungen

- Python 3.8 oder höher
- Mindestens 4 GB RAM
- 500 MB freier Festplattenspeicher

### Installationsschritte

1. Stellen Sie sicher, dass Python 3.8 oder höher installiert ist.
2. Laden Sie das Anwendungspaket herunter.
3. Entpacken Sie das Paket in ein Verzeichnis Ihrer Wahl.
4. Öffnen Sie ein Terminal oder eine Kommandozeile und navigieren Sie zum Anwendungsverzeichnis.
5. Führen Sie den folgenden Befehl aus, um die erforderlichen Abhängigkeiten zu installieren:

```
pip install -r requirements.txt
```

6. Starten Sie die Anwendung mit:

```
python main.py
```

## Hauptfunktionen

### Dateianalyse

Die Anwendung kann verschiedene Dateitypen analysieren und Ihnen detaillierte Informationen dazu anzeigen:

- **Textdateien**: Wortanzahl, Zeilenanzahl, Zeichenanzahl, Spracherkennung
- **Bilder**: Abmessungen, Farbtiefe, Format, EXIF-Daten
- **Videos**: Länge, Auflösung, Codec, Metadaten
- **Audio**: Länge, Bitrate, Format, Metadaten
- **Dokumente**: Seitenanzahl, Autor, Erstellungsdatum
- **Code**: Programmiersprache, Zeilenanzahl, Funktionen/Klassen
- **Tabellen**: Zeilen- und Spaltenanzahl, Datentypen

Um eine Datei zu analysieren:
1. Wählen Sie die Datei im Datei-Browser aus.
2. Klicken Sie auf den "Analysieren"-Button oder wechseln Sie zum "Analyse"-Tab.
3. Die Analyseergebnisse werden im Hauptbereich angezeigt.

### Dateivorschau

Die Anwendung bietet eine integrierte Vorschau für verschiedene Dateitypen:

- **Textdateien**: Textinhalt mit Syntaxhervorhebung
- **Bilder**: Bildvorschau mit Zoom-Funktion
- **Videos**: Videoplayer mit Grundfunktionen
- **Audio**: Audioplayer mit Grundfunktionen
- **Dokumente**: PDF-Vorschau
- **Code**: Syntaxhervorhebung und Codestruktur
- **Tabellen**: Tabellenansicht mit Sortier- und Filterfunktionen

Um eine Vorschau anzuzeigen:
1. Wählen Sie die Datei im Datei-Browser aus.
2. Die Vorschau wird automatisch im Vorschaubereich angezeigt.
3. Nutzen Sie die Steuerelemente im Vorschaubereich für spezifische Funktionen (z.B. Zoom, Abspielen).

### Intelligentes Dateimanagement

#### Automatische Gruppierung

Die Anwendung kann Dateien automatisch nach verschiedenen Kriterien gruppieren:

- **Nach Dateityp**: Gruppiert Dateien nach ihrem Typ (Dokumente, Bilder, Videos, etc.)
- **Nach Datum**: Gruppiert Dateien nach Erstellungs- oder Änderungsdatum
- **Nach Größe**: Gruppiert Dateien nach ihrer Größe
- **Nach Inhalt**: Gruppiert Dateien basierend auf Inhaltsähnlichkeit

Um Dateien zu gruppieren:
1. Wählen Sie das Quellverzeichnis im Datei-Browser aus.
2. Wechseln Sie zum "Organisieren"-Tab.
3. Wählen Sie die gewünschte Gruppierungsmethode.
4. Wählen Sie das Zielverzeichnis.
5. Klicken Sie auf "Dateien organisieren".

#### Aufräumvorschläge

Die Anwendung analysiert Ihre Verzeichnisse und macht intelligente Vorschläge zum Aufräumen:

- Identifizierung leerer Verzeichnisse
- Erkennung temporärer und unnötiger Dateien
- Vorschläge zur Archivierung alter Dateien
- Hinweise auf besonders große Dateien und Verzeichnisse

Um Aufräumvorschläge zu erhalten:
1. Wählen Sie das zu analysierende Verzeichnis im Datei-Browser aus.
2. Wechseln Sie zum "Aufräumen"-Tab.
3. Klicken Sie auf "Verzeichnis analysieren".
4. Die Vorschläge werden im Hauptbereich angezeigt.
5. Wählen Sie die gewünschten Aktionen aus und klicken Sie auf "Ausführen".

#### Duplikaterkennung

Die Anwendung kann Duplikate in Ihren Dateien erkennen:

- Exakte Duplikate (identischer Inhalt)
- Ähnliche Dateien (ähnlicher Inhalt)
- Verschiedene Versionen der gleichen Datei

Um Duplikate zu finden:
1. Wählen Sie das zu durchsuchende Verzeichnis im Datei-Browser aus.
2. Wechseln Sie zum "Duplikate"-Tab.
3. Wählen Sie die Suchoptionen (Rekursiv, Vergleichsmethode, Dateitypen).
4. Klicken Sie auf "Nach Duplikaten suchen".
5. Die gefundenen Duplikate werden gruppiert angezeigt.
6. Wählen Sie die zu löschenden Duplikate aus und klicken Sie auf "Ausgewählte löschen".

### Benutzeroberfläche

#### Hauptansicht

Die Hauptansicht der Anwendung besteht aus mehreren Bereichen:

- **Datei-Browser**: Zeigt die Verzeichnisstruktur und Dateien an.
- **Vorschaubereich**: Zeigt eine Vorschau der ausgewählten Datei an.
- **Informationsbereich**: Zeigt Informationen zur ausgewählten Datei an.
- **Aktionsbereich**: Enthält Schaltflächen für verschiedene Aktionen.
- **Tab-Bereich**: Ermöglicht den Wechsel zwischen verschiedenen Funktionen.

#### Tastenkombinationen

Die Anwendung unterstützt verschiedene Tastenkombinationen für eine effiziente Bedienung:

- **Strg+O**: Datei öffnen
- **Strg+S**: Datei speichern
- **Strg+F**: Suchen
- **Strg+Z**: Rückgängig
- **Strg+Y**: Wiederherstellen
- **F5**: Aktualisieren
- **F1**: Hilfe anzeigen

## Erweiterte Funktionen

### Plugin-System

Die Anwendung verfügt über ein leistungsfähiges Plugin-System, das es ermöglicht, die Funktionalität zu erweitern:

- **Python-Plugins**: Erweitern Sie die Anwendung mit eigenen Python-Skripten.
- **YAML-Workflows**: Definieren Sie komplexe Arbeitsabläufe in YAML-Dateien.
- **Hook-System**: Reagieren Sie auf Ereignisse in der Anwendung.

Um Plugins zu verwalten:
1. Wechseln Sie zum "Plugins"-Tab.
2. Hier werden alle verfügbaren Plugins angezeigt.
3. Aktivieren oder deaktivieren Sie Plugins nach Bedarf.
4. Klicken Sie auf "Plugin installieren", um neue Plugins hinzuzufügen.

### Anpassungsmöglichkeiten

Die Anwendung bietet verschiedene Anpassungsmöglichkeiten:

- **Erscheinungsbild**: Wählen Sie zwischen Hell- und Dunkel-Modus.
- **Sprache**: Wählen Sie Ihre bevorzugte Sprache.
- **Dateityp-Zuordnungen**: Passen Sie an, wie verschiedene Dateitypen behandelt werden.
- **Tastenkombinationen**: Definieren Sie eigene Tastenkombinationen.

Um die Anwendung anzupassen:
1. Wechseln Sie zum "Einstellungen"-Tab.
2. Wählen Sie die gewünschte Kategorie.
3. Nehmen Sie Ihre Änderungen vor und klicken Sie auf "Speichern".

## Fehlerbehebung

### Häufige Probleme

#### Die Anwendung startet nicht

- Stellen Sie sicher, dass Python 3.8 oder höher installiert ist.
- Überprüfen Sie, ob alle Abhängigkeiten korrekt installiert sind.
- Prüfen Sie die Konsolenausgabe auf Fehlermeldungen.

#### Dateien werden nicht korrekt analysiert

- Stellen Sie sicher, dass die Datei nicht beschädigt ist.
- Überprüfen Sie, ob der Dateityp unterstützt wird.
- Prüfen Sie, ob Sie Leserechte für die Datei haben.

#### Plugins funktionieren nicht

- Stellen Sie sicher, dass das Plugin kompatibel mit Ihrer Anwendungsversion ist.
- Überprüfen Sie, ob alle Abhängigkeiten des Plugins installiert sind.
- Prüfen Sie die Plugin-Logs auf Fehlermeldungen.

### Support

Wenn Sie Hilfe benötigen oder Fehler melden möchten:

- Besuchen Sie unsere Support-Website: [support.fileorganizer.com](https://support.fileorganizer.com)
- Senden Sie eine E-Mail an: support@fileorganizer.com
- Öffnen Sie ein Issue auf GitHub: [github.com/fileorganizer/issues](https://github.com/fileorganizer/issues)

## Datenschutz und Sicherheit

Die Anwendung respektiert Ihre Privatsphäre und Sicherheit:

- Alle Daten werden lokal auf Ihrem Computer verarbeitet.
- Es werden keine Daten ohne Ihre ausdrückliche Zustimmung an externe Server gesendet.
- Die optionale KI-Unterstützung kann aktiviert werden, wenn Sie erweiterte Funktionen nutzen möchten.

## Lizenz

Diese Anwendung wird unter der MIT-Lizenz veröffentlicht. Weitere Informationen finden Sie in der LICENSE-Datei im Anwendungsverzeichnis.
