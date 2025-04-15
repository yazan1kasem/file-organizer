import hashlib
import logging
import sys
import os
from PyQt6.QtGui import QFileSystemModel  # Correct import location
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QTreeView, QListView,
    QTabWidget, QSplitter, QMenu, QStatusBar, QToolBar, QComboBox,
    QLineEdit, QMessageBox, QProgressBar, QStyle, QDialog, QCheckBox
)
from PyQt6.QtCore import Qt, QDir, QSize, QModelIndex, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QFont
from src.ui.file_organizer import FileOrganizerWidget
from src.ui.file_preview import FilePreviewWidget

class FileOrganizerUI(QMainWindow):
    """
    Hauptfenster der KI-basierten Dateiverwaltungsanwendung.
    """

    def __init__(self):
        super().__init__()

        # Fenstertitel und Größe
        self.setWindowTitle("KI-Dateiverwaltung")
        self.setMinimumSize(1000, 600)

        # Zentrales Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Hauptlayout
        self.main_layout = QVBoxLayout(self.central_widget)

        # Erstelle UI-Komponenten
        self._create_toolbar()
        self._create_main_view()
        self._create_statusbar()

        # Initialisiere Dateisystem-Modell
        self._initialize_file_system_model()

        # Verbinde Signale und Slots
        self._connect_signals()

    def _create_toolbar(self):
        """Erstellt die Toolbar mit Aktionen."""
        self.toolbar = QToolBar("Hauptwerkzeugleiste")
        self.toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(self.toolbar)

        # Verzeichnis öffnen
        self.action_open = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon),
                                   "Verzeichnis öffnen", self)
        self.action_open.setStatusTip("Ein Verzeichnis öffnen")
        self.toolbar.addAction(self.action_open)

        self.toolbar.addSeparator()

        # Ansicht aktualisieren
        self.action_refresh = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload),
                                      "Aktualisieren", self)
        self.action_refresh.setStatusTip("Ansicht aktualisieren")
        self.toolbar.addAction(self.action_refresh)

        # Nach oben navigieren
        self.action_up = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowUp), "Nach oben", self)
        self.action_up.setStatusTip("Zum übergeordneten Verzeichnis wechseln")
        self.toolbar.addAction(self.action_up)

        self.toolbar.addSeparator()

        # Dateien organisieren
        self.action_organize = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogListView),
                                       "Organisieren", self)
        self.action_organize.setStatusTip("Dateien automatisch organisieren")
        self.toolbar.addAction(self.action_organize)

        # Duplikate finden
        self.action_duplicates = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView),
                                         "Duplikate finden", self)
        self.action_duplicates.setStatusTip("Nach Duplikaten suchen")
        self.toolbar.addAction(self.action_duplicates)

        self.toolbar.addSeparator()

        # Suchfeld
        self.search_label = QLabel("Suchen:")
        self.toolbar.addWidget(self.search_label)

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Dateien suchen...")
        self.search_field.setMinimumWidth(200)
        self.toolbar.addWidget(self.search_field)

        # Filter-Dropdown
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("Alle Dateien")
        self.filter_combo.addItem("Dokumente")
        self.filter_combo.addItem("Bilder")
        self.filter_combo.addItem("Videos")
        self.filter_combo.addItem("Audio")
        self.filter_combo.addItem("Archive")
        self.toolbar.addWidget(self.filter_combo)

    def _create_main_view(self):
        """Erstellt die Hauptansicht mit Verzeichnisbaum und Dateiliste."""
        # Splitter für Verzeichnisbaum und Hauptbereich
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_layout.addWidget(self.splitter)

        # Verzeichnisbaum
        self.tree_view = QTreeView()
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setMinimumWidth(200)
        self.splitter.addWidget(self.tree_view)

        # Rechter Bereich mit Tabs
        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout(self.right_panel)
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.splitter.addWidget(self.right_panel)

        # Tab-Widget
        self.tab_widget = QTabWidget()
        self.right_layout.addWidget(self.tab_widget)

        # Dateien-Tab
        self.files_widget = QWidget()
        self.files_layout = QVBoxLayout(self.files_widget)
        self.files_layout.setContentsMargins(0, 0, 0, 0)

        # Dateiliste
        self.list_view = QListView()
        self.list_view.setViewMode(QListView.ViewMode.IconMode)
        self.list_view.setIconSize(QSize(48, 48))
        self.list_view.setGridSize(QSize(120, 120))
        self.list_view.setResizeMode(QListView.ResizeMode.Adjust)
        self.list_view.setWrapping(True)
        self.files_layout.addWidget(self.list_view)

        self.tab_widget.addTab(self.files_widget, "Dateien")

        # Analyse-Tab
        self.analysis_widget = QWidget()
        self.analysis_layout = QVBoxLayout(self.analysis_widget)

        self.analysis_label = QLabel("Wählen Sie eine Datei aus, um sie zu analysieren.")
        self.analysis_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.analysis_layout.addWidget(self.analysis_label)

        self.tab_widget.addTab(self.analysis_widget, "Analyse")

        # Duplikate-Tab
        self.duplicates_widget = QWidget()
        self.duplicates_layout = QVBoxLayout(self.duplicates_widget)

        self.duplicates_label = QLabel("Klicken Sie auf 'Duplikate finden', um nach Duplikaten zu suchen.")
        self.duplicates_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.duplicates_layout.addWidget(self.duplicates_label)

        self.tab_widget.addTab(self.duplicates_widget, "Duplikate")
        # Dateiorganisation-Tab
        self.organizer_widget = FileOrganizerWidget()
        self.tab_widget.addTab(self.organizer_widget, "Dateiorganisation")

        # Dateivorschau-Tab
        self.preview_widget = FilePreviewWidget()
        self.tab_widget.addTab(self.preview_widget, "Dateivorschau")
        # Splitter-Verhältnis setzen
        self.splitter.setSizes([int(self.width() * 0.3), int(self.width() * 0.7)])

    def _create_statusbar(self):
        """Erstellt die Statusleiste."""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Fortschrittsbalken
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(150)
        self.progress_bar.setVisible(False)
        self.statusbar.addPermanentWidget(self.progress_bar)

        # Standard-Statustext
        self.statusbar.showMessage("Bereit")

    def _initialize_file_system_model(self):
        """Initialisiert das Dateisystem-Modell."""
        self.file_system_model = QFileSystemModel()
        self.file_system_model.setRootPath(QDir.homePath())

        # Setze Filter
        self.file_system_model.setFilter(QDir.Filter.NoDotAndDotDot | QDir.Filter.AllEntries)

        # Verbinde Modell mit Views
        self.tree_view.setModel(self.file_system_model)
        self.list_view.setModel(self.file_system_model)

        # Verstecke alle Spalten außer dem Namen im Tree View
        for i in range(1, self.file_system_model.columnCount()):
            self.tree_view.hideColumn(i)

        # Setze Wurzelindex für Tree View
        root_index = self.file_system_model.index(QDir.homePath())
        self.tree_view.setRootIndex(root_index)

        # Setze anfänglichen Pfad für List View
        self.list_view.setRootIndex(root_index)

    def _connect_signals(self):
        """Verbindet Signale mit Slots."""
        # Toolbar-Aktionen
        self.action_open.triggered.connect(self.open_directory)
        self.action_refresh.triggered.connect(self.refresh_view)
        self.action_up.triggered.connect(self.navigate_up)
        self.action_organize.triggered.connect(self.organize_files)
        self.action_duplicates.triggered.connect(self.find_duplicates)

        # Tree View
        self.tree_view.clicked.connect(self.tree_item_clicked)

        # List View
        self.list_view.doubleClicked.connect(self.list_item_double_clicked)
        self.list_view.clicked.connect(self.list_item_clicked)

        # Suchfeld
        self.search_field.textChanged.connect(self.search_files)

        # Filter-Dropdown
        self.filter_combo.currentIndexChanged.connect(self.apply_filter)

    def open_directory(self):
        """Öffnet einen Verzeichnisauswahldialog."""
        directory = QFileDialog.getExistingDirectory(
            self, "Verzeichnis öffnen", QDir.homePath(),
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks
        )

        if directory:
            self.set_current_directory(directory)

    def set_current_directory(self, directory):
        """Setzt das aktuelle Verzeichnis."""
        index = self.file_system_model.index(directory)
        if index.isValid():
            # Aktualisiere Tree View
            self.tree_view.setCurrentIndex(index)
            self.tree_view.expand(index)

            # Aktualisiere List View
            self.list_view.setRootIndex(index)

            # Aktualisiere Statusleiste
            self.statusbar.showMessage(f"Verzeichnis: {directory}")

    def refresh_view(self):
        """Aktualisiert die Ansicht."""
        self.file_system_model.setRootPath(self.file_system_model.rootPath())
        self.statusbar.showMessage("Ansicht aktualisiert")

    def navigate_up(self):
        """Navigiert zum übergeordneten Verzeichnis."""
        current_index = self.list_view.rootIndex()
        parent_index = current_index.parent()

        if parent_index.isValid():
            self.list_view.setRootIndex(parent_index)
            self.tree_view.setCurrentIndex(parent_index)

            parent_path = self.file_system_model.filePath(parent_index)
            self.statusbar.showMessage(f"Verzeichnis: {parent_path}")

    def tree_item_clicked(self, index):
        """Behandelt Klicks im Verzeichnisbaum."""
        path = self.file_system_model.filePath(index)

        if self.file_system_model.isDir(index):
            self.list_view.setRootIndex(index)
            self.statusbar.showMessage(f"Verzeichnis: {path}")

    def list_item_double_clicked(self, index):
        """Behandelt Doppelklicks in der Dateiliste."""
        path = self.file_system_model.filePath(index)

        if self.file_system_model.isDir(index):
            # Wenn es ein Verzeichnis ist, navigiere hinein
            self.list_view.setRootIndex(index)
            self.tree_view.setCurrentIndex(index)
            self.statusbar.showMessage(f"Verzeichnis: {path}")
        else:
            # Wenn es eine Datei ist, öffne sie mit dem Standardprogramm
            # In einer vollständigen Implementierung würde hier die Datei geöffnet werden
            self.statusbar.showMessage(f"Datei ausgewählt: {path}")
            self.show_file_analysis(path)

    def list_item_clicked(self, index):
        """Behandelt Klicks in der Dateiliste."""
        path = self.file_system_model.filePath(index)
        self.statusbar.showMessage(f"Ausgewählt: {path}")
        print("DEBUG: Geklickt auf:", path)  # ← Temporärer Check

        if not self.file_system_model.isDir(index):
            # 1. Zeige Analyse
            self.show_file_analysis(path)

            # 2. Zeige Vorschau im Tab
            self.preview_widget.set_file(path)
            self.tab_widget.setCurrentWidget(self.preview_widget)

    def search_files(self, text):
        """Sucht nach Dateien basierend auf dem Suchtext."""
        if not text:
            # Wenn das Suchfeld leer ist, zeige alle Dateien
            self.file_system_model.setNameFilters([])
            self.file_system_model.setNameFilterDisables(True)
        else:
            # Andernfalls filtere nach dem Suchtext
            self.file_system_model.setNameFilters([f"*{text}*"])
            self.file_system_model.setNameFilterDisables(False)

    def apply_filter(self, index):
        """Wendet den ausgewählten Filter an."""
        filter_text = self.filter_combo.currentText()

        if filter_text == "Alle Dateien":
            self.file_system_model.setNameFilters([])
            self.file_system_model.setNameFilterDisables(True)
        elif filter_text == "Dokumente":
            self.file_system_model.setNameFilters(["*.txt", "*.pdf", "*.docx", "*.doc", "*.rtf", "*.odt"])
            self.file_system_model.setNameFilterDisables(False)
        elif filter_text == "Bilder":
            self.file_system_model.setNameFilters(["*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp", "*.svg"])
            self.file_system_model.setNameFilterDisables(False)
        elif filter_text == "Videos":
            self.file_system_model.setNameFilters(["*.mp4", "*.mkv", "*.mov", "*.avi", "*.wmv"])
            self.file_system_model.setNameFilterDisables(False)
        elif filter_text == "Audio":
            self.file_system_model.setNameFilters(["*.mp3", "*.wav", "*.flac", "*.m4a", "*.ogg"])
            self.file_system_model.setNameFilterDisables(False)
        elif filter_text == "Archive":
            self.file_system_model.setNameFilters(["*.zip", "*.rar", "*.7z", "*.tar", "*.gz"])
            self.file_system_model.setNameFilterDisables(False)

    def show_file_analysis(self, file_path):
        """Zeigt die Analyse einer Datei an."""
        # In einer vollständigen Implementierung würde hier die Dateianalyse durchgeführt werden
        # Für dieses Beispiel zeigen wir nur grundlegende Informationen an

        file_info = QFileInfo(file_path)

        # Erstelle Analyse-Text
        analysis_text = f"""
        <h2>{file_info.fileName()}</h2>
        <p><b>Pfad:</b> {file_path}</p>
        <p><b>Größe:</b> {self.format_size(file_info.size())}</p>
        <p><b>Erstellt:</b> {file_info.birthTime().toString()}</p>
        <p><b>Zuletzt geändert:</b> {file_info.lastModified().toString()}</p>
        <p><b>Zuletzt gelesen:</b> {file_info.lastRead().toString()}</p>
        <p><b>Typ:</b> {self.get_file_type(file_info.suffix())}</p>
        """

        # Aktualisiere Analyse-Tab
        self.analysis_label.setText(analysis_text)

        # Wechsle zum Analyse-Tab
        self.tab_widget.setCurrentIndex(1)

    def organize_files(self):
        """Organisiert Dateien im aktuellen Verzeichnis."""
        current_path = self.file_system_model.filePath(self.list_view.rootIndex())

        # Zeige Dialog mit Organisationsoptionen
        organize_dialog = QDialog(self)
        organize_dialog.setWindowTitle("Dateien organisieren")
        organize_dialog.setMinimumWidth(400)

        dialog_layout = QVBoxLayout(organize_dialog)

        # Organisationsmethode
        method_label = QLabel("Organisationsmethode:")
        dialog_layout.addWidget(method_label)

        method_combo = QComboBox()
        method_combo.addItem("Nach Dateityp")
        method_combo.addItem("Nach Datum")
        method_combo.addItem("Nach Größe")
        dialog_layout.addWidget(method_combo)

        # Zielverzeichnis
        target_layout = QHBoxLayout()
        target_label = QLabel("Zielverzeichnis:")
        target_layout.addWidget(target_label)

        target_field = QLineEdit(current_path)
        target_layout.addWidget(target_field)

        target_button = QPushButton("...")
        target_button.setMaximumWidth(30)
        target_layout.addWidget(target_button)

        dialog_layout.addLayout(target_layout)

        # Optionen
        move_checkbox = QCheckBox("Dateien verschieben (statt kopieren)")
        move_checkbox.setChecked(True)
        dialog_layout.addWidget(move_checkbox)

        # Buttons
        button_layout = QHBoxLayout()
        cancel_button = QPushButton("Abbrechen")
        organize_button = QPushButton("Organisieren")
        organize_button.setDefault(True)

        button_layout.addWidget(cancel_button)
        button_layout.addWidget(organize_button)

        dialog_layout.addLayout(button_layout)

        # Verbinde Signale
        cancel_button.clicked.connect(organize_dialog.reject)
        organize_button.clicked.connect(organize_dialog.accept)
        target_button.clicked.connect(lambda: self.select_target_directory(target_field))

        # Zeige Dialog
        if organize_dialog.exec() == QDialog.DialogCode.Accepted:
            method = method_combo.currentText()
            target = target_field.text()
            move = move_checkbox.isChecked()

            # In einer vollständigen Implementierung würde hier die Dateiorganisation durchgeführt werden
            QMessageBox.information(
                self, "Dateien organisieren",
                f"Dateien würden nach {method} organisiert werden.\n"
                f"Zielverzeichnis: {target}\n"
                f"Dateien {'verschieben' if move else 'kopieren'}"
            )

            # Aktualisiere Ansicht
            self.refresh_view()

    def find_duplicates(self):
        """Sucht nach Dateiduplikaten im aktuellen Verzeichnis basierend auf Dateihash."""
        current_path = self.file_system_model.filePath(self.list_view.rootIndex())

        # Zeige Fortschrittsbalken
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        QApplication.processEvents()

        try:
            # Sammle alle Dateien im Verzeichnis
            all_files = []
            for root, _, files in os.walk(current_path):
                for file in files:
                    all_files.append(os.path.join(root, file))

            if not all_files:
                self._show_no_files_message(current_path)
                return

            duplicates = {}
            total_files = len(all_files)
            hashing_progress = 0

            # Hash-Berechnung für jede Datei
            for i, file_path in enumerate(all_files):
                try:
                    file_hash = self._calculate_file_hash(file_path)
                    if file_hash in duplicates:
                        duplicates[file_hash].append(file_path)
                    else:
                        duplicates[file_hash] = [file_path]

                    # Fortschritt aktualisieren
                    hashing_progress = int((i + 1) / total_files * 100)
                    self.progress_bar.setValue(hashing_progress)
                    QApplication.processEvents()

                except Exception as e:
                    logging.error(f"Fehler bei Verarbeitung von {file_path}: {e}")

            # Filtere nur echte Duplikate (mehr als eine Datei pro Hash)
            real_duplicates = {h: files for h, files in duplicates.items() if len(files) > 1}

            if not real_duplicates:
                self._show_no_duplicates_message(current_path)
            else:
                self._display_duplicates(real_duplicates)

        except Exception as e:
            logging.error(f"Fehler bei Duplikatsuche: {e}")
            QMessageBox.critical(self, "Fehler", f"Fehler bei der Duplikatsuche:\n{str(e)}")
        finally:
            self.progress_bar.setVisible(False)

    def _calculate_file_hash(self, file_path, chunk_size=8192):
        """Berechnet MD5-Hash einer Datei in Chunks."""
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                md5.update(chunk)
        return md5.hexdigest()

    def _show_no_files_message(self, path):
        """Zeigt Meldung wenn keine Dateien gefunden wurden."""
        self.duplicates_label.setText(f"""
        <h2>Duplikatsuche in {path}</h2>
        <p style='color:red;'>Keine Dateien gefunden!</p>
        """)
        self.tab_widget.setCurrentIndex(2)

    def _show_no_duplicates_message(self, path):
        """Zeigt Meldung wenn keine Duplikate gefunden wurden."""
        self.duplicates_label.setText(f"""
        <h2>Duplikatsuche in {path}</h2>
        <p style='color:green;'>Keine Duplikate gefunden!</p>
        """)
        self.tab_widget.setCurrentIndex(2)

    def _display_duplicates(self, duplicates):
        """Zeigt gefundene Duplikate in einer strukturierten Liste an."""
        html_content = ["<h2>Gefundene Duplikate</h2>"]

        for hash_val, files in duplicates.items():
            html_content.append(f"<h3>Hash: {hash_val}</h3>")
            html_content.append("<ul>")
            for file in files:
                file_size = os.path.getsize(file)
                html_content.append(f"<li>{file} ({self._format_size(file_size)})</li>")
            html_content.append("</ul>")

        self.duplicates_label.setText("\n".join(html_content))
        self.tab_widget.setCurrentIndex(2)

    def _format_size(self, size_bytes):
        """Formatiert Dateigröße in lesbare Einheiten."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} TB"

    def select_target_directory(self, target_field):
        """Öffnet einen Dialog zur Auswahl des Zielverzeichnisses."""
        directory = QFileDialog.getExistingDirectory(
            self, "Zielverzeichnis auswählen", target_field.text(),
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks
        )

        if directory:
            target_field.setText(directory)



    def get_file_type(self, extension):
        """Gibt den Dateityp basierend auf der Erweiterung zurück."""
        extension = extension.lower()

        if extension in ['.txt', '.md', '.pdf', '.docx', '.doc', '.rtf', '.odt']:
            return "Dokument"
        elif extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']:
            return "Bild"
        elif extension in ['.mp4', '.mkv', '.mov', '.avi', '.wmv']:
            return "Video"
        elif extension in ['.mp3', '.wav', '.flac', '.m4a', '.ogg']:
            return "Audio"
        elif extension in ['.csv', '.xlsx', '.xls', '.ods']:
            return "Tabelle"
        elif extension in ['.pptx', '.ppt', '.odp']:
            return "Präsentation"
        elif extension in ['.zip', '.rar', '.7z', '.tar', '.gz']:
            return "Archiv"
        elif extension in ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h', '.php', '.rb']:
            return "Code"
        elif extension in ['.db', '.sqlite', '.sql']:
            return "Datenbank"
        elif extension in ['.env', '.cfg', '.yaml', '.yml', '.ini', '.json', '.xml', '.lock']:
            return "Konfiguration"
        else:
            return "Unbekannt"


# Hauptfunktion
def main():
    app = QApplication(sys.argv)

    # Setze Anwendungsinformationen
    app.setApplicationName("KI-Dateiverwaltung")
    app.setApplicationVersion("0.1.0")

    # Erstelle und zeige Hauptfenster
    window = FileOrganizerUI()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    import time  # Für die Simulation des Fortschritts
    from PyQt6.QtCore import QFileInfo  # Für Dateiinformationen

    main()
