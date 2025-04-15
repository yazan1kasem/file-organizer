import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QFileDialog, QListWidget,
    QTabWidget, QSplitter, QMessageBox, QProgressBar
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont

class FilePreviewWidget(QWidget):
    """
    Widget zur Vorschau verschiedener Dateitypen.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Hauptlayout
        self.layout = QVBoxLayout(self)
        
        # Titel
        self.title_label = QLabel("Dateivorschau")
        self.title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)
        
        # Vorschaubereich
        self.preview_area = QWidget()
        self.preview_layout = QVBoxLayout(self.preview_area)
        
        self.info_label = QLabel("Wählen Sie eine Datei aus, um eine Vorschau anzuzeigen.")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_layout.addWidget(self.info_label)
        
        self.layout.addWidget(self.preview_area)
        
        # Aktionsbereich
        self.action_area = QWidget()
        self.action_layout = QHBoxLayout(self.action_area)
        
        self.open_button = QPushButton("Öffnen")
        self.open_button.setEnabled(False)
        self.action_layout.addWidget(self.open_button)
        
        self.analyze_button = QPushButton("Analysieren")
        self.analyze_button.setEnabled(False)
        self.action_layout.addWidget(self.analyze_button)
        
        self.layout.addWidget(self.action_area)
        
        # Aktueller Dateipfad
        self.current_file_path = None
    
    def set_file(self, file_path):
        """
        Setzt die anzuzeigende Datei.
        
        Args:
            file_path (str): Pfad zur Datei.
        """
        self.current_file_path = file_path
        
        if not file_path or not os.path.isfile(file_path):
            self.clear_preview()
            return
        
        # Aktiviere Buttons
        self.open_button.setEnabled(True)
        self.analyze_button.setEnabled(True)
        
        # Aktualisiere Titel
        self.title_label.setText(f"Vorschau: {os.path.basename(file_path)}")
        
        # Bestimme Dateityp anhand der Erweiterung
        _, extension = os.path.splitext(file_path)
        extension = extension.lower()
        
        # Zeige entsprechende Vorschau
        if extension in ['.txt', '.md', '.py', '.html', '.css', '.js', '.json', '.xml', '.csv']:
            self._show_text_preview(file_path)
        elif extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            self._show_image_preview(file_path)
        elif extension in ['.pdf']:
            self._show_pdf_preview(file_path)
        elif extension in ['.mp3', '.wav', '.flac', '.m4a']:
            self._show_audio_preview(file_path)
        elif extension in ['.mp4', '.mkv', '.mov', '.avi']:
            self._show_video_preview(file_path)
        else:
            self._show_generic_preview(file_path)
    
    def clear_preview(self):
        """Löscht die aktuelle Vorschau."""
        # Lösche alle Widgets im Vorschaubereich
        for i in reversed(range(self.preview_layout.count())):
            widget = self.preview_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Setze Standardtext
        self.info_label = QLabel("Wählen Sie eine Datei aus, um eine Vorschau anzuzeigen.")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_layout.addWidget(self.info_label)
        
        # Deaktiviere Buttons
        self.open_button.setEnabled(False)
        self.analyze_button.setEnabled(False)
        
        # Setze Standardtitel
        self.title_label.setText("Dateivorschau")
        
        # Lösche aktuellen Dateipfad
        self.current_file_path = None
    
    def _show_text_preview(self, file_path):
        """
        Zeigt eine Vorschau für Textdateien.
        
        Args:
            file_path (str): Pfad zur Textdatei.
        """
        # Lösche vorherige Vorschau
        for i in reversed(range(self.preview_layout.count())):
            widget = self.preview_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        try:
            # Lese die ersten 1000 Zeichen der Datei
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(1000)
            
            # Erstelle Vorschau-Label
            preview_label = QLabel(content)
            preview_label.setWordWrap(True)
            preview_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            
            # Füge Label zum Layout hinzu
            self.preview_layout.addWidget(preview_label)
            
        except Exception as e:
            error_label = QLabel(f"Fehler beim Lesen der Datei: {str(e)}")
            error_label.setWordWrap(True)
            self.preview_layout.addWidget(error_label)
    
    def _show_image_preview(self, file_path):
        """
        Zeigt eine Vorschau für Bilddateien.
        
        Args:
            file_path (str): Pfad zur Bilddatei.
        """
        # Lösche vorherige Vorschau
        for i in reversed(range(self.preview_layout.count())):
            widget = self.preview_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        try:
            # In einer vollständigen Implementierung würde hier ein QPixmap verwendet werden
            # Für dieses Beispiel zeigen wir nur einen Platzhaltertext an
            preview_label = QLabel("Bildvorschau würde hier angezeigt werden.")
            preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Füge Label zum Layout hinzu
            self.preview_layout.addWidget(preview_label)
            
        except Exception as e:
            error_label = QLabel(f"Fehler beim Anzeigen des Bildes: {str(e)}")
            error_label.setWordWrap(True)
            self.preview_layout.addWidget(error_label)
    
    def _show_pdf_preview(self, file_path):
        """
        Zeigt eine Vorschau für PDF-Dateien.
        
        Args:
            file_path (str): Pfad zur PDF-Datei.
        """
        # Lösche vorherige Vorschau
        for i in reversed(range(self.preview_layout.count())):
            widget = self.preview_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # In einer vollständigen Implementierung würde hier ein PDF-Renderer verwendet werden
        # Für dieses Beispiel zeigen wir nur einen Platzhaltertext an
        preview_label = QLabel("PDF-Vorschau würde hier angezeigt werden.")
        preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Füge Label zum Layout hinzu
        self.preview_layout.addWidget(preview_label)
    
    def _show_audio_preview(self, file_path):
        """
        Zeigt eine Vorschau für Audiodateien.
        
        Args:
            file_path (str): Pfad zur Audiodatei.
        """
        # Lösche vorherige Vorschau
        for i in reversed(range(self.preview_layout.count())):
            widget = self.preview_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # In einer vollständigen Implementierung würde hier ein Audio-Player verwendet werden
        # Für dieses Beispiel zeigen wir nur einen Platzhaltertext an
        preview_label = QLabel("Audio-Vorschau würde hier angezeigt werden.")
        preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Füge Label zum Layout hinzu
        self.preview_layout.addWidget(preview_label)
    
    def _show_video_preview(self, file_path):
        """
        Zeigt eine Vorschau für Videodateien.
        
        Args:
            file_path (str): Pfad zur Videodatei.
        """
        # Lösche vorherige Vorschau
        for i in reversed(range(self.preview_layout.count())):
            widget = self.preview_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # In einer vollständigen Implementierung würde hier ein Video-Player verwendet werden
        # Für dieses Beispiel zeigen wir nur einen Platzhaltertext an
        preview_label = QLabel("Video-Vorschau würde hier angezeigt werden.")
        preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Füge Label zum Layout hinzu
        self.preview_layout.addWidget(preview_label)
    
    def _show_generic_preview(self, file_path):
        """
        Zeigt eine generische Vorschau für nicht speziell unterstützte Dateitypen.
        
        Args:
            file_path (str): Pfad zur Datei.
        """
        # Lösche vorherige Vorschau
        for i in reversed(range(self.preview_layout.count())):
            widget = self.preview_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Zeige Dateiinformationen an
        file_stat = os.stat(file_path)
        file_size = self._format_size(file_stat.st_size)
        
        info_text = f"""
        <b>Dateiname:</b> {os.path.basename(file_path)}<br>
        <b>Pfad:</b> {file_path}<br>
        <b>Größe:</b> {file_size}<br>
        <b>Erstellt:</b> {self._format_time(file_stat.st_ctime)}<br>
        <b>Zuletzt geändert:</b> {self._format_time(file_stat.st_mtime)}<br>
        <b>Zuletzt zugegriffen:</b> {self._format_time(file_stat.st_atime)}<br>
        """
        
        preview_label = QLabel(info_text)
        preview_label.setTextFormat(Qt.TextFormat.RichText)
        preview_label.setWordWrap(True)
        preview_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        
        # Füge Label zum Layout hinzu
        self.preview_layout.addWidget(preview_label)
    
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
    
    def _format_time(self, timestamp):
        """
        Formatiert einen Zeitstempel in eine lesbare Form.
        
        Args:
            timestamp (float): Zeitstempel.
            
        Returns:
            str: Formatierte Zeit.
        """
        from datetime import datetime
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# Beispiel für die Verwendung
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = QWidget()
    window.setWindowTitle("Dateivorschau-Test")
    window.setMinimumSize(600, 400)
    
    layout = QVBoxLayout(window)
    
    preview_widget = FilePreviewWidget()
    layout.addWidget(preview_widget)
    
    # Button zum Auswählen einer Datei
    select_button = QPushButton("Datei auswählen")
    
    def select_file():
        file_path, _ = QFileDialog.getOpenFileName(window, "Datei auswählen")
        if file_path:
            preview_widget.set_file(file_path)
    
    select_button.clicked.connect(select_file)
    layout.addWidget(select_button)
    
    window.show()
    
    sys.exit(app.exec())
