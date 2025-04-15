import os
import sys
import logging
from pathlib import Path
import hashlib

# Konfiguration des Logging-Systems
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("duplicate_detector")

class DuplicateDetector:
    """
    Klasse zur Erkennung von Duplikaten in Dateisystemen.
    """
    def __init__(self):
        """
        Initialisiert den DuplicateDetector.
        """
        self.logger = logger
    
    def find_duplicates(self, directory_path, use_content_hash=True, recursive=True):
        """
        Findet Duplikate in einem Verzeichnis.
        
        Args:
            directory_path (str): Pfad zum zu analysierenden Verzeichnis.
            use_content_hash (bool): Ob der Inhalt der Dateien für den Vergleich gehasht werden soll.
            recursive (bool): Ob Unterverzeichnisse rekursiv durchsucht werden sollen.
            
        Returns:
            dict: Informationen über gefundene Duplikate.
        """
        self.logger.info(f"Suche nach Duplikaten in: {directory_path}")
        
        result = {
            "total_duplicates": 0,
            "duplicate_groups": [],
            "wasted_space": 0
        }
        
        try:
            directory = Path(directory_path)
            if not directory.exists() or not directory.is_dir():
                self.logger.error(f"Verzeichnis existiert nicht oder ist kein Verzeichnis: {directory_path}")
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
            
            self.logger.info(f"Gefundene Dateien: {len(files)}")
            
            # Gruppiere Dateien nach Größe (erster Schritt zur Duplikaterkennung)
            size_groups = {}
            for file_path in files:
                size = file_path.stat().st_size
                if size == 0:  # Überspringe leere Dateien
                    continue
                    
                if size in size_groups:
                    size_groups[size].append(file_path)
                else:
                    size_groups[size] = [file_path]
            
            # Finde Gruppen mit mehr als einer Datei gleicher Größe
            for size, size_files in size_groups.items():
                if len(size_files) > 1:
                    if use_content_hash:
                        # Gruppiere Dateien nach Inhaltshash
                        hash_groups = self._group_by_hash(size_files)
                        
                        # Füge Duplikatgruppen hinzu
                        for file_hash, hash_files in hash_groups.items():
                            if len(hash_files) > 1:
                                duplicate_files = [{"path": str(f), "name": f.name, "size": size} for f in hash_files]
                                result["duplicate_groups"].append({
                                    "hash": file_hash,
                                    "size": size,
                                    "files": duplicate_files
                                })
                                # Zähle Duplikate (alle außer dem ersten in jeder Gruppe)
                                result["total_duplicates"] += len(hash_files) - 1
                                # Berechne verschwendeten Speicherplatz
                                result["wasted_space"] += size * (len(hash_files) - 1)
                    else:
                        # Betrachte alle Dateien mit gleicher Größe als potenzielle Duplikate
                        duplicate_files = [{"path": str(f), "name": f.name, "size": size} for f in size_files]
                        result["duplicate_groups"].append({
                            "size": size,
                            "files": duplicate_files
                        })
                        # Zähle Duplikate (alle außer dem ersten in jeder Gruppe)
                        result["total_duplicates"] += len(size_files) - 1
                        # Berechne verschwendeten Speicherplatz
                        result["wasted_space"] += size * (len(size_files) - 1)
            
            self.logger.info(f"Duplikatsuche abgeschlossen: {result['total_duplicates']} Duplikate gefunden")
            self.logger.info(f"Verschwendeter Speicherplatz: {self._format_size(result['wasted_space'])}")
            return result
            
        except Exception as e:
            self.logger.error(f"Fehler bei der Duplikatsuche: {e}")
            return result
    
    def _group_by_hash(self, files, chunk_size=8192):
        """
        Gruppiert Dateien nach ihrem Inhaltshash.
        
        Args:
            files (list): Liste von Dateipfaden.
            chunk_size (int): Größe der zu lesenden Chunks in Bytes.
            
        Returns:
            dict: Gruppierte Dateien nach Hash.
        """
        hash_groups = {}
        
        for file_path in files:
            try:
                file_hash = self._calculate_file_hash(file_path, chunk_size)
                if file_hash in hash_groups:
                    hash_groups[file_hash].append(file_path)
                else:
                    hash_groups[file_hash] = [file_path]
            except Exception as e:
                self.logger.error(f"Fehler beim Berechnen des Hashes für {file_path}: {e}")
        
        return hash_groups
    
    def _calculate_file_hash(self, file_path, chunk_size=8192):
        """
        Berechnet den SHA-256-Hash einer Datei.
        
        Args:
            file_path (Path): Pfad zur Datei.
            chunk_size (int): Größe der zu lesenden Chunks in Bytes.
            
        Returns:
            str: Hexadezimaler Hash-Wert.
        """
        hasher = hashlib.sha256()
        
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                hasher.update(chunk)
        
        return hasher.hexdigest()
    
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
    
    def remove_duplicates(self, duplicate_groups, keep_strategy="first"):
        """
        Entfernt Duplikate basierend auf einer Strategie.
        
        Args:
            duplicate_groups (list): Liste von Duplikatgruppen.
            keep_strategy (str): Strategie zum Behalten von Dateien ("first", "newest", "oldest").
            
        Returns:
            dict: Ergebnis der Entfernungsoperation.
        """
        self.logger.info(f"Entferne Duplikate mit Strategie: {keep_strategy}")
        
        result = {
            "removed_files": 0,
            "freed_space": 0,
            "errors": []
        }
        
        for group in duplicate_groups:
            files = group.get("files", [])
            if len(files) <= 1:
                continue
            
            # Bestimme, welche Datei behalten werden soll
            files_to_keep = []
            files_to_remove = []
            
            if keep_strategy == "first":
                files_to_keep = [files[0]]
                files_to_remove = files[1:]
            elif keep_strategy == "newest" or keep_strategy == "oldest":
                # Sortiere Dateien nach Änderungszeit
                sorted_files = sorted(files, key=lambda f: Path(f["path"]).stat().st_mtime, reverse=(keep_strategy == "newest"))
                files_to_keep = [sorted_files[0]]
                files_to_remove = sorted_files[1:]
            
            # Entferne Duplikate
            for file_info in files_to_remove:
                try:
                    file_path = Path(file_info["path"])
                    file_size = file_info["size"]
                    
                    self.logger.info(f"Entferne Duplikat: {file_path}")
                    file_path.unlink()
                    
                    result["removed_files"] += 1
                    result["freed_space"] += file_size
                except Exception as e:
                    error_msg = f"Fehler beim Entfernen von {file_info['path']}: {e}"
                    self.logger.error(error_msg)
                    result["errors"].append(error_msg)
        
        self.logger.info(f"Duplikatentfernung abgeschlossen: {result['removed_files']} Dateien entfernt")
        self.logger.info(f"Freigegebener Speicherplatz: {self._format_size(result['freed_space'])}")
        return result

# Beispiel für die Verwendung
if __name__ == "__main__":
    detector = DuplicateDetector()
    
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        print(f"Suche nach Duplikaten in: {directory}")
        result = detector.find_duplicates(directory)
        print(f"Gefundene Duplikate: {result['total_duplicates']}")
        print(f"Verschwendeter Speicherplatz: {detector._format_size(result['wasted_space'])}")
        
        if result['duplicate_groups']:
            print("\nDuplikatgruppen:")
            for i, group in enumerate(result['duplicate_groups']):
                print(f"\nGruppe {i+1} (Größe: {detector._format_size(group['size'])}):")
                for file in group['files']:
                    print(f"  - {file['path']}")
    else:
        print("Bitte geben Sie ein Verzeichnis als Argument an.")
