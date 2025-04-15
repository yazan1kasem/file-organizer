import unittest
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Füge Projektverzeichnis zum Pfad hinzu
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ui.main_window import FileOrganizerUI
from PyQt6.QtWidgets import QApplication

class TestIntegration(unittest.TestCase):
    """Test-Klasse für Integrationstests."""
    
    @classmethod
    def setUpClass(cls):
        """Richtet die Testumgebung für alle Tests ein."""
        # Initialisiere QApplication für UI-Tests
        cls.app = QApplication([])
    
    def setUp(self):
        """Richtet die Testumgebung für jeden Test ein."""
        # Erstelle temporäres Verzeichnis für Testdateien
        self.test_dir = tempfile.mkdtemp()
        
        # Erstelle verschiedene Testdateien
        self.create_test_files()
    
    def tearDown(self):
        """Räumt die Testumgebung nach jedem Test auf."""
        shutil.rmtree(self.test_dir)
    
    def create_test_files(self):
        """Erstellt verschiedene Testdateien für die Tests."""
        # Textdateien
        self.text_file = os.path.join(self.test_dir, "document.txt")
        with open(self.text_file, "w") as f:
            f.write("Dies ist ein einfaches Textdokument.")
        
        # Bilddateien
        self.jpg_file = os.path.join(self.test_dir, "image.jpg")
        with open(self.jpg_file, "wb") as f:
            f.write(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00')
        
        # Codedateien
        self.python_file = os.path.join(self.test_dir, "script.py")
        with open(self.python_file, "w") as f:
            f.write("print('Hello, World!')")
        
        # Duplikate
        self.text_file_dup = os.path.join(self.test_dir, "document_copy.txt")
        with open(self.text_file_dup, "w") as f:
            f.write("Dies ist ein einfaches Textdokument.")
    
    def test_end_to_end_workflow(self):
        """Testet den gesamten Workflow der Anwendung."""
        # Dieser Test simuliert einen typischen Workflow:
        # 1. Verzeichnis analysieren
        # 2. Duplikate finden
        # 3. Dateien organisieren
        
        from src.file_analyzer import FileAnalyzer
        from src.duplicate_detector import DuplicateDetector
        from src.smart_file_manager import SmartFileManager
        
        # 1. Verzeichnis analysieren
        analyzer = FileAnalyzer()
        
        # Analysiere jede Datei im Testverzeichnis
        file_analyses = {}
        for file_name in os.listdir(self.test_dir):
            file_path = os.path.join(self.test_dir, file_name)
            if os.path.isfile(file_path):
                analysis = analyzer.analyze_file(file_path)
                file_analyses[file_path] = analysis
        
        # Prüfe, ob alle Dateien analysiert wurden
        self.assertEqual(len(file_analyses), 4)
        
        # 2. Duplikate finden
        detector = DuplicateDetector()
        duplicates = detector.find_duplicates(self.test_dir)
        
        # Prüfe, ob Duplikate gefunden wurden
        self.assertEqual(len(duplicates), 1)
        self.assertEqual(len(duplicates[0]["files"]), 2)
        
        # 3. Dateien organisieren
        manager = SmartFileManager()
        target_dir = os.path.join(self.test_dir, "organized")
        
        # Organisiere nach Dateityp
        result = manager.auto_organize_directory(
            self.test_dir, 
            target_dir, 
            organization_method="by_type",
            move_files=False
        )
        
        # Prüfe, ob die Organisation erfolgreich war
        self.assertTrue(result["organized_files"] > 0)
        
        # Prüfe, ob die Zielverzeichnisse erstellt wurden
        self.assertTrue(os.path.exists(os.path.join(target_dir, "Dokumente")))
        self.assertTrue(os.path.exists(os.path.join(target_dir, "Bilder")))
        self.assertTrue(os.path.exists(os.path.join(target_dir, "Code")))
        
        # Prüfe, ob die Dateien kopiert wurden
        self.assertTrue(os.path.exists(os.path.join(target_dir, "Dokumente", "document.txt")))
        self.assertTrue(os.path.exists(os.path.join(target_dir, "Dokumente", "document_copy.txt")))
        self.assertTrue(os.path.exists(os.path.join(target_dir, "Bilder", "image.jpg")))
        self.assertTrue(os.path.exists(os.path.join(target_dir, "Code", "script.py")))
    
    def test_plugin_integration(self):
        """Testet die Integration des Plugin-Systems."""
        from src.plugin_system import PluginManager, PluginInterface
        
        # Erstelle ein Test-Plugin
        class TestPlugin(PluginInterface):
            def __init__(self):
                super().__init__()
                self.name = "TestPlugin"
                self.description = "Ein Test-Plugin"
                self.version = "0.1.0"
                self.author = "Test"
            
            def initialize(self, app_context):
                self.app_context = app_context
                return True
            
            def execute(self, directory, *args, **kwargs):
                # Zähle Dateien im Verzeichnis
                file_count = 0
                for _, _, files in os.walk(directory):
                    file_count += len(files)
                return {"file_count": file_count}
            
            def cleanup(self):
                return True
        
        # Erstelle Plugin-Manager
        plugin_manager = PluginManager()
        
        # Registriere Plugin manuell
        plugin = TestPlugin()
        plugin_manager.plugins["test_plugin"] = plugin
        
        # Führe Plugin aus
        result = plugin_manager.execute_plugin("test_plugin", self.test_dir)
        
        # Prüfe Ergebnis
        self.assertIsNotNone(result)
        self.assertEqual(result["file_count"], 4)

if __name__ == "__main__":
    unittest.main()
