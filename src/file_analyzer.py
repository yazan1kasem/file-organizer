import os
import sys
import logging
from pathlib import Path

# Konfiguration des Logging-Systems
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("file_analyzer")

class FileAnalyzer:
    """
    Klasse zur Analyse von Dateien und deren Inhalten.
    """
    def __init__(self, supported_extensions=None):
        """
        Initialisiert den FileAnalyzer.
        
        Args:
            supported_extensions (dict, optional): Wörterbuch mit unterstützten Dateierweiterungen.
        """
        self.logger = logger
        
        # Standardmäßig unterstützte Dateierweiterungen
        self.supported_extensions = supported_extensions or {
            "text": [".txt", ".md", ".pdf", ".docx", ".json", ".py", ".html", ".ipynb"],
            "image": [".jpg", ".jpeg", ".png", ".svg", ".raw", ".webp", ".gif"],
            "video": [".mp4", ".mkv", ".mov", ".avi"],
            "audio": [".mp3", ".wav", ".flac", ".m4a"],
            "data": [".csv", ".xlsx", ".parquet", ".sav", ".tsv"],
            "archive": [".zip", ".rar", ".7z", ".iso"],
            "config": [".env", ".cfg", ".yaml", ".yml", ".ini", ".lock"],
            "model": [".pt", ".onnx", ".h5", ".pkl", ".npy"],
            "other": [".log", ".tmp", ".db", ".torrent", ".bak"]
        }
    
    def analyze_file(self, file_path):
        """
        Analysiert eine Datei und gibt Metadaten zurück.
        
        Args:
            file_path (str): Pfad zur zu analysierenden Datei.
            
        Returns:
            dict: Metadaten der Datei.
        """
        self.logger.info(f"Analysiere Datei: {file_path}")
        
        try:
            path = Path(file_path)
            if not path.exists() or not path.is_file():
                self.logger.error(f"Datei existiert nicht oder ist keine Datei: {file_path}")
                return {"error": "Datei nicht gefunden"}
            
            # Grundlegende Metadaten
            stats = path.stat()
            metadata = {
                "path": str(path),
                "name": path.name,
                "size": stats.st_size,
                "created": stats.st_ctime,
                "modified": stats.st_mtime,
                "accessed": stats.st_atime,
                "extension": path.suffix.lower(),
                "type": self._get_file_type(path.suffix.lower()),
                "mime_type": self._get_mime_type(path)
            }
            
            # Erweiterte Analyse basierend auf Dateityp
            if metadata["type"] == "text":
                self._analyze_text_file(path, metadata)
            elif metadata["type"] == "image":
                self._analyze_image_file(path, metadata)
            elif metadata["type"] == "audio":
                self._analyze_audio_file(path, metadata)
            elif metadata["type"] == "video":
                self._analyze_video_file(path, metadata)
            elif metadata["type"] == "data":
                self._analyze_data_file(path, metadata)
            
            return metadata
            
        except Exception as e:
            self.logger.error(f"Fehler bei der Dateianalyse: {e}")
            return {"error": str(e)}
    
    def _get_file_type(self, extension):
        """
        Bestimmt den Dateityp anhand der Erweiterung.
        
        Args:
            extension (str): Dateierweiterung.
            
        Returns:
            str: Dateityp.
        """
        for file_type, extensions in self.supported_extensions.items():
            if extension in extensions:
                return file_type
        return "unknown"
    
    def _get_mime_type(self, file_path):
        """
        Bestimmt den MIME-Typ einer Datei.
        
        Args:
            file_path (Path): Pfad zur Datei.
            
        Returns:
            str: MIME-Typ der Datei.
        """
        # In einer vollständigen Implementierung würde hier python-magic verwendet werden
        # Für dieses Beispiel verwenden wir eine einfache Zuordnung basierend auf der Erweiterung
        extension_to_mime = {
            ".txt": "text/plain",
            ".md": "text/markdown",
            ".pdf": "application/pdf",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".json": "application/json",
            ".py": "text/x-python",
            ".html": "text/html",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".svg": "image/svg+xml",
            ".mp4": "video/mp4",
            ".mp3": "audio/mpeg",
            ".wav": "audio/wav",
            ".csv": "text/csv",
            ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ".zip": "application/zip"
        }
        
        return extension_to_mime.get(file_path.suffix.lower(), "application/octet-stream")
    
    def _analyze_text_file(self, file_path, metadata):
        """
        Analysiert eine Textdatei.
        
        Args:
            file_path (Path): Pfad zur Textdatei.
            metadata (dict): Metadaten-Dictionary, das aktualisiert wird.
        """
        try:
            # Zähle Zeilen, Wörter und Zeichen
            line_count = 0
            word_count = 0
            char_count = 0
            
            # Lese nur die ersten 1000 Zeilen für die Analyse
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for i, line in enumerate(f):
                    if i >= 1000:  # Begrenze die Analyse auf 1000 Zeilen
                        break
                    line_count += 1
                    word_count += len(line.split())
                    char_count += len(line)
            
            metadata.update({
                "line_count": line_count,
                "word_count": word_count,
                "char_count": char_count,
                "is_binary": False
            })
            
            # Extrahiere Vorschau (erste 500 Zeichen)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                preview = f.read(500)
                metadata["preview"] = preview
                
        except UnicodeDecodeError:
            # Wenn die Datei nicht als Text gelesen werden kann, ist sie wahrscheinlich binär
            metadata.update({
                "is_binary": True,
                "preview": None
            })
    
    def _analyze_image_file(self, file_path, metadata):
        """
        Analysiert eine Bilddatei.
        
        Args:
            file_path (Path): Pfad zur Bilddatei.
            metadata (dict): Metadaten-Dictionary, das aktualisiert wird.
        """
        # In einer vollständigen Implementierung würde hier Pillow verwendet werden
        # Für dieses Beispiel fügen wir nur einen Platzhalter hinzu
        metadata.update({
            "image_info": {
                "width": "nicht verfügbar",
                "height": "nicht verfügbar",
                "format": file_path.suffix.lower().replace(".", ""),
                "mode": "nicht verfügbar"
            }
        })
    
    def _analyze_audio_file(self, file_path, metadata):
        """
        Analysiert eine Audiodatei.
        
        Args:
            file_path (Path): Pfad zur Audiodatei.
            metadata (dict): Metadaten-Dictionary, das aktualisiert wird.
        """
        # In einer vollständigen Implementierung würde hier librosa verwendet werden
        # Für dieses Beispiel fügen wir nur einen Platzhalter hinzu
        metadata.update({
            "audio_info": {
                "duration": "nicht verfügbar",
                "sample_rate": "nicht verfügbar",
                "channels": "nicht verfügbar"
            }
        })
    
    def _analyze_video_file(self, file_path, metadata):
        """
        Analysiert eine Videodatei.
        
        Args:
            file_path (Path): Pfad zur Videodatei.
            metadata (dict): Metadaten-Dictionary, das aktualisiert wird.
        """
        # In einer vollständigen Implementierung würde hier moviepy verwendet werden
        # Für dieses Beispiel fügen wir nur einen Platzhalter hinzu
        metadata.update({
            "video_info": {
                "duration": "nicht verfügbar",
                "resolution": "nicht verfügbar",
                "fps": "nicht verfügbar",
                "codec": "nicht verfügbar"
            }
        })
    
    def _analyze_data_file(self, file_path, metadata):
        """
        Analysiert eine Datendatei.
        
        Args:
            file_path (Path): Pfad zur Datendatei.
            metadata (dict): Metadaten-Dictionary, das aktualisiert wird.
        """
        # In einer vollständigen Implementierung würde hier pandas verwendet werden
        # Für dieses Beispiel fügen wir nur einen Platzhalter hinzu
        metadata.update({
            "data_info": {
                "rows": "nicht verfügbar",
                "columns": "nicht verfügbar",
                "format": file_path.suffix.lower().replace(".", "")
            }
        })
    
    def generate_preview(self, file_path):
        """
        Generiert eine Vorschau für eine Datei.
        
        Args:
            file_path (str): Pfad zur Datei.
            
        Returns:
            dict: Vorschauinformationen.
        """
        self.logger.info(f"Generiere Vorschau für: {file_path}")
        
        metadata = self.analyze_file(file_path)
        if "error" in metadata:
            return metadata
        
        preview = {"metadata": metadata, "content": None}
        
        try:
            file_type = metadata["type"]
            
            if file_type == "text":
                # Für Textdateien: Zeige die ersten 1000 Zeichen
                if not metadata.get("is_binary", False):
                    preview["content"] = metadata.get("preview", "")
            
            elif file_type == "image":
                # Für Bilder: In einer vollständigen Implementierung würde hier ein Thumbnail erstellt werden
                preview["content"] = "Bildvorschau nicht verfügbar"
            
            elif file_type == "audio":
                # Für Audiodateien: In einer vollständigen Implementierung würde hier eine Wellenform erstellt werden
                preview["content"] = "Audiovorschau nicht verfügbar"
            
            elif file_type == "video":
                # Für Videodateien: In einer vollständigen Implementierung würde hier ein Thumbnail erstellt werden
                preview["content"] = "Videovorschau nicht verfügbar"
            
            elif file_type == "data":
                # Für Datendateien: In einer vollständigen Implementierung würden hier die ersten Zeilen angezeigt werden
                preview["content"] = "Datenvorschau nicht verfügbar"
            
            return preview
            
        except Exception as e:
            self.logger.error(f"Fehler bei der Vorschauerstellung: {e}")
            return {"error": str(e), "metadata": metadata}

# Beispiel für die Verwendung
if __name__ == "__main__":
    analyzer = FileAnalyzer()
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(f"Analysiere Datei: {file_path}")
        metadata = analyzer.analyze_file(file_path)
        print("Metadaten:")
        for key, value in metadata.items():
            print(f"  {key}: {value}")
        
        print("\nVorschau:")
        preview = analyzer.generate_preview(file_path)
        if "error" not in preview:
            print(preview.get("content", "Keine Vorschau verfügbar"))
    else:
        print("Bitte geben Sie einen Dateipfad als Argument an.")
