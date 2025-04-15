import unittest
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Füge Projektverzeichnis zum Pfad hinzu
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.plugin_system import PluginManager, PluginInterface, WorkflowPlugin

class TestPluginSystem(unittest.TestCase):
    """Test-Klasse für das Plugin-System."""
    
    def setUp(self):
        """Richtet die Testumgebung ein."""
        # Erstelle temporäres Verzeichnis für Test-Plugins
        self.test_dir = tempfile.mkdtemp()
        self.plugin_dir = os.path.join(self.test_dir, "plugins")
        os.makedirs(self.plugin_dir)
        
        # Erstelle ein Test-Plugin
        self.plugin_file = os.path.join(self.plugin_dir, "test_plugin.py")
        with open(self.plugin_file, "w") as f:
            f.write("""
from src.plugin_system import PluginInterface

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
    
    def execute(self, *args, **kwargs):
        return {"status": "success", "args": args, "kwargs": kwargs}
    
    def cleanup(self):
        return True
""")
        
        # Erstelle einen Test-Workflow
        self.workflow_file = os.path.join(self.plugin_dir, "test_workflow.yaml")
        with open(self.workflow_file, "w") as f:
            f.write("""
name: Test-Workflow
description: Ein Test-Workflow
version: 0.1.0
author: Test

variables:
  test_var: "Testwert"

steps:
  - name: Test-Schritt
    type: plugin_call
    plugin: test_plugin
    method: execute
    args: ["Test"]
    kwargs:
      param: "Wert"

output:
  - test_var
""")
        
        # Erstelle Plugin-Manager
        self.plugin_manager = PluginManager([self.plugin_dir])
        self.plugin_manager.set_app_context({"test": "context"})
    
    def tearDown(self):
        """Räumt die Testumgebung auf."""
        shutil.rmtree(self.test_dir)
    
    def test_discover_plugins(self):
        """Testet die discover_plugins-Methode."""
        plugins = self.plugin_manager.discover_plugins()
        self.assertIsNotNone(plugins)
        self.assertEqual(len(plugins), 2)
        self.assertIn("test_plugin", plugins)
        self.assertIn("workflow:test_workflow", plugins)
    
    def test_load_python_plugin(self):
        """Testet das Laden eines Python-Plugins."""
        plugin = self.plugin_manager._load_python_plugin("test_plugin")
        self.assertIsNotNone(plugin)
        self.assertEqual(plugin.name, "TestPlugin")
        self.assertEqual(plugin.description, "Ein Test-Plugin")
    
    def test_load_workflow(self):
        """Testet das Laden eines YAML-Workflows."""
        plugin = self.plugin_manager._load_workflow("test_workflow")
        self.assertIsNotNone(plugin)
        self.assertEqual(plugin.name, "test_workflow")
        self.assertEqual(plugin.description, "Ein Test-Workflow")
    
    def test_register_plugin(self):
        """Testet die register_plugin-Methode."""
        result = self.plugin_manager.register_plugin("test_plugin")
        self.assertTrue(result)
        
        plugins = self.plugin_manager.get_all_plugins()
        self.assertEqual(len(plugins), 1)
        self.assertIn("test_plugin", plugins)
    
    def test_execute_plugin(self):
        """Testet die execute_plugin-Methode."""
        self.plugin_manager.register_plugin("test_plugin")
        
        result = self.plugin_manager.execute_plugin("test_plugin", "arg1", param="value")
        self.assertIsNotNone(result)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["args"], ("arg1",))
        self.assertEqual(result["kwargs"], {"param": "value"})
    
    def test_hooks(self):
        """Testet das Hook-System."""
        # Definiere einen Test-Hook
        hook_called = False
        hook_args = None
        hook_kwargs = None
        
        def test_hook(*args, **kwargs):
            nonlocal hook_called, hook_args, hook_kwargs
            hook_called = True
            hook_args = args
            hook_kwargs = kwargs
            return "hook_result"
        
        # Registriere Hook
        self.plugin_manager.register_hook("test_hook", test_hook)
        
        # Löse Hook aus
        results = self.plugin_manager.trigger_hook("test_hook", "arg1", param="value")
        
        # Prüfe Ergebnisse
        self.assertTrue(hook_called)
        self.assertEqual(hook_args, ("arg1",))
        self.assertEqual(hook_kwargs, {"param": "value"})
        self.assertEqual(results, ["hook_result"])
        
        # Entferne Hook
        result = self.plugin_manager.unregister_hook("test_hook", test_hook)
        self.assertTrue(result)
        
        # Löse Hook erneut aus
        hook_called = False
        results = self.plugin_manager.trigger_hook("test_hook", "arg1", param="value")
        self.assertFalse(hook_called)
        self.assertEqual(results, [])

if __name__ == "__main__":
    unittest.main()
