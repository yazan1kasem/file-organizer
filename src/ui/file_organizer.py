import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QFileDialog, QListWidget, QListWidgetItem,
    QTabWidget, QSplitter, QMessageBox, QProgressBar, QDialog, QCheckBox,
    QRadioButton, QButtonGroup, QGroupBox, QComboBox, QLineEdit
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont

class FileOrganizerWidget(QWidget):
    """
    Widget zur intelligenten Organisation von Dateien.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Hauptlayout
        self.layout = QVBoxLayout(self)
        
        # Titel
        self.title_label = QLabel("Intelligente Dateiorganisation")
        self.title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)
        
        # Quellverzeichnis
        source_layout = QHBoxLayout()
        source_label = QLabel("Quellverzeichnis:")
        source_layout.addWidget(source_label)
        
        self.source_field = QLineEdit()
        self.source_field.setReadOnly(True)
        source_layout.addWidget(self.source_field)
        
        self.source_button = QPushButton("Durchsuchen...")
        source_layout.addWidget(self.source_button)
        
        self.layout.addLayout(source_layout)
        
        # Zielverzeichnis
        target_layout = QHBoxLayout()
        target_label = QLabel("Zielverzeichnis:")
        target_layout.addWidget(target_label)
        
        self.target_field = QLineEdit()
        self.target_field.setReadOnly(True)
        target_layout.addWidget(self.target_field)
        
        self.target_button = QPushButton("Durchsuchen...")
        target_layout.addWidget(self.target_button)
        
        self.layout.addLayout(target_layout)
        
        # Organisationsmethode
        method_group = QGroupBox("Organisationsmethode")
        method_layout = QVBoxLayout()
        
        self.method_combo = QComboBox()
        self.method_combo.addItem("Nach Dateityp organisieren")
        self.method_combo.addItem("Nach Datum organisieren")
        self.method_combo.addItem("Nach Größe organisieren")
        self.method_combo.addItem("Nach Inhalt organisieren")
        method_layout.addWidget(self.method_combo)
        
        # Optionen für Datumsmethode
        self.date_options = QWidget()
        date_options_layout = QHBoxLayout(self.date_options)
        date_options_layout.setContentsMargins(0, 0, 0, 0)
        
        date_format_label = QLabel("Datumsformat:")
        date_options_layout.addWidget(date_format_label)
        
        self.date_format_combo = QComboBox()
        self.date_format_combo.addItem("Jahr")
        self.date_format_combo.addItem("Jahr/Monat")
        self.date_format_combo.addItem("Jahr/Monat/Tag")
        date_options_layout.addWidget(self.date_format_combo)
        
        method_layout.addWidget(self.date_options)
        self.date_options.setVisible(False)
        
        # Optionen für Inhaltsorganisation
        self.content_options = QWidget()
        content_options_layout = QHBoxLayout(self.content_options)
        content_options_layout.setContentsMargins(0, 0, 0, 0)
        
        content_method_label = QLabel("Inhaltsmethode:")
        content_options_layout.addWidget(content_method_label)
        
        self.content_method_combo = QComboBox()
        self.content_method_combo.addItem("Textähnlichkeit")
        self.content_method_combo.addItem("Bildähnlichkeit")
        self.content_method_combo.addItem("Thematische Gruppierung")
        content_options_layout.addWidget(self.content_method_combo)
        
        method_layout.addWidget(self.content_options)
        self.content_options.setVisible(False)
        
        method_group.setLayout(method_layout)
        self.layout.addWidget(method_group)
        
        # Allgemeine Optionen
        options_group = QGroupBox("Optionen")
        options_layout = QVBoxLayout()
        
        self.recursive_check = QCheckBox("Unterverzeichnisse einbeziehen")
        options_layout.addWidget(self.recursive_check)
        
        self.move_check = QCheckBox("Dateien verschieben (statt kopieren)")
        self.move_check.setChecked(True)
        options_layout.addWidget(self.move_check)
        
        self.overwrite_check = QCheckBox("Bestehende Dateien überschreiben")
        options_layout.addWidget(self.overwrite_check)
        
        options_group.setLayout(options_layout)
        self.layout.addWidget(options_group)
        
        # Fortschrittsbereich
        progress_layout = QVBoxLayout()
        
        self.status_label = QLabel("Bereit")
        progress_layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        progress_layout.addWidget(self.progress_bar)
        
        self.layout.addLayout(progress_layout)
        
        # Aktionsbereich
        action_layout = QHBoxLayout()
        
        self.organize_button = QPushButton("Dateien organisieren")
        self.organize_button.setEnabled(False)
        action_layout.addWidget(self.organize_button)
        
        self.cancel_button = QPushButton("Abbrechen")
        self.cancel_button.setEnabled(False)
        action_layout.addWidget(self.cancel_button)
        
        self.layout.addLayout(action_layout)
        
        # Verbinde Signale
        self.source_button.clicked.connect(self.select_source_directory)
        self.target_button.clicked.connect(self.select_target_directory)
        self.method_combo.currentIndexChanged.connect(self.method_changed)
        self.organize_button.clicked.connect(self.organize_files)
        self.cancel_button.clicked.connect(self.cancel_organization)
    
    def select_source_directory(self):
        """
        Öffnet einen Dialog zur Auswahl des Quellverzeichnisses.
        """
        directory = QFileDialog.getExistingDirectory(
            self, "Quellverzeichnis auswählen", os.path.expanduser("~"),
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks
        )
        
        if directory:
            self.source_field.setText(directory)
            
            # Wenn kein Zielverzeichnis ausgewählt ist, setze es auf das gleiche wie das Quellverzeichnis
            if not self.target_field.text():
                self.target_field.setText(directory)
            
            # Aktiviere Organisieren-Button, wenn sowohl Quell- als auch Zielverzeichnis ausgewählt sind
            self.organize_button.setEnabled(bool(self.target_field.text()))
    
    def select_target_directory(self):
        """
        Öffnet einen Dialog zur Auswahl des Zielverzeichnisses.
        """
        directory = QFileDialog.getExistingDirectory(
            self, "Zielverzeichnis auswählen", self.source_field.text() or os.path.expanduser("~"),
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks
        )
        
        if directory:
            self.target_field.setText(directory)
            
            # Aktiviere Organisieren-Button, wenn sowohl Quell- als auch Zielverzeichnis ausgewählt sind
            self.organize_button.setEnabled(bool(self.source_field.text()))
    
    def method_changed(self, index):
        """
        Aktualisiert die UI basierend auf der ausgewählten Organisationsmethode.
        
        Args:
            index (int): Index der ausgewählten Methode.
        """
        # Verstecke alle methodenspezifischen Optionen
        self.date_options.setVisible(False)
        self.content_options.setVisible(False)
        
        # Zeige entsprechende Optionen basierend auf der ausgewählten Methode
        if index == 1:  # Nach Datum organisieren
            self.date_options.setVisible(True)
        elif index == 3:  # Nach Inhalt organisieren
            self.content_options.setVisible(True)
    
    def organize_files(self):
        """
        Organisiert Dateien basierend auf den ausgewählten Optionen.
        """
        source_dir = self.source_field.text()
        target_dir = self.target_field.text()
        
        if not source_dir or not target_dir:
            QMessageBox.warning(self, "Fehler", "Bitte wählen Sie Quell- und Zielverzeichnis aus.")
            return
        
        method = self.method_combo.currentText()
        recursive = self.recursive_check.isChecked()
        move_files = self.move_check.isChecked()
        overwrite = self.overwrite_check.isChecked()
        
        # Bestätigungsdialog
        confirm_msg = f"Möchten Sie die Dateien in\n{source_dir}\n"
        confirm_msg += f"nach {method.lower()} organisieren?\n\n"
        confirm_msg += f"Zielverzeichnis: {target_dir}\n"
        confirm_msg += f"Dateien werden {'verschoben' if move_files else 'kopiert'}.\n"
        confirm_msg += f"Unterverzeichnisse werden {'einbezogen' if recursive else 'ignoriert'}.\n"
        confirm_msg += f"Bestehende Dateien werden {'überschrieben' if overwrite else 'übersprungen'}."
        
        confirm = QMessageBox.question(
            self, "Dateien organisieren",
            confirm_msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            # In einer vollständigen Implementierung würde hier die Dateiorganisation durchgeführt werden
            # Für dieses Beispiel simulieren wir den Prozess
            
            # Deaktiviere UI-Elemente während der Organisation
            self.organize_button.setEnabled(False)
            self.source_button.setEnabled(False)
            self.target_button.setEnabled(False)
            self.method_combo.setEnabled(False)
            self.recursive_check.setEnabled(False)
            self.move_check.setEnabled(False)
            self.overwrite_check.setEnabled(False)
            
            # Aktiviere Abbrechen-Button
            self.cancel_button.setEnabled(True)
            
            # Zeige Fortschrittsbalken
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            
            # Aktualisiere Status
            self.status_label.setText(f"Organisiere Dateien nach {method.lower()}...")
            
            # Simuliere Fortschritt
            self.simulate_organization()
    
    def simulate_organization(self):
        """
        Simuliert den Organisationsprozess.
        """
        import time
        
        # Simuliere Dateisuche
        self.status_label.setText("Suche Dateien...")
        for i in range(30):
            self.progress_bar.setValue(i)
            QApplication.processEvents()
            time.sleep(0.02)
        
        # Simuliere Analyse
        self.status_label.setText("Analysiere Dateien...")
        for i in range(30, 70):
            self.progress_bar.setValue(i)
            QApplication.processEvents()
            time.sleep(0.02)
        
        # Simuliere Organisation
        self.status_label.setText("Organisiere Dateien...")
        for i in range(70, 100):
            self.progress_bar.setValue(i)
            QApplication.processEvents()
            time.sleep(0.02)
        
        # Abschluss
        self.progress_bar.setValue(100)
        self.status_label.setText("Organisation abgeschlossen!")
        
        # Zeige Ergebnisdialog
        QMessageBox.information(
            self, "Organisation abgeschlossen",
            "Die Dateien wurden erfolgreich organisiert.\n\n"
            "Organisierte Dateien: 42\n"
            "Übersprungene Dateien: 3\n"
            "Fehler: 0"
        )
        
        # Setze UI zurück
        self.reset_ui()
    
    def cancel_organization(self):
        """
        Bricht den Organisationsprozess ab.
        """
        # In einer vollständigen Implementierung würde hier der Organisationsprozess abgebrochen werden
        # Für dieses Beispiel setzen wir einfach die UI zurück
        
        # Zeige Bestätigungsdialog
        confirm = QMessageBox.question(
            self, "Organisation abbrechen",
            "Möchten Sie den Organisationsprozess wirklich abbrechen?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            self.status_label.setText("Organisation abgebrochen.")
            self.reset_ui()
    
    def reset_ui(self):
        """
        Setzt die UI nach der Organisation zurück.
        """
        # Aktiviere UI-Elemente
        self.organize_button.setEnabled(True)
        self.source_button.setEnabled(True)
        self.target_button.setEnabled(True)
        self.method_combo.setEnabled(True)
        self.recursive_check.setEnabled(True)
        self.move_check.setEnabled(True)
        self.overwrite_check.setEnabled(True)
        
        # Deaktiviere Abbrechen-Button
        self.cancel_button.setEnabled(False)
        
        # Verstecke Fortschrittsbalken
        self.progress_bar.setVisible(False)

# Beispiel für die Verwendung
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = QWidget()
    window.setWindowTitle("Dateiorganisation-Test")
    window.setMinimumSize(800, 600)
    
    layout = QVBoxLayout(window)
    
    organizer_widget = FileOrganizerWidget()
    layout.addWidget(organizer_widget)
    
    window.show()
    
    sys.exit(app.exec())
