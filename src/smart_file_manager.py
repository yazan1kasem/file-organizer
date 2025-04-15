import os
import sys
import logging
from pathlib import Path
import shutil
import hashlib
from collections import defaultdict
import re
from datetime import datetime

# Konfiguration des Logging-Systems
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("smart_file_manager")

class SmartFileManager:
    """
    Klasse für intelligentes Dateimanagement mit automatischer Gruppierung,
    Aufräumvorschlägen und Ähnlichkeitserkennung.
    """
    def __init__(self):
        """
        Initialisiert den SmartFileManager.
        """
        self.logger = logger
    
    def analyze_directory_structure(self, directory_path):
        """
        Analysiert die Struktur eines Verzeichnisses und gibt Statistiken zurück.
        
        Args:
            directory_path (str): Pfad zum zu analysierenden Verzeichnis.
            
        Returns:
            dict: Statistiken über die Verzeichnisstruktur.
        """
        self.logger.info(f"Analysiere Verzeichnisstruktur: {directory_path}")
        
        result = {
            "total_files": 0,
            "total_directories": 0,
            "file_types": defaultdict(int),
            "size_distribution": defaultdict(int),
            "date_distribution": defaultdict(int),
            "empty_directories": [],
            "large_directories": [],
            "old_files": [],
            "large_files": []
        }
        
        try:
            directory = Path(directory_path)
            if not directory.exists() or not directory.is_dir():
                self.logger.error(f"Verzeichnis existiert nicht oder ist kein Verzeichnis: {directory_path}")
                return result
            
            # Durchlaufe alle Dateien und Verzeichnisse
            for root, dirs, files in os.walk(directory):
                root_path = Path(root)
                
                # Zähle Verzeichnisse
                result["total_directories"] += len(dirs)
                
                # Prüfe auf leere Verzeichnisse
                if not dirs and not files:
                    result["empty_directories"].append(str(root_path))
                
                # Sammle Informationen über Dateien
                dir_size = 0
                for file in files:
                    file_path = root_path / file
                    
                    # Überspringe symbolische Links
                    if file_path.is_symlink():
                        continue
                    
                    result["total_files"] += 1
                    
                    try:
                        # Dateigröße
                        file_size = file_path.stat().st_size
                        dir_size += file_size
                        
                        # Dateityp
                        file_ext = file_path.suffix.lower()
                        result["file_types"][file_ext] += 1
                        
                        # Größenverteilung
                        if file_size < 10 * 1024:  # < 10 KB
                            result["size_distribution"]["< 10 KB"] += 1
                        elif file_size < 1024 * 1024:  # < 1 MB
                            result["size_distribution"]["< 1 MB"] += 1
                        elif file_size < 10 * 1024 * 1024:  # < 10 MB
                            result["size_distribution"]["< 10 MB"] += 1
                        elif file_size < 100 * 1024 * 1024:  # < 100 MB
                            result["size_distribution"]["< 100 MB"] += 1
                        elif file_size < 1024 * 1024 * 1024:  # < 1 GB
                            result["size_distribution"]["< 1 GB"] += 1
                        else:  # >= 1 GB
                            result["size_distribution"][">= 1 GB"] += 1
                        
                        # Große Dateien
                        if file_size > 100 * 1024 * 1024:  # > 100 MB
                            result["large_files"].append({
                                "path": str(file_path),
                                "size": file_size
                            })
                        
                        # Datumsverteilung
                        mod_time = file_path.stat().st_mtime
                        mod_date = datetime.fromtimestamp(mod_time)
                        year_month = mod_date.strftime("%Y-%m")
                        result["date_distribution"][year_month] += 1
                        
                        # Alte Dateien
                        current_time = datetime.now().timestamp()
                        if current_time - mod_time > 365 * 24 * 60 * 60:  # Älter als 1 Jahr
                            result["old_files"].append({
                                "path": str(file_path),
                                "last_modified": mod_date.strftime("%Y-%m-%d")
                            })
                    
                    except Exception as e:
                        self.logger.error(f"Fehler bei der Analyse von {file_path}: {e}")
                
                # Große Verzeichnisse
                if dir_size > 1024 * 1024 * 1024:  # > 1 GB
                    result["large_directories"].append({
                        "path": str(root_path),
                        "size": dir_size
                    })
            
            # Sortiere Ergebnisse
            result["large_files"] = sorted(result["large_files"], key=lambda x: x["size"], reverse=True)[:20]
            result["large_directories"] = sorted(result["large_directories"], key=lambda x: x["size"], reverse=True)[:20]
            result["old_files"] = sorted(result["old_files"], key=lambda x: x["last_modified"])[:100]
            
            self.logger.info(f"Verzeichnisanalyse abgeschlossen: {result['total_files']} Dateien, {result['total_directories']} Verzeichnisse")
            return result
            
        except Exception as e:
            self.logger.error(f"Fehler bei der Verzeichnisanalyse: {e}")
            return result
    
    def generate_cleanup_suggestions(self, directory_path):
        """
        Generiert Vorschläge zum Aufräumen eines Verzeichnisses.
        
        Args:
            directory_path (str): Pfad zum zu analysierenden Verzeichnis.
            
        Returns:
            dict: Aufräumvorschläge.
        """
        self.logger.info(f"Generiere Aufräumvorschläge für: {directory_path}")
        
        result = {
            "empty_directories": [],
            "duplicate_files": [],
            "temp_files": [],
            "old_files": [],
            "large_files": [],
            "organization_suggestions": []
        }
        
        try:
            # Analysiere Verzeichnisstruktur
            analysis = self.analyze_directory_structure(directory_path)
            
            # Leere Verzeichnisse
            result["empty_directories"] = analysis["empty_directories"]
            
            # Alte Dateien
            result["old_files"] = analysis["old_files"]
            
            # Große Dateien
            result["large_files"] = analysis["large_files"]
            
            # Temporäre Dateien finden
            temp_extensions = ['.tmp', '.temp', '.bak', '.cache', '.log']
            temp_patterns = [r'~\$.*', r'.*\.swp', r'.*\.swo', r'Thumbs\.db', r'\.DS_Store']
            
            directory = Path(directory_path)
            for root, _, files in os.walk(directory):
                root_path = Path(root)
                for file in files:
                    file_path = root_path / file
                    
                    # Überspringe symbolische Links
                    if file_path.is_symlink():
                        continue
                    
                    # Prüfe auf temporäre Dateierweiterungen
                    if any(file.lower().endswith(ext) for ext in temp_extensions):
                        result["temp_files"].append(str(file_path))
                    
                    # Prüfe auf temporäre Dateimuster
                    if any(re.match(pattern, file) for pattern in temp_patterns):
                        result["temp_files"].append(str(file_path))
            
            # Organisationsvorschläge basierend auf Dateitypen
            file_types = analysis["file_types"]
            if len(file_types) > 5:
                result["organization_suggestions"].append({
                    "type": "by_file_type",
                    "description": "Organisiere Dateien nach Dateityp",
                    "reason": f"Es wurden {len(file_types)} verschiedene Dateitypen gefunden."
                })
            
            # Organisationsvorschläge basierend auf Datumsverteilung
            date_distribution = analysis["date_distribution"]
            if len(date_distribution) > 12:
                result["organization_suggestions"].append({
                    "type": "by_date",
                    "description": "Organisiere Dateien nach Datum",
                    "reason": f"Die Dateien stammen aus {len(date_distribution)} verschiedenen Monaten."
                })
            
            # Organisationsvorschläge basierend auf Größenverteilung
            size_distribution = analysis["size_distribution"]
            if size_distribution.get(">= 1 GB", 0) > 0 or size_distribution.get("< 1 GB", 0) > 10:
                result["organization_suggestions"].append({
                    "type": "by_size",
                    "description": "Organisiere Dateien nach Größe",
                    "reason": "Es wurden mehrere große Dateien gefunden."
                })
            
            self.logger.info(f"Aufräumvorschläge generiert: {len(result['empty_directories'])} leere Verzeichnisse, {len(result['temp_files'])} temporäre Dateien")
            return result
            
        except Exception as e:
            self.logger.error(f"Fehler bei der Generierung von Aufräumvorschlägen: {e}")
            return result
    
    def group_files_by_similarity(self, directory_path, similarity_threshold=0.7, max_files=1000):
        """
        Gruppiert Dateien nach Ähnlichkeit.
        
        Args:
            directory_path (str): Pfad zum zu analysierenden Verzeichnis.
            similarity_threshold (float): Schwellenwert für die Ähnlichkeit (0.0 bis 1.0).
            max_files (int): Maximale Anzahl zu analysierender Dateien.
            
        Returns:
            dict: Gruppierte Dateien nach Ähnlichkeit.
        """
        self.logger.info(f"Gruppiere Dateien nach Ähnlichkeit in: {directory_path}")
        
        result = {
            "similar_text_files": [],
            "similar_image_files": [],
            "similar_names": []
        }
        
        try:
            directory = Path(directory_path)
            if not directory.exists() or not directory.is_dir():
                self.logger.error(f"Verzeichnis existiert nicht oder ist kein Verzeichnis: {directory_path}")
                return result
            
            # Sammle Dateien
            text_files = []
            image_files = []
            all_files = []
            
            text_extensions = ['.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml', '.csv']
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']
            
            for root, _, files in os.walk(directory):
                root_path = Path(root)
                for file in files:
                    file_path = root_path / file
                    
                    # Überspringe symbolische Links
                    if file_path.is_symlink():
                        continue
                    
                    all_files.append(file_path)
                    
                    # Kategorisiere Dateien
                    ext = file_path.suffix.lower()
                    if ext in text_extensions:
                        text_files.append(file_path)
                    elif ext in image_extensions:
                        image_files.append(file_path)
                    
                    # Begrenze die Anzahl der Dateien
                    if len(all_files) >= max_files:
                        break
                
                if len(all_files) >= max_files:
                    break
            
            # Gruppiere Textdateien nach Inhalt
            if text_files:
                text_groups = self._group_text_files_by_content(text_files, similarity_threshold)
                result["similar_text_files"] = text_groups
            
            # Gruppiere Bilddateien nach Inhalt
            # In einer vollständigen Implementierung würde hier eine Bildähnlichkeitsanalyse durchgeführt werden
            # Für dieses Beispiel gruppieren wir nach Dateigröße als einfache Annäherung
            if image_files:
                image_groups = self._group_files_by_size(image_files)
                result["similar_image_files"] = image_groups
            
            # Gruppiere Dateien nach Namensähnlichkeit
            name_groups = self._group_files_by_name_similarity(all_files, similarity_threshold)
            result["similar_names"] = name_groups
            
            self.logger.info(f"Ähnlichkeitsgruppierung abgeschlossen: {len(result['similar_text_files'])} Textgruppen, {len(result['similar_image_files'])} Bildgruppen, {len(result['similar_names'])} Namensgruppen")
            return result
            
        except Exception as e:
            self.logger.error(f"Fehler bei der Ähnlichkeitsgruppierung: {e}")
            return result
    
    def _group_text_files_by_content(self, files, similarity_threshold):
        """
        Gruppiert Textdateien nach Inhaltsähnlichkeit.
        
        Args:
            files (list): Liste von Dateipfaden.
            similarity_threshold (float): Schwellenwert für die Ähnlichkeit.
            
        Returns:
            list: Gruppen ähnlicher Dateien.
        """
        groups = []
        
        try:
            # Extrahiere Inhalt und berechne Hashes
            file_contents = {}
            for file_path in files:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # Berechne Shingles (n-Gramme) für den Inhalt
                    shingles = self._compute_shingles(content)
                    
                    file_contents[str(file_path)] = {
                        "path": str(file_path),
                        "shingles": shingles
                    }
                except Exception as e:
                    self.logger.error(f"Fehler beim Lesen von {file_path}: {e}")
            
            # Gruppiere Dateien basierend auf Jaccard-Ähnlichkeit
            processed = set()
            
            for file_path, file_data in file_contents.items():
                if file_path in processed:
                    continue
                
                similar_files = []
                
                for other_path, other_data in file_contents.items():
                    if other_path == file_path or other_path in processed:
                        continue
                    
                    similarity = self._jaccard_similarity(file_data["shingles"], other_data["shingles"])
                    
                    if similarity >= similarity_threshold:
                        similar_files.append({
                            "path": other_data["path"],
                            "similarity": similarity
                        })
                        processed.add(other_path)
                
                if similar_files:
                    groups.append({
                        "base_file": file_data["path"],
                        "similar_files": similar_files
                    })
                    processed.add(file_path)
            
            return groups
            
        except Exception as e:
            self.logger.error(f"Fehler bei der Textdateigruppierung: {e}")
            return groups
    
    def _compute_shingles(self, text, k=5):
        """
        Berechnet k-Shingles (k-Gramme) für einen Text.
        
        Args:
            text (str): Eingabetext.
            k (int): Größe der Shingles.
            
        Returns:
            set: Menge von Shingles.
        """
        # Normalisiere Text
        text = re.sub(r'\s+', ' ', text.lower())
        
        # Berechne Shingles
        shingles = set()
        for i in range(len(text) - k + 1):
            shingles.add(text[i:i+k])
        
        return shingles
    
    def _jaccard_similarity(self, set1, set2):
        """
        Berechnet die Jaccard-Ähnlichkeit zwischen zwei Mengen.
        
        Args:
            set1 (set): Erste Menge.
            set2 (set): Zweite Menge.
            
        Returns:
            float: Jaccard-Ähnlichkeit (0.0 bis 1.0).
        """
        if not set1 or not set2:
            return 0.0
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union
    
    def _group_files_by_size(self, files):
        """
        Gruppiert Dateien nach Größe.
        
        Args:
            files (list): Liste von Dateipfaden.
            
        Returns:
            list: Gruppen von Dateien mit ähnlicher Größe.
        """
        groups = []
        
        try:
            # Gruppiere Dateien nach Größe
            size_groups = defaultdict(list)
            
            for file_path in files:
                try:
                    size = file_path.stat().st_size
                    size_groups[size].append(str(file_path))
                except Exception as e:
                    self.logger.error(f"Fehler beim Lesen der Größe von {file_path}: {e}")
            
            # Erstelle Gruppen mit mehr als einer Datei
            for size, paths in size_groups.items():
                if len(paths) > 1:
                    groups.append({
                        "size": size,
                        "files": paths
                    })
            
            # Sortiere Gruppen nach Größe
            groups = sorted(groups, key=lambda x: x["size"], reverse=True)
            
            return groups
            
        except Exception as e:
            self.logger.error(f"Fehler bei der Dateigruppierung nach Größe: {e}")
            return groups
    
    def _group_files_by_name_similarity(self, files, similarity_threshold):
        """
        Gruppiert Dateien nach Namensähnlichkeit.
        
        Args:
            files (list): Liste von Dateipfaden.
            similarity_threshold (float): Schwellenwert für die Ähnlichkeit.
            
        Returns:
            list: Gruppen von Dateien mit ähnlichen Namen.
        """
        groups = []
        
        try:
            # Extrahiere Dateinamen
            file_names = {}
            for file_path in files:
                name = file_path.stem.lower()
                file_names[str(file_path)] = {
                    "path": str(file_path),
                    "name": name
                }
            
            # Gruppiere Dateien basierend auf Levenshtein-Distanz
            processed = set()
            
            for file_path, file_data in file_names.items():
                if file_path in processed:
                    continue
                
                similar_files = []
                
                for other_path, other_data in file_names.items():
                    if other_path == file_path or other_path in processed:
                        continue
                    
                    similarity = self._name_similarity(file_data["name"], other_data["name"])
                    
                    if similarity >= similarity_threshold:
                        similar_files.append({
                            "path": other_data["path"],
                            "similarity": similarity
                        })
                        processed.add(other_path)
                
                if similar_files:
                    groups.append({
                        "base_file": file_data["path"],
                        "base_name": file_data["name"],
                        "similar_files": similar_files
                    })
                    processed.add(file_path)
            
            return groups
            
        except Exception as e:
            self.logger.error(f"Fehler bei der Dateigruppierung nach Namensähnlichkeit: {e}")
            return groups
    
    def _name_similarity(self, name1, name2):
        """
        Berechnet die Ähnlichkeit zwischen zwei Dateinamen.
        
        Args:
            name1 (str): Erster Name.
            name2 (str): Zweiter Name.
            
        Returns:
            float: Ähnlichkeitswert (0.0 bis 1.0).
        """
        # Einfache Implementierung basierend auf gemeinsamen Zeichen
        if not name1 or not name2:
            return 0.0
        
        # Berechne Levenshtein-Distanz
        distance = self._levenshtein_distance(name1, name2)
        max_len = max(len(name1), len(name2))
        
        if max_len == 0:
            return 1.0
        
        # Normalisiere Distanz zu Ähnlichkeit
        similarity = 1.0 - (distance / max_len)
        
        return similarity
    
    def _levenshtein_distance(self, s1, s2):
        """
        Berechnet die Levenshtein-Distanz zwischen zwei Strings.
        
        Args:
            s1 (str): Erster String.
            s2 (str): Zweiter String.
            
        Returns:
            int: Levenshtein-Distanz.
        """
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def auto_organize_directory(self, directory_path, target_directory=None, organization_method="by_type", move_files=False):
        """
        Organisiert ein Verzeichnis automatisch basierend auf einer Methode.
        
        Args:
            directory_path (str): Pfad zum zu organisierenden Verzeichnis.
            target_directory (str, optional): Zielverzeichnis für die organisierten Dateien.
            organization_method (str): Organisationsmethode ("by_type", "by_date", "by_size", "by_content").
            move_files (bool): Ob Dateien verschoben oder kopiert werden sollen.
            
        Returns:
            dict: Ergebnis der Organisationsoperation.
        """
        self.logger.info(f"Organisiere Verzeichnis automatisch: {directory_path}")
        
        result = {
            "organized_files": 0,
            "skipped_files": 0,
            "errors": []
        }
        
        try:
            directory = Path(directory_path)
            if not directory.exists() or not directory.is_dir():
                self.logger.error(f"Verzeichnis existiert nicht oder ist kein Verzeichnis: {directory_path}")
                result["errors"].append(f"Verzeichnis ungültig: {directory_path}")
                return result
            
            if target_directory is None:
                target_directory = directory_path
            
            target = Path(target_directory)
            if not target.exists():
                target.mkdir(parents=True)
            
            # Organisiere basierend auf der Methode
            if organization_method == "by_type":
                return self._organize_by_type(directory, target, move_files)
            elif organization_method == "by_date":
                return self._organize_by_date(directory, target, move_files)
            elif organization_method == "by_size":
                return self._organize_by_size(directory, target, move_files)
            elif organization_method == "by_content":
                return self._organize_by_content(directory, target, move_files)
            else:
                self.logger.error(f"Unbekannte Organisationsmethode: {organization_method}")
                result["errors"].append(f"Unbekannte Organisationsmethode: {organization_method}")
                return result
            
        except Exception as e:
            self.logger.error(f"Fehler bei der automatischen Organisation: {e}")
            result["errors"].append(str(e))
            return result
    
    def _organize_by_type(self, source_dir, target_dir, move_files):
        """
        Organisiert Dateien nach Typ.
        
        Args:
            source_dir (Path): Quellverzeichnis.
            target_dir (Path): Zielverzeichnis.
            move_files (bool): Ob Dateien verschoben oder kopiert werden sollen.
            
        Returns:
            dict: Ergebnis der Organisationsoperation.
        """
        result = {
            "organized_files": 0,
            "skipped_files": 0,
            "errors": []
        }
        
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
        for file_path in source_dir.glob("*"):
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
            type_dir = target_dir / file_type
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
        
        self.logger.info(f"Organisation nach Typ abgeschlossen: {result['organized_files']} Dateien organisiert")
        return result
    
    def _organize_by_date(self, source_dir, target_dir, move_files):
        """
        Organisiert Dateien nach Datum.
        
        Args:
            source_dir (Path): Quellverzeichnis.
            target_dir (Path): Zielverzeichnis.
            move_files (bool): Ob Dateien verschoben oder kopiert werden sollen.
            
        Returns:
            dict: Ergebnis der Organisationsoperation.
        """
        result = {
            "organized_files": 0,
            "skipped_files": 0,
            "errors": []
        }
        
        # Sammle alle Dateien
        for file_path in source_dir.glob("*"):
            if not file_path.is_file():
                continue
            
            try:
                # Hole Änderungsdatum
                mod_time = file_path.stat().st_mtime
                mod_date = datetime.fromtimestamp(mod_time)
                
                # Erstelle Zielverzeichnis basierend auf Jahr und Monat
                date_dir = target_dir / f"{mod_date.year}" / f"{mod_date.month:02d}"
                if not date_dir.exists():
                    date_dir.mkdir(parents=True)
                
                # Zieldatei
                target_file = date_dir / file_path.name
                
                # Überspringe, wenn Datei bereits im richtigen Verzeichnis ist
                if str(file_path.parent) == str(date_dir):
                    result["skipped_files"] += 1
                    continue
                
                # Überspringe, wenn Zieldatei bereits existiert
                if target_file.exists():
                    result["skipped_files"] += 1
                    self.logger.warning(f"Zieldatei existiert bereits: {target_file}")
                    continue
                
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
        
        self.logger.info(f"Organisation nach Datum abgeschlossen: {result['organized_files']} Dateien organisiert")
        return result
    
    def _organize_by_size(self, source_dir, target_dir, move_files):
        """
        Organisiert Dateien nach Größe.
        
        Args:
            source_dir (Path): Quellverzeichnis.
            target_dir (Path): Zielverzeichnis.
            move_files (bool): Ob Dateien verschoben oder kopiert werden sollen.
            
        Returns:
            dict: Ergebnis der Organisationsoperation.
        """
        result = {
            "organized_files": 0,
            "skipped_files": 0,
            "errors": []
        }
        
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
        for file_path in source_dir.glob("*"):
            if not file_path.is_file():
                continue
            
            try:
                # Hole Dateigröße
                file_size = file_path.stat().st_size
                
                # Bestimme Größenkategorie
                size_category = "Sonstige"
                for category, max_size in size_categories.items():
                    if file_size < max_size:
                        size_category = category
                        break
                
                # Erstelle Zielverzeichnis
                size_dir = target_dir / size_category
                if not size_dir.exists():
                    size_dir.mkdir(parents=True)
                
                # Zieldatei
                target_file = size_dir / file_path.name
                
                # Überspringe, wenn Datei bereits im richtigen Verzeichnis ist
                if str(file_path.parent) == str(size_dir):
                    result["skipped_files"] += 1
                    continue
                
                # Überspringe, wenn Zieldatei bereits existiert
                if target_file.exists():
                    result["skipped_files"] += 1
                    self.logger.warning(f"Zieldatei existiert bereits: {target_file}")
                    continue
                
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
        
        self.logger.info(f"Organisation nach Größe abgeschlossen: {result['organized_files']} Dateien organisiert")
        return result
    
    def _organize_by_content(self, source_dir, target_dir, move_files):
        """
        Organisiert Dateien nach Inhalt.
        
        Args:
            source_dir (Path): Quellverzeichnis.
            target_dir (Path): Zielverzeichnis.
            move_files (bool): Ob Dateien verschoben oder kopiert werden sollen.
            
        Returns:
            dict: Ergebnis der Organisationsoperation.
        """
        result = {
            "organized_files": 0,
            "skipped_files": 0,
            "errors": []
        }
        
        # In einer vollständigen Implementierung würde hier eine Inhaltsanalyse durchgeführt werden
        # Für dieses Beispiel organisieren wir nach Dateityp und fügen eine einfache Ähnlichkeitsanalyse hinzu
        
        # Gruppiere Dateien nach Ähnlichkeit
        similarity_groups = self.group_files_by_similarity(str(source_dir))
        
        # Erstelle Verzeichnisse für Ähnlichkeitsgruppen
        if similarity_groups["similar_text_files"]:
            text_group_dir = target_dir / "Ähnliche Textdateien"
            if not text_group_dir.exists():
                text_group_dir.mkdir(parents=True)
            
            # Organisiere ähnliche Textdateien
            for i, group in enumerate(similarity_groups["similar_text_files"]):
                group_dir = text_group_dir / f"Gruppe_{i+1}"
                if not group_dir.exists():
                    group_dir.mkdir(parents=True)
                
                # Verschiebe oder kopiere Basisdatei
                base_file = Path(group["base_file"])
                target_file = group_dir / base_file.name
                
                try:
                    if move_files:
                        shutil.move(str(base_file), str(target_file))
                    else:
                        shutil.copy2(str(base_file), str(target_file))
                    
                    result["organized_files"] += 1
                except Exception as e:
                    error_msg = f"Fehler beim {'Verschieben' if move_files else 'Kopieren'} von {base_file}: {e}"
                    self.logger.error(error_msg)
                    result["errors"].append(error_msg)
                
                # Verschiebe oder kopiere ähnliche Dateien
                for similar in group["similar_files"]:
                    similar_file = Path(similar["path"])
                    target_file = group_dir / similar_file.name
                    
                    try:
                        if move_files:
                            shutil.move(str(similar_file), str(target_file))
                        else:
                            shutil.copy2(str(similar_file), str(target_file))
                        
                        result["organized_files"] += 1
                    except Exception as e:
                        error_msg = f"Fehler beim {'Verschieben' if move_files else 'Kopieren'} von {similar_file}: {e}"
                        self.logger.error(error_msg)
                        result["errors"].append(error_msg)
        
        # Organisiere restliche Dateien nach Typ
        remaining_files = [f for f in source_dir.glob("*") if f.is_file()]
        if remaining_files:
            # Verwende die Methode zur Organisation nach Typ für die restlichen Dateien
            type_result = self._organize_by_type(source_dir, target_dir, move_files)
            
            # Aktualisiere Ergebnis
            result["organized_files"] += type_result["organized_files"]
            result["skipped_files"] += type_result["skipped_files"]
            result["errors"].extend(type_result["errors"])
        
        self.logger.info(f"Organisation nach Inhalt abgeschlossen: {result['organized_files']} Dateien organisiert")
        return result

# Beispiel für die Verwendung
if __name__ == "__main__":
    manager = SmartFileManager()
    
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        print(f"Analysiere Verzeichnis: {directory}")
        
        # Generiere Aufräumvorschläge
        suggestions = manager.generate_cleanup_suggestions(directory)
        
        print("\nAufräumvorschläge:")
        print(f"Leere Verzeichnisse: {len(suggestions['empty_directories'])}")
        print(f"Temporäre Dateien: {len(suggestions['temp_files'])}")
        print(f"Alte Dateien: {len(suggestions['old_files'])}")
        print(f"Große Dateien: {len(suggestions['large_files'])}")
        
        print("\nOrganisationsvorschläge:")
        for suggestion in suggestions["organization_suggestions"]:
            print(f"- {suggestion['description']}: {suggestion['reason']}")
    else:
        print("Bitte geben Sie ein Verzeichnis als Argument an.")
