import os
import sys
import logging
from pathlib import Path
import shutil

# Konfiguration des Logging-Systems
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("file_manager")

class FileManager:
    """
    Klasse zur intelligenten Verwaltung und Organisation von Dateien.
    """
    def __init__(self):
        """
        Initialisiert den FileManager.
        """
        self.logger = logger
    
    def organize_by_type(self, directory_path, target_directory=None, move_files=True):
        """
        Organisiert Dateien nach ihrem Typ.
        
        Args:
            directory_path (str): Pfad zum zu organisierenden Verzeichnis.
            target_directory (str, optional): Zielverzeichnis für die organisierten Dateien.
            move_files (bool): Ob Dateien verschoben oder kopiert werden sollen.
            
        Returns:
            dict: Ergebnis der Organisationsoperation.
        """
        self.logger.info(f"Organisiere Dateien nach Typ in: {directory_path}")
        
        if target_directory is None:
            target_directory = directory_path
        
        result = {
            "organized_files": 0,
            "skipped_files": 0,
            "errors": []
        }
        
        try:
            directory = Path(directory_path)
            target = Path(target_directory)
            
            if not directory.exists() or not directory.is_dir():
                self.logger.error(f"Quellverzeichnis existiert nicht oder ist kein Verzeichnis: {directory_path}")
                result["errors"].append(f"Quellverzeichnis ungültig: {directory_path}")
                return result
            
            if not target.exists():
                target.mkdir(parents=True)
            
            # Definiere Dateitypen und ihre Erweiterungen
            file_types = {
                "Dokumente": [".txt", ".md", ".pdf", ".docx", ".doc", ".rtf", ".odt"],
                "Bilder": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".raw", ".webp"],
                "Videos": [".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv", ".webm"],
                "Audio": [".mp3", ".wav", ".flac", ".m4a", ".ogg", ".aac"],
                "Tabellen": [".csv", ".xlsx", ".xls", ".ods"],
                "Präsentationen": [".pptx", ".ppt", ".odp"],
                "Archive": [".zip", ".rar", ".7z", ".tar", ".gz", ".iso"],
                "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h", ".php", ".rb"],
                "Datenbanken": [".db", ".sqlite", ".sql"],
                "Konfiguration": [".env", ".cfg", ".yaml", ".yml", ".ini", ".json", ".xml", ".lock"]
            }
            
            # Sammle alle Dateien
            for file_path in directory.glob("*"):
                if not file_path.is_file():
                    continue
                
                # Bestimme Dateityp anhand der Erweiterung
                file_type = "Sonstiges"  # Standardtyp
                extension = file_path.suffix.lower()
                
                for type_name, extensions in file_types.items():
                    if extension in extensions:
                        file_type = type_name
                        break
                
                # Erstelle Zielverzeichnis für diesen Dateityp
                type_dir = target / file_type
                if not type_dir.exists():
                    type_dir.mkdir(parents=True)
                
                # Zieldatei
                target_file = type_dir / file_path.name
                
                # Überspringe, wenn Datei bereits im richtigen Verzeichnis ist
                if str(file_path.parent) == str(type_dir):
                    result["skipped_files"] += 1
                    continue
                
                # Überspringe, wenn Zieldatei bereits existiert
                if target_file.exists():
                    result["skipped_files"] += 1
                    self.logger.warning(f"Zieldatei existiert bereits: {target_file}")
                    continue
                
                try:
                    # Verschiebe oder kopiere Datei
                    if move_files:
                        shutil.move(str(file_path), str(target_file))
                    else:
                        shutil.copy2(str(file_path), str(target_file))
                    
                    result["organized_files"] += 1
                    self.logger.info(f"Datei {'verschoben' if move_files else 'kopiert'}: {file_path} -> {target_file}")
                except Exception as e:
                    error_msg = f"Fehler beim {'Verschieben' if move_files else 'Kopieren'} von {file_path}: {e}"
                    self.logger.error(error_msg)
                    result["errors"].append(error_msg)
            
            self.logger.info(f"Organisation abgeschlossen: {result['organized_files']} Dateien organisiert")
            return result
            
        except Exception as e:
            self.logger.error(f"Fehler bei der Dateiorganisation: {e}")
            result["errors"].append(str(e))
            return result
    
    def organize_by_date(self, directory_path, target_directory=None, date_format="year_month", move_files=True):
        """
        Organisiert Dateien nach ihrem Änderungsdatum.
        
        Args:
            directory_path (str): Pfad zum zu organisierenden Verzeichnis.
            target_directory (str, optional): Zielverzeichnis für die organisierten Dateien.
            date_format (str): Format der Datumsorganisation ("year_month", "year", "year_month_day").
            move_files (bool): Ob Dateien verschoben oder kopiert werden sollen.
            
        Returns:
            dict: Ergebnis der Organisationsoperation.
        """
        self.logger.info(f"Organisiere Dateien nach Datum in: {directory_path}")
        
        if target_directory is None:
            target_directory = directory_path
        
        result = {
            "organized_files": 0,
            "skipped_files": 0,
            "errors": []
        }
        
        try:
            directory = Path(directory_path)
            target = Path(target_directory)
            
            if not directory.exists() or not directory.is_dir():
                self.logger.error(f"Quellverzeichnis existiert nicht oder ist kein Verzeichnis: {directory_path}")
                result["errors"].append(f"Quellverzeichnis ungültig: {directory_path}")
                return result
            
            if not target.exists():
                target.mkdir(parents=True)
            
            # Sammle alle Dateien
            for file_path in directory.glob("*"):
                if not file_path.is_file():
                    continue
                
                # Hole Änderungsdatum
                mod_time = file_path.stat().st_mtime
                mod_date = datetime.fromtimestamp(mod_time)
                
                # Bestimme Zielverzeichnis basierend auf Datumsformat
                if date_format == "year":
                    date_dir = str(mod_date.year)
                elif date_format == "year_month_day":
                    date_dir = f"{mod_date.year}/{mod_date.month:02d}/{mod_date.day:02d}"
                else:  # year_month
                    date_dir = f"{mod_date.year}/{mod_date.month:02d}"
                
                # Erstelle Zielverzeichnis
                type_dir = target / date_dir
                if not type_dir.exists():
                    type_dir.mkdir(parents=True)
                
                # Zieldatei
                target_file = type_dir / file_path.name
                
                # Überspringe, wenn Datei bereits im richtigen Verzeichnis ist
                if str(file_path.parent) == str(type_dir):
                    result["skipped_files"] += 1
                    continue
                
                # Überspringe, wenn Zieldatei bereits existiert
                if target_file.exists():
                    result["skipped_files"] += 1
                    self.logger.warning(f"Zieldatei existiert bereits: {target_file}")
                    continue
                
                try:
                    # Verschiebe oder kopiere Datei
                    if move_files:
                        shutil.move(str(file_path), str(target_file))
                    else:
                        shutil.copy2(str(file_path), str(target_file))
                    
                    result["organized_files"] += 1
                    self.logger.info(f"Datei {'verschoben' if move_files else 'kopiert'}: {file_path} -> {target_file}")
                except Exception as e:
                    error_msg = f"Fehler beim {'Verschieben' if move_files else 'Kopieren'} von {file_path}: {e}"
                    self.logger.error(error_msg)
                    result["errors"].append(error_msg)
            
            self.logger.info(f"Organisation abgeschlossen: {result['organized_files']} Dateien organisiert")
            return result
            
        except Exception as e:
            self.logger.error(f"Fehler bei der Dateiorganisation: {e}")
            result["errors"].append(str(e))
            return result
    
    def organize_by_size(self, directory_path, target_directory=None, move_files=True):
        """
        Organisiert Dateien nach ihrer Größe.
        
        Args:
            directory_path (str): Pfad zum zu organisierenden Verzeichnis.
            target_directory (str, optional): Zielverzeichnis für die organisierten Dateien.
            move_files (bool): Ob Dateien verschoben oder kopiert werden sollen.
            
        Returns:
            dict: Ergebnis der Organisationsoperation.
        """
        self.logger.info(f"Organisiere Dateien nach Größe in: {directory_path}")
        
        if target_directory is None:
            target_directory = directory_path
        
        result = {
            "organized_files": 0,
            "skipped_files": 0,
            "errors": []
        }
        
        try:
            directory = Path(directory_path)
            target = Path(target_directory)
            
            if not directory.exists() or not directory.is_dir():
                self.logger.error(f"Quellverzeichnis existiert nicht oder ist kein Verzeichnis: {directory_path}")
                result["errors"].append(f"Quellverzeichnis ungültig: {directory_path}")
                return result
            
            if not target.exists():
                target.mkdir(parents=True)
            
            # Definiere Größenkategorien
            size_categories = {
                "Winzig (< 10 KB)": 10 * 1024,
                "Klein (< 1 MB)": 1024 * 1024,
                "Mittel (< 10 MB)": 10 * 1024 * 1024,
                "Groß (< 100 MB)": 100 * 1024 * 1024,
                "Sehr groß (< 1 GB)": 1024 * 1024 * 1024,
                "Riesig (≥ 1 GB)": float('inf')
            }
            
            # Sammle alle Dateien
            for file_path in directory.glob("*"):
                if not file_path.is_file():
                    continue
                
                # Hole Dateigröße
                file_size = file_path.stat().st_size
                
                # Bestimme Größenkategorie
                size_category = "Sonstige"
                for category, max_size in size_categories.items():
                    if file_size < max_size:
                        size_category = category
                        break
                
                # Erstelle Zielverzeichnis
                type_dir = target / size_category
                if not type_dir.exists():
                    type_dir.mkdir(parents=True)
                
                # Zieldatei
                target_file = type_dir / file_path.name
                
                # Überspringe, wenn Datei bereits im richtigen Verzeichnis ist
                if str(file_path.parent) == str(type_dir):
                    result["skipped_files"] += 1
                    continue
                
                # Überspringe, wenn Zieldatei bereits existiert
                if target_file.exists():
                    result["skipped_files"] += 1
                    self.logger.warning(f"Zieldatei existiert bereits: {target_file}")
                    continue
                
                try:
                    # Verschiebe oder kopiere Datei
                    if move_files:
                        shutil.move(str(file_path), str(target_file))
                    else:
                        shutil.copy2(str(file_path), str(target_file))
                    
                    result["organized_files"] += 1
                    self.logger.info(f"Datei {'verschoben' if move_files else 'kopiert'}: {file_path} -> {target_file}")
                except Exception as e:
                    error_msg = f"Fehler beim {'Verschieben' if move_files else 'Kopieren'} von {file_path}: {e}"
                    self.logger.error(error_msg)
                    result["errors"].append(error_msg)
            
            self.logger.info(f"Organisation abgeschlossen: {result['organized_files']} Dateien organisiert")
            return result
            
        except Exception as e:
            self.logger.error(f"Fehler bei der Dateiorganisation: {e}")
            result["errors"].append(str(e))
            return result
    
    def rename_files(self, directory_path, pattern, replacement, recursive=False):
        """
        Benennt Dateien in einem Verzeichnis um.
        
        Args:
            directory_path (str): Pfad zum Verzeichnis.
            pattern (str): Muster, das ersetzt werden soll.
            replacement (str): Ersetzungstext.
            recursive (bool): Ob Unterverzeichnisse rekursiv durchsucht werden sollen.
            
        Returns:
            dict: Ergebnis der Umbenennungsoperation.
        """
        self.logger.info(f"Benenne Dateien in {directory_path} um: {pattern} -> {replacement}")
        
        result = {
            "renamed_files": 0,
            "skipped_files": 0,
            "errors": []
        }
        
        try:
            directory = Path(directory_path)
            if not directory.exists() or not directory.is_dir():
                self.logger.error(f"Verzeichnis existiert nicht oder ist kein Verzeichnis: {directory_path}")
                result["errors"].append(f"Verzeichnis ungültig: {directory_path}")
                return result
            
            # Sammle alle Dateien
            files = []
            if recursive:
                for file_path in directory.glob("**/*"):
                    if file_path.is_file():
                        files.append(file_path)
            else:
                for file_path in directory.glob("*"):
                    if file_path.is_file():
                        files.append(file_path)
            
            # Benenne Dateien um
            for file_path in files:
                old_name = file_path.name
                new_name = old_name.replace(pattern, replacement)
                
                # Überspringe, wenn kein Muster gefunden wurde
                if old_name == new_name:
                    result["skipped_files"] += 1
                    continue
                
                new_path = file_path.parent / new_name
                
                # Überspringe, wenn Zieldatei bereits existiert
                if new_path.exists():
                    result["skipped_files"] += 1
                    self.logger.warning(f"Zieldatei existiert bereits: {new_path}")
                    continue
                
                try:
                    # Benenne Datei um
                    file_path.rename(new_path)
                    result["renamed_files"] += 1
                    self.logger.info(f"Datei umbenannt: {file_path} -> {new_path}")
                except Exception as e:
                    error_msg = f"Fehler beim Umbenennen von {file_path}: {e}"
                    self.logger.error(error_msg)
                    result["errors"].append(error_msg)
            
            self.logger.info(f"Umbenennung abgeschlossen: {result['renamed_files']} Dateien umbenannt")
            return result
            
        except Exception as e:
            self.logger.error(f"Fehler bei der Dateiumbenennung: {e}")
            result["errors"].append(str(e))
            return result
    
    def cleanup_empty_directories(self, directory_path, recursive=True):
        """
        Entfernt leere Verzeichnisse.
        
        Args:
            directory_path (str): Pfad zum zu bereinigenden Verzeichnis.
            recursive (bool): Ob Unterverzeichnisse rekursiv durchsucht werden sollen.
            
        Returns:
            dict: Ergebnis der Bereinigungsoperation.
        """
        self.logger.info(f"Bereinige leere Verzeichnisse in: {directory_path}")
        
        result = {
            "removed_directories": 0,
            "errors": []
        }
        
        try:
            directory = Path(directory_path)
            if not directory.exists() or not directory.is_dir():
                self.logger.error(f"Verzeichnis existiert nicht oder ist kein Verzeichnis: {directory_path}")
                result["errors"].append(f"Verzeichnis ungültig: {directory_path}")
                return result
            
            # Sammle alle Verzeichnisse
            directories = []
            if recursive:
                for dir_path in directory.glob("**"):
                    if dir_path.is_dir() and dir_path != directory:
                        directories.append(dir_path)
            else:
                for dir_path in directory.glob("*"):
                    if dir_path.is_dir():
                        directories.append(dir_path)
            
            # Sortiere Verzeichnisse nach Tiefe (tiefste zuerst)
            directories.sort(key=lambda x: len(str(x).split(os.sep)), reverse=True)
            
            # Entferne leere Verzeichnisse
            for dir_path in directories:
                try:
                    # Prüfe, ob Verzeichnis leer ist
                    if not any(dir_path.iterdir()):
                        dir_path.rmdir()
                        result["removed_directories"] += 1
                        self.logger.info(f"Leeres Verzeichnis entfernt: {dir_path}")
                except Exception as e:
                    error_msg = f"Fehler beim Entfernen von {dir_path}: {e}"
                    self.logger.error(error_msg)
                    result["errors"].append(error_msg)
            
            self.logger.info(f"Bereinigung abgeschlossen: {result['removed_directories']} leere Verzeichnisse entfernt")
            return result
            
        except Exception as e:
            self.logger.error(f"Fehler bei der Verzeichnisbereinigung: {e}")
            result["errors"].append(str(e))
            return result

# Beispiel für die Verwendung
if __name__ == "__main__":
    from datetime import datetime
    
    manager = FileManager()
    
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        print(f"Organisiere Dateien in: {directory}")
        
        # Organisiere nach Typ
        result = manager.organize_by_type(directory, move_files=False)
        print(f"Organisierte Dateien: {result['organized_files']}")
        print(f"Übersprungene Dateien: {result['skipped_files']}")
        if result['errors']:
            print(f"Fehler: {len(result['errors'])}")
    else:
        print("Bitte geben Sie ein Verzeichnis als Argument an.")
