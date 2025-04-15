import unittest
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Füge Projektverzeichnis zum Pfad hinzu
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.file_analyzer import FileAnalyzer
from src.duplicate_detector import DuplicateDetector
from src.file_manager import FileManager
from src.smart_file_manager import SmartFileManager

class TestFileAnalyzer(unittest.TestCase):
    """Test-Klasse für den FileAnalyzer."""
    
    def setUp(self):
        """Richtet die Testumgebung ein."""
        self.analyzer = FileAnalyzer()
        
        # Erstelle temporäres Verzeichnis für Testdateien
        self.test_dir = tempfile.mkdtemp()
        
        # Erstelle Testdateien
        self.text_file = os.path.join(self.test_dir, "test.txt")
        with open(self.text_file, "w") as f:
            f.write("Dies ist eine Testdatei für den FileAnalyzer.")
        
        self.image_file = os.path.join(self.test_dir, "test.jpg")
        with open(self.image_file, "wb") as f:
            # Erstelle eine minimale JPEG-Datei
            f.write(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x03\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xff\xd9')
    
    def tearDown(self):
        """Räumt die Testumgebung auf."""
        shutil.rmtree(self.test_dir)
    
    def test_get_file_info(self):
        """Testet die get_file_info-Methode."""
        # Teste Textdatei
        info = self.analyzer.get_file_info(self.text_file)
        self.assertIsNotNone(info)
        self.assertEqual(info["file_path"], self.text_file)
        self.assertEqual(info["file_type"], "text")
        self.assertEqual(info["extension"], ".txt")
        
        # Teste Bilddatei
        info = self.analyzer.get_file_info(self.image_file)
        self.assertIsNotNone(info)
        self.assertEqual(info["file_path"], self.image_file)
        self.assertEqual(info["file_type"], "image")
        self.assertEqual(info["extension"], ".jpg")
    
    def test_analyze_text_file(self):
        """Testet die Analyse von Textdateien."""
        analysis = self.analyzer.analyze_file(self.text_file)
        self.assertIsNotNone(analysis)
        self.assertEqual(analysis["file_path"], self.text_file)
        self.assertEqual(analysis["file_type"], "text")
        self.assertIn("content_preview", analysis)
        self.assertIn("word_count", analysis)
        self.assertIn("line_count", analysis)
    
    def test_analyze_image_file(self):
        """Testet die Analyse von Bilddateien."""
        analysis = self.analyzer.analyze_file(self.image_file)
        self.assertIsNotNone(analysis)
        self.assertEqual(analysis["file_path"], self.image_file)
        self.assertEqual(analysis["file_type"], "image")
        self.assertIn("dimensions", analysis)
        self.assertIn("file_size", analysis)

class TestDuplicateDetector(unittest.TestCase):
    """Test-Klasse für den DuplicateDetector."""
    
    def setUp(self):
        """Richtet die Testumgebung ein."""
        self.detector = DuplicateDetector()
        
        # Erstelle temporäres Verzeichnis für Testdateien
        self.test_dir = tempfile.mkdtemp()
        
        # Erstelle Testdateien
        self.file1 = os.path.join(self.test_dir, "file1.txt")
        with open(self.file1, "w") as f:
            f.write("Dies ist Testinhalt für die Duplikaterkennung.")
        
        self.file2 = os.path.join(self.test_dir, "file2.txt")
        with open(self.file2, "w") as f:
            f.write("Dies ist Testinhalt für die Duplikaterkennung.")
        
        self.file3 = os.path.join(self.test_dir, "file3.txt")
        with open(self.file3, "w") as f:
            f.write("Dies ist ein anderer Testinhalt.")
    
    def tearDown(self):
        """Räumt die Testumgebung auf."""
        shutil.rmtree(self.test_dir)
    
    def test_are_files_identical(self):
        """Testet die are_files_identical-Methode."""
        # Teste identische Dateien
        self.assertTrue(self.detector.are_files_identical(self.file1, self.file2))
        
        # Teste unterschiedliche Dateien
        self.assertFalse(self.detector.are_files_identical(self.file1, self.file3))
    
    def test_find_duplicates(self):
        """Testet die find_duplicates-Methode."""
        duplicates = self.detector.find_duplicates(self.test_dir)
        self.assertIsNotNone(duplicates)
        self.assertEqual(len(duplicates), 1)  # Eine Duplikatgruppe
        
        # Prüfe, ob die Duplikatgruppe die richtigen Dateien enthält
        group = duplicates[0]
        self.assertEqual(len(group["files"]), 2)
        self.assertIn(self.file1, group["files"])
        self.assertIn(self.file2, group["files"])

class TestSmartFileManager(unittest.TestCase):
    """Test-Klasse für den SmartFileManager."""
    
    def setUp(self):
        """Richtet die Testumgebung ein."""
        self.manager = SmartFileManager()
        
        # Erstelle temporäres Verzeichnis für Testdateien
        self.test_dir = tempfile.mkdtemp()
        self.target_dir = tempfile.mkdtemp()
        
        # Erstelle verschiedene Testdateien
        self.text_file = os.path.join(self.test_dir, "document.txt")
        with open(self.text_file, "w") as f:
            f.write("Dies ist ein Textdokument.")
        
        self.image_file = os.path.join(self.test_dir, "image.jpg")
        with open(self.image_file, "wb") as f:
            f.write(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00')
        
        self.code_file = os.path.join(self.test_dir, "script.py")
        with open(self.code_file, "w") as f:
            f.write("print('Hello, World!')")
    
    def tearDown(self):
        """Räumt die Testumgebung auf."""
        shutil.rmtree(self.test_dir)
        shutil.rmtree(self.target_dir)
    
    def test_analyze_directory_structure(self):
        """Testet die analyze_directory_structure-Methode."""
        analysis = self.manager.analyze_directory_structure(self.test_dir)
        self.assertIsNotNone(analysis)
        self.assertEqual(analysis["total_files"], 3)
        self.assertEqual(analysis["total_directories"], 0)
        self.assertEqual(len(analysis["file_types"]), 3)
    
    def test_generate_cleanup_suggestions(self):
        """Testet die generate_cleanup_suggestions-Methode."""
        suggestions = self.manager.generate_cleanup_suggestions(self.test_dir)
        self.assertIsNotNone(suggestions)
        self.assertIn("organization_suggestions", suggestions)
    
    def test_auto_organize_by_type(self):
        """Testet die auto_organize_directory-Methode mit Typ-Organisation."""
        result = self.manager.auto_organize_directory(
            self.test_dir, 
            self.target_dir, 
            organization_method="by_type",
            move_files=False
        )
        
        self.assertIsNotNone(result)
        self.assertTrue(result["organized_files"] > 0)
        
        # Prüfe, ob die Zielverzeichnisse erstellt wurden
        self.assertTrue(os.path.exists(os.path.join(self.target_dir, "Dokumente")))
        self.assertTrue(os.path.exists(os.path.join(self.target_dir, "Bilder")))
        self.assertTrue(os.path.exists(os.path.join(self.target_dir, "Code")))
        
        # Prüfe, ob die Dateien kopiert wurden
        self.assertTrue(os.path.exists(os.path.join(self.target_dir, "Dokumente", "document.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.target_dir, "Bilder", "image.jpg")))
        self.assertTrue(os.path.exists(os.path.join(self.target_dir, "Code", "script.py")))

if __name__ == "__main__":
    unittest.main()
