import unittest
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Füge Projektverzeichnis zum Pfad hinzu
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.file_analyzer import FileAnalyzer

class TestFileTypes(unittest.TestCase):
    """Test-Klasse für die Unterstützung verschiedener Dateitypen."""
    
    def setUp(self):
        """Richtet die Testumgebung ein."""
        self.analyzer = FileAnalyzer()
        
        # Erstelle temporäres Verzeichnis für Testdateien
        self.test_dir = tempfile.mkdtemp()
        
        # Erstelle verschiedene Testdateien
        self.create_test_files()
    
    def tearDown(self):
        """Räumt die Testumgebung auf."""
        shutil.rmtree(self.test_dir)
    
    def create_test_files(self):
        """Erstellt verschiedene Testdateien für die Tests."""
        # Textdateien
        self.text_file = os.path.join(self.test_dir, "document.txt")
        with open(self.text_file, "w") as f:
            f.write("Dies ist ein einfaches Textdokument.")
        
        self.markdown_file = os.path.join(self.test_dir, "readme.md")
        with open(self.markdown_file, "w") as f:
            f.write("# Überschrift\n\nDies ist ein Markdown-Dokument.")
        
        # Bilddateien
        self.jpg_file = os.path.join(self.test_dir, "image.jpg")
        with open(self.jpg_file, "wb") as f:
            f.write(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00')
        
        self.png_file = os.path.join(self.test_dir, "icon.png")
        with open(self.png_file, "wb") as f:
            f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82')
        
        # Codedateien
        self.python_file = os.path.join(self.test_dir, "script.py")
        with open(self.python_file, "w") as f:
            f.write("print('Hello, World!')")
        
        self.javascript_file = os.path.join(self.test_dir, "script.js")
        with open(self.javascript_file, "w") as f:
            f.write("console.log('Hello, World!');")
        
        self.html_file = os.path.join(self.test_dir, "page.html")
        with open(self.html_file, "w") as f:
            f.write("<html><body><h1>Hello, World!</h1></body></html>")
        
        # Tabellendateien
        self.csv_file = os.path.join(self.test_dir, "data.csv")
        with open(self.csv_file, "w") as f:
            f.write("Name,Alter,Stadt\nMax,30,Berlin\nAnna,25,Hamburg")
        
        # Konfigurationsdateien
        self.json_file = os.path.join(self.test_dir, "config.json")
        with open(self.json_file, "w") as f:
            f.write('{"name": "Test", "version": "1.0.0"}')
        
        self.yaml_file = os.path.join(self.test_dir, "config.yaml")
        with open(self.yaml_file, "w") as f:
            f.write("name: Test\nversion: 1.0.0")
        
        # Archivdateien (leere Dummy-Dateien)
        self.zip_file = os.path.join(self.test_dir, "archive.zip")
        with open(self.zip_file, "wb") as f:
            f.write(b'PK\x05\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    
    def test_text_files(self):
        """Testet die Unterstützung von Textdateien."""
        # Teste TXT-Datei
        info = self.analyzer.get_file_info(self.text_file)
        self.assertEqual(info["file_type"], "text")
        self.assertEqual(info["extension"], ".txt")
        
        # Teste Markdown-Datei
        info = self.analyzer.get_file_info(self.markdown_file)
        self.assertEqual(info["file_type"], "text")
        self.assertEqual(info["extension"], ".md")
        
        # Teste Analyse von Textdateien
        analysis = self.analyzer.analyze_file(self.text_file)
        self.assertIn("content_preview", analysis)
        self.assertIn("word_count", analysis)
        self.assertIn("line_count", analysis)
    
    def test_image_files(self):
        """Testet die Unterstützung von Bilddateien."""
        # Teste JPG-Datei
        info = self.analyzer.get_file_info(self.jpg_file)
        self.assertEqual(info["file_type"], "image")
        self.assertEqual(info["extension"], ".jpg")
        
        # Teste PNG-Datei
        info = self.analyzer.get_file_info(self.png_file)
        self.assertEqual(info["file_type"], "image")
        self.assertEqual(info["extension"], ".png")
        
        # Teste Analyse von Bilddateien
        analysis = self.analyzer.analyze_file(self.jpg_file)
        self.assertIn("file_size", analysis)
    
    def test_code_files(self):
        """Testet die Unterstützung von Codedateien."""
        # Teste Python-Datei
        info = self.analyzer.get_file_info(self.python_file)
        self.assertEqual(info["file_type"], "code")
        self.assertEqual(info["extension"], ".py")
        
        # Teste JavaScript-Datei
        info = self.analyzer.get_file_info(self.javascript_file)
        self.assertEqual(info["file_type"], "code")
        self.assertEqual(info["extension"], ".js")
        
        # Teste HTML-Datei
        info = self.analyzer.get_file_info(self.html_file)
        self.assertEqual(info["file_type"], "code")
        self.assertEqual(info["extension"], ".html")
        
        # Teste Analyse von Codedateien
        analysis = self.analyzer.analyze_file(self.python_file)
        self.assertIn("content_preview", analysis)
        self.assertIn("line_count", analysis)
    
    def test_data_files(self):
        """Testet die Unterstützung von Datendateien."""
        # Teste CSV-Datei
        info = self.analyzer.get_file_info(self.csv_file)
        self.assertEqual(info["file_type"], "data")
        self.assertEqual(info["extension"], ".csv")
        
        # Teste Analyse von Datendateien
        analysis = self.analyzer.analyze_file(self.csv_file)
        self.assertIn("content_preview", analysis)
        self.assertIn("line_count", analysis)
    
    def test_config_files(self):
        """Testet die Unterstützung von Konfigurationsdateien."""
        # Teste JSON-Datei
        info = self.analyzer.get_file_info(self.json_file)
        self.assertEqual(info["file_type"], "config")
        self.assertEqual(info["extension"], ".json")
        
        # Teste YAML-Datei
        info = self.analyzer.get_file_info(self.yaml_file)
        self.assertEqual(info["file_type"], "config")
        self.assertEqual(info["extension"], ".yaml")
        
        # Teste Analyse von Konfigurationsdateien
        analysis = self.analyzer.analyze_file(self.json_file)
        self.assertIn("content_preview", analysis)
    
    def test_archive_files(self):
        """Testet die Unterstützung von Archivdateien."""
        # Teste ZIP-Datei
        info = self.analyzer.get_file_info(self.zip_file)
        self.assertEqual(info["file_type"], "archive")
        self.assertEqual(info["extension"], ".zip")
        
        # Teste Analyse von Archivdateien
        analysis = self.analyzer.analyze_file(self.zip_file)
        self.assertIn("file_size", analysis)

if __name__ == "__main__":
    unittest.main()
