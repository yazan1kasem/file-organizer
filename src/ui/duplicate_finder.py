import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QListWidget, QListWidgetItem,
    QTabWidget, QSplitter, QMessageBox, QProgressBar, QDialog, QCheckBox,
    QRadioButton, QButtonGroup, QGroupBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont


class DuplicateFinderWidget(QWidget):
    """
    Widget zur Suche und Verwaltung von Duplikaten.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Hauptlayout
        self.layout = QVBoxLayout(self)

        # Titel
        self.title_label = QLabel("Duplikatsuche")
        self.title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Optionen
        self.options_group = QGroupBox("Suchoptionen")
        options_layout = QVBoxLayout()

        # Suchtiefe
        depth_layout = QHBoxLayout()
        depth_label = QLabel("Suchtiefe:")
        depth_layout.addWidget(depth_label)

        self.depth_group = QButtonGroup(self)

        self.current_dir_radio = QRadioButton("Nur aktuelles Verzeichnis")
        self.current_dir_radio.setChecked(True)
        self.depth_group.addButton(self.current_dir_radio)
        depth_layout.addWidget(self.current_dir_radio)

        self.recursive_radio = QRadioButton("Rekursiv (alle Unterverzeichnisse)")
        self.depth_group.addButton(self.recursive_radio)
        depth_layout.addWidget(self.recursive_radio)

        options_layout.addLayout(depth_layout)

        # Vergleichsmethode
        method_layout = QHBoxLayout()
        method_label = QLabel("Vergleichsmethode:")
        method_layout.addWidget(method_label)

        self.method_group = QButtonGroup(self)

        self.size_radio = QRadioButton("Nur Größe")
        self.method_group.addButton(self.size_radio)
        method_layout.addWidget(self.size_radio)

        self.content_radio = QRadioButton("Inhalt (genauer, aber langsamer)")
        self.content_radio.setChecked(True)
        self.method_group.addButton(self.content_radio)
        method_layout.addWidget(self.content_radio)

        options_layout.addLayout(method_layout)

        # Dateitypen
        types_layout = QHBoxLayout()
        types_label = QLabel("Dateitypen:")
        types_layout.addWidget(types_label)

        self.all_types_check = QCheckBox("Alle Dateitypen")
        self.all_types_check.setChecked(True)
        types_layout.addWidget(self.all_types_check)

        self.images_check = QCheckBox("Bilder")
        types_layout.addWidget(self.images_check)

        self.documents_check = QCheckBox("Dokumente")
        types_layout.addWidget(self.documents_check)

        self.videos_check = QCheckBox("Videos")
        types_layout.addWidget(self.videos_check)

        options_layout.addLayout(types_layout)

        self.options_group.setLayout(options_layout)
        self.layout.addWidget(self.options_group)

        # Aktionsbereich
        action_layout = QHBoxLayout()

        self.search_button = QPushButton("Nach Duplikaten suchen")
        action_layout.addWidget(self.search_button)

        self.clear_button = QPushButton("Ergebnisse löschen")
        self.clear_button.setEnabled(False)
        action_layout.addWidget(self.clear_button)

        self.layout.addLayout(action_layout)

        # Fortschrittsbalken
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.layout.addWidget(self.progress_bar)

        # Ergebnisbereich
        self.results_label = QLabel("Keine Duplikate gefunden.")
        self.results_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.results_label)

        self.results_list = QListWidget()
        self.results_list.setVisible(False)
        self.layout.addWidget(self.results_list)

        # Aktionen für gefundene Duplikate
        duplicate_action_layout = QHBoxLayout()

        self.select_all_button = QPushButton("Alle auswählen")
        self.select_all_button.setEnabled(False)
        duplicate_action_layout.addWidget(self.select_all_button)

        self.select_none_button = QPushButton("Keine auswählen")
        self.select_none_button.setEnabled(False)
        duplicate_action_layout.addWidget(self.select_none_button)

        self.remove_selected_button = QPushButton("Ausgewählte löschen")
        self.remove_selected_button.setEnabled(False)
        duplicate_action_layout.addWidget(self.remove_selected_button)

        self.layout.addLayout(duplicate_action_layout)

        # Verbinde Signale
        self.search_button.clicked.connect(self.search_duplicates)
        self.clear_button.clicked.connect(self.clear_results)
        self.all_types_check.stateChanged.connect(self.toggle_file_types)
        self.select_all_button.clicked.connect(self.select_all_duplicates)
        self.select_none_button.clicked.connect(self.select_no_duplicates)
        self.remove_selected_button.clicked.connect(self.remove_selected_duplicates)

    def toggle_file_types(self, state):
        """
        Aktiviert oder deaktiviert die Dateityp-Checkboxen basierend auf dem Status der "Alle Dateitypen"-Checkbox.
        
        Args:
            state (int): Status der Checkbox.
        """
        enabled = state != Qt.CheckState.Checked
        self.images_check.setEnabled(enabled)
        self.documents_check.setEnabled(enabled)
        self.videos_check.setEnabled(enabled)

    def search_duplicates(self):
        """
        Sucht nach Duplikaten basierend auf den ausgewählten Optionen.
        """
        # In einer vollständigen Implementierung würde hier die Duplikatsuche durchgeführt werden
        # Für dieses Beispiel simulieren wir den Prozess

        # Zeige Fortschrittsbalken
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        # Deaktiviere Suchbutton während der Suche
        self.search_button.setEnabled(False)

        # Simuliere Fortschritt
        for i in range(101):
            self.progress_bar.setValue(i)
            QApplication.processEvents()
            import time
            time.sleep(0.02)

        # Verstecke Fortschrittsbalken
        self.progress_bar.setVisible(False)

        # Aktiviere Suchbutton wieder
        self.search_button.setEnabled(True)

        # Zeige Ergebnisse
        self.show_sample_results()

    def show_sample_results(self):
        """
        Zeigt Beispielergebnisse für die Duplikatsuche an.
        """
        # Verstecke Ergebnislabel
        self.results_label.setVisible(False)

        # Lösche vorherige Ergebnisse
        self.results_list.clear()

        # Füge Beispielergebnisse hinzu
        self.add_duplicate_group("Gruppe 1 - 3 Duplikate (1.2 MB)", [
            "/home/user/Dokumente/bericht.pdf",
            "/home/user/Downloads/bericht_kopie.pdf",
            "/home/user/Backup/bericht.pdf"
        ])

        self.add_duplicate_group("Gruppe 2 - 2 Duplikate (4.5 MB)", [
            "/home/user/Bilder/urlaub2023.jpg",
            "/home/user/Backup/Fotos/urlaub2023.jpg"
        ])

        self.add_duplicate_group("Gruppe 3 - 4 Duplikate (250 KB)", [
            "/home/user/Dokumente/notizen.txt",
            "/home/user/Desktop/notizen.txt",
            "/home/user/Downloads/notizen.txt",
            "/home/user/Backup/notizen.txt"
        ])

        # Zeige Ergebnisliste
        self.results_list.setVisible(True)

        # Aktiviere Buttons
        self.clear_button.setEnabled(True)
        self.select_all_button.setEnabled(True)
        self.select_none_button.setEnabled(True)
        self.remove_selected_button.setEnabled(True)

    def add_duplicate_group(self, group_title, file_paths):
        """
        Fügt eine Gruppe von Duplikaten zur Ergebnisliste hinzu.
        
        Args:
            group_title (str): Titel der Gruppe.
            file_paths (list): Liste von Dateipfaden.
        """
        # Füge Gruppentitel hinzu
        group_item = QListWidgetItem(group_title)
        group_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        group_item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        group_item.setBackground(Qt.GlobalColor.lightGray)
        self.results_list.addItem(group_item)

        # Füge Dateien hinzu
        for file_path in file_paths:
            file_item = QListWidgetItem(file_path)
            file_item.setFlags(
                Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsUserCheckable)
            file_item.setCheckState(Qt.CheckState.Unchecked)
            self.results_list.addItem(file_item)

    def clear_results(self):
        """
        Löscht die Ergebnisse der Duplikatsuche.
        """
        # Lösche Ergebnisliste
        self.results_list.clear()
        self.results_list.setVisible(False)

        # Zeige Standardtext
        self.results_label.setText("Keine Duplikate gefunden.")
        self.results_label.setVisible(True)

        # Deaktiviere Buttons
        self.clear_button.setEnabled(False)
        self.select_all_button.setEnabled(False)
        self.select_none_button.setEnabled(False)
        self.remove_selected_button.setEnabled(False)

    def select_all_duplicates(self):
        """
        Wählt alle Duplikate aus.
        """
        for i in range(self.results_list.count()):
            item = self.results_list.item(i)
            if item.flags() & Qt.ItemFlag.ItemIsUserCheckable:
                item.setCheckState(Qt.CheckState.Checked)

    def select_no_duplicates(self):
        """
        Wählt keine Duplikate aus.
        """
        for i in range(self.results_list.count()):
            item = self.results_list.item(i)
            if item.flags() & Qt.ItemFlag.ItemIsUserCheckable:
                item.setCheckState(Qt.CheckState.Unchecked)

    def remove_selected_duplicates(self):
        """
        Entfernt die ausgewählten Duplikate.
        """
        # Zähle ausgewählte Dateien
        selected_count = 0
        for i in range(self.results_list.count()):
            item = self.results_list.item(i)
            if item.flags() & Qt.ItemFlag.ItemIsUserCheckable and item.checkState() == Qt.CheckState.Checked:
                selected_count += 1

        if selected_count == 0:
            QMessageBox.information(self, "Keine Auswahl", "Bitte wählen Sie mindestens eine Datei aus.")
            return

        # Bestätigungsdialog
        confirm = QMessageBox.question(
            self, "Duplikate löschen",
            f"Möchten Sie {selected_count} ausgewählte Dateien wirklich löschen?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            # In einer vollständigen Implementierung würden hier die Dateien gelöscht werden
            # Für dieses Beispiel zeigen wir nur eine Meldung an
            QMessageBox.information(
                self, "Duplikate gelöscht",
                f"{selected_count} Dateien wurden gelöscht."
            )

            # Aktualisiere Ergebnisliste
            self.clear_results()


# Beispiel für die Verwendung
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Duplikatsuche-Test")
    window.setMinimumSize(800, 600)

    layout = QVBoxLayout(window)

    duplicate_widget = DuplicateFinderWidget()
    layout.addWidget(duplicate_widget)

    window.show()

    sys.exit(app.exec())
