import os
import shutil
import sys
import logging
import importlib.util
import inspect
import yaml
from pathlib import Path
from typing import Dict, List, Any, Callable, Optional, Type

# Konfiguration des Logging-Systems
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("plugin_system")

class PluginInterface:
    """
    Basisklasse für alle Plugins.
    Alle Plugins müssen diese Klasse erweitern und die erforderlichen Methoden implementieren.
    """
    def __init__(self):
        self.name = self.__class__.__name__
        self.description = "Kein Beschreibung verfügbar"
        self.version = "0.1.0"
        self.author = "Unbekannt"
    
    def initialize(self, app_context: Dict[str, Any]) -> bool:
        """
        Initialisiert das Plugin mit dem Anwendungskontext.
        
        Args:
            app_context (dict): Anwendungskontext mit Referenzen zu wichtigen Objekten.
            
        Returns:
            bool: True, wenn die Initialisierung erfolgreich war, sonst False.
        """
        return True
    
    def get_info(self) -> Dict[str, str]:
        """
        Gibt Informationen über das Plugin zurück.
        
        Returns:
            dict: Plugin-Informationen.
        """
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "author": self.author
        }
    
    def execute(self, *args, **kwargs) -> Any:
        """
        Führt die Hauptfunktion des Plugins aus.
        
        Returns:
            Any: Ergebnis der Plugin-Ausführung.
        """
        raise NotImplementedError("Die execute-Methode muss implementiert werden")
    
    def cleanup(self) -> bool:
        """
        Bereinigt Ressourcen, die vom Plugin verwendet werden.
        
        Returns:
            bool: True, wenn die Bereinigung erfolgreich war, sonst False.
        """
        return True

class PluginManager:
    """
    Verwaltet die Erkennung, Registrierung und Ausführung von Plugins.
    """
    def __init__(self, plugin_dirs: List[str] = None):
        """
        Initialisiert den PluginManager.
        
        Args:
            plugin_dirs (list, optional): Liste von Verzeichnissen, in denen nach Plugins gesucht werden soll.
        """
        self.logger = logger
        self.plugins: Dict[str, PluginInterface] = {}
        self.plugin_dirs = plugin_dirs or ["plugins"]
        self.app_context: Dict[str, Any] = {}
        self.hooks: Dict[str, List[Callable]] = {}
    
    def set_app_context(self, context: Dict[str, Any]) -> None:
        """
        Setzt den Anwendungskontext, der an Plugins übergeben wird.
        
        Args:
            context (dict): Anwendungskontext mit Referenzen zu wichtigen Objekten.
        """
        self.app_context = context
    
    def discover_plugins(self) -> List[str]:
        """
        Sucht nach verfügbaren Plugins in den Plugin-Verzeichnissen.
        
        Returns:
            list: Liste der gefundenen Plugin-Namen.
        """
        discovered_plugins = []
        
        for plugin_dir in self.plugin_dirs:
            plugin_path = Path(plugin_dir)
            
            if not plugin_path.exists() or not plugin_path.is_dir():
                self.logger.warning(f"Plugin-Verzeichnis existiert nicht: {plugin_dir}")
                continue
            
            # Suche nach Python-Modulen
            for file_path in plugin_path.glob("*.py"):
                if file_path.name.startswith("__"):
                    continue
                
                plugin_name = file_path.stem
                discovered_plugins.append(plugin_name)
                self.logger.info(f"Plugin gefunden: {plugin_name}")
            
            # Suche nach YAML-Workflows
            for file_path in plugin_path.glob("*.yaml") or plugin_path.glob("*.yml"):
                workflow_name = file_path.stem
                discovered_plugins.append(f"workflow:{workflow_name}")
                self.logger.info(f"Workflow gefunden: {workflow_name}")
        
        return discovered_plugins
    
    def load_plugin(self, plugin_name: str) -> Optional[PluginInterface]:
        """
        Lädt ein Plugin anhand seines Namens.
        
        Args:
            plugin_name (str): Name des zu ladenden Plugins.
            
        Returns:
            PluginInterface: Plugin-Instanz oder None, wenn das Plugin nicht geladen werden konnte.
        """
        if plugin_name.startswith("workflow:"):
            # Lade YAML-Workflow
            workflow_name = plugin_name.split(":", 1)[1]
            return self._load_workflow(workflow_name)
        else:
            # Lade Python-Plugin
            return self._load_python_plugin(plugin_name)
    
    def _load_python_plugin(self, plugin_name: str) -> Optional[PluginInterface]:
        """
        Lädt ein Python-Plugin.
        
        Args:
            plugin_name (str): Name des zu ladenden Plugins.
            
        Returns:
            PluginInterface: Plugin-Instanz oder None, wenn das Plugin nicht geladen werden konnte.
        """
        for plugin_dir in self.plugin_dirs:
            plugin_path = Path(plugin_dir) / f"{plugin_name}.py"
            
            if not plugin_path.exists():
                continue
            
            try:
                # Lade Modul
                spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
                if spec is None or spec.loader is None:
                    self.logger.error(f"Konnte Modul-Spezifikation für {plugin_name} nicht erstellen")
                    return None
                
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Finde Plugin-Klasse
                plugin_class = None
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, PluginInterface) and 
                        obj is not PluginInterface):
                        plugin_class = obj
                        break
                
                if plugin_class is None:
                    self.logger.error(f"Keine Plugin-Klasse in {plugin_name} gefunden")
                    return None
                
                # Erstelle Plugin-Instanz
                plugin = plugin_class()
                
                # Initialisiere Plugin
                if not plugin.initialize(self.app_context):
                    self.logger.error(f"Initialisierung von {plugin_name} fehlgeschlagen")
                    return None
                
                self.logger.info(f"Plugin {plugin_name} erfolgreich geladen")
                return plugin
                
            except Exception as e:
                self.logger.error(f"Fehler beim Laden von {plugin_name}: {e}")
                return None
        
        self.logger.error(f"Plugin {plugin_name} nicht gefunden")
        return None
    
    def _load_workflow(self, workflow_name: str) -> Optional[PluginInterface]:
        """
        Lädt einen YAML-Workflow als Plugin.
        
        Args:
            workflow_name (str): Name des zu ladenden Workflows.
            
        Returns:
            PluginInterface: Workflow-Plugin-Instanz oder None, wenn der Workflow nicht geladen werden konnte.
        """
        for plugin_dir in self.plugin_dirs:
            # Suche nach YAML-Datei
            yaml_path = None
            for ext in [".yaml", ".yml"]:
                path = Path(plugin_dir) / f"{workflow_name}{ext}"
                if path.exists():
                    yaml_path = path
                    break
            
            if yaml_path is None:
                continue
            
            try:
                # Lade YAML-Datei
                with open(yaml_path, 'r', encoding='utf-8') as f:
                    workflow_data = yaml.safe_load(f)
                
                # Erstelle Workflow-Plugin
                workflow_plugin = WorkflowPlugin(workflow_name, workflow_data, yaml_path)
                
                # Initialisiere Plugin
                if not workflow_plugin.initialize(self.app_context):
                    self.logger.error(f"Initialisierung von Workflow {workflow_name} fehlgeschlagen")
                    return None
                
                self.logger.info(f"Workflow {workflow_name} erfolgreich geladen")
                return workflow_plugin
                
            except Exception as e:
                self.logger.error(f"Fehler beim Laden von Workflow {workflow_name}: {e}")
                return None
        
        self.logger.error(f"Workflow {workflow_name} nicht gefunden")
        return None
    
    def register_plugin(self, plugin_name: str) -> bool:
        """
        Registriert ein Plugin anhand seines Namens.
        
        Args:
            plugin_name (str): Name des zu registrierenden Plugins.
            
        Returns:
            bool: True, wenn das Plugin erfolgreich registriert wurde, sonst False.
        """
        if plugin_name in self.plugins:
            self.logger.warning(f"Plugin {plugin_name} ist bereits registriert")
            return True
        
        plugin = self.load_plugin(plugin_name)
        if plugin is None:
            return False
        
        self.plugins[plugin_name] = plugin
        self.logger.info(f"Plugin {plugin_name} erfolgreich registriert")
        return True
    
    def unregister_plugin(self, plugin_name: str) -> bool:
        """
        Hebt die Registrierung eines Plugins auf.
        
        Args:
            plugin_name (str): Name des zu entfernenden Plugins.
            
        Returns:
            bool: True, wenn das Plugin erfolgreich entfernt wurde, sonst False.
        """
        if plugin_name not in self.plugins:
            self.logger.warning(f"Plugin {plugin_name} ist nicht registriert")
            return False
        
        plugin = self.plugins[plugin_name]
        
        # Bereinige Plugin-Ressourcen
        if not plugin.cleanup():
            self.logger.warning(f"Bereinigung von {plugin_name} fehlgeschlagen")
        
        # Entferne Plugin
        del self.plugins[plugin_name]
        self.logger.info(f"Plugin {plugin_name} erfolgreich entfernt")
        return True
    
    def get_plugin(self, plugin_name: str) -> Optional[PluginInterface]:
        """
        Gibt ein registriertes Plugin zurück.
        
        Args:
            plugin_name (str): Name des Plugins.
            
        Returns:
            PluginInterface: Plugin-Instanz oder None, wenn das Plugin nicht registriert ist.
        """
        return self.plugins.get(plugin_name)
    
    def get_all_plugins(self) -> Dict[str, PluginInterface]:
        """
        Gibt alle registrierten Plugins zurück.
        
        Returns:
            dict: Dictionary mit Plugin-Namen als Schlüssel und Plugin-Instanzen als Werte.
        """
        return self.plugins.copy()
    
    def execute_plugin(self, plugin_name: str, *args, **kwargs) -> Any:
        """
        Führt ein Plugin aus.
        
        Args:
            plugin_name (str): Name des auszuführenden Plugins.
            *args: Positionsargumente für das Plugin.
            **kwargs: Schlüsselwortargumente für das Plugin.
            
        Returns:
            Any: Ergebnis der Plugin-Ausführung oder None, wenn das Plugin nicht ausgeführt werden konnte.
        """
        plugin = self.get_plugin(plugin_name)
        if plugin is None:
            self.logger.error(f"Plugin {plugin_name} ist nicht registriert")
            return None
        
        try:
            result = plugin.execute(*args, **kwargs)
            self.logger.info(f"Plugin {plugin_name} erfolgreich ausgeführt")
            return result
        except Exception as e:
            self.logger.error(f"Fehler bei der Ausführung von {plugin_name}: {e}")
            return None
    
    def register_hook(self, hook_name: str, callback: Callable) -> None:
        """
        Registriert einen Hook-Callback.
        
        Args:
            hook_name (str): Name des Hooks.
            callback (callable): Callback-Funktion.
        """
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        
        self.hooks[hook_name].append(callback)
        self.logger.info(f"Hook {hook_name} registriert")
    
    def unregister_hook(self, hook_name: str, callback: Callable) -> bool:
        """
        Hebt die Registrierung eines Hook-Callbacks auf.
        
        Args:
            hook_name (str): Name des Hooks.
            callback (callable): Callback-Funktion.
            
        Returns:
            bool: True, wenn der Hook erfolgreich entfernt wurde, sonst False.
        """
        if hook_name not in self.hooks:
            return False
        
        if callback in self.hooks[hook_name]:
            self.hooks[hook_name].remove(callback)
            self.logger.info(f"Hook {hook_name} entfernt")
            return True
        
        return False
    
    def trigger_hook(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """
        Löst einen Hook aus und ruft alle registrierten Callbacks auf.
        
        Args:
            hook_name (str): Name des Hooks.
            *args: Positionsargumente für die Callbacks.
            **kwargs: Schlüsselwortargumente für die Callbacks.
            
        Returns:
            list: Liste der Ergebnisse aller Callbacks.
        """
        if hook_name not in self.hooks:
            return []
        
        results = []
        for callback in self.hooks[hook_name]:
            try:
                result = callback(*args, **kwargs)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Fehler bei der Ausführung von Hook {hook_name}: {e}")
        
        return results

class WorkflowPlugin(PluginInterface):
    """
    Plugin-Implementierung für YAML-Workflows.
    """
    def __init__(self, name: str, workflow_data: Dict[str, Any], yaml_path: Path):
        """
        Initialisiert das Workflow-Plugin.
        
        Args:
            name (str): Name des Workflows.
            workflow_data (dict): Workflow-Daten aus der YAML-Datei.
            yaml_path (Path): Pfad zur YAML-Datei.
        """
        super().__init__()
        self.name = name
        self.workflow_data = workflow_data
        self.yaml_path = yaml_path
        
        # Setze Plugin-Informationen aus Workflow-Daten
        self.description = workflow_data.get("description", f"Workflow: {name}")
        self.version = workflow_data.get("version", "0.1.0")
        self.author = workflow_data.get("author", "Unbekannt")
        
        # Workflow-spezifische Attribute
        self.steps = workflow_data.get("steps", [])
        self.variables = workflow_data.get("variables", {})
    
    def initialize(self, app_context: Dict[str, Any]) -> bool:
        """
        Initialisiert das Workflow-Plugin.
        
        Args:
            app_context (dict): Anwendungskontext.
            
        Returns:
            bool: True, wenn die Initialisierung erfolgreich war, sonst False.
        """
        self.app_context = app_context
        return True
    
    def execute(self, *args, **kwargs) -> Any:
        """
        Führt den Workflow aus.
        
        Returns:
            dict: Ergebnis der Workflow-Ausführung.
        """
        result = {
            "success": True,
            "steps_executed": 0,
            "errors": [],
            "output": {}
        }
        
        # Initialisiere Workflow-Variablen
        variables = self.variables.copy()
        
        # Füge übergebene Argumente zu Variablen hinzu
        for key, value in kwargs.items():
            variables[key] = value
        
        # Führe Workflow-Schritte aus
        for i, step in enumerate(self.steps):
            step_name = step.get("name", f"Schritt {i+1}")
            step_type = step.get("type", "unknown")
            
            try:
                if step_type == "file_operation":
                    self._execute_file_operation(step, variables, result)
                elif step_type == "plugin_call":
                    self._execute_plugin_call(step, variables, result)
                elif step_type == "condition":
                    self._execute_condition(step, variables, result)
                elif step_type == "loop":
                    self._execute_loop(step, variables, result)
                else:
                    result["errors"].append(f"Unbekannter Schritttyp: {step_type} in {step_name}")
                    continue
                
                result["steps_executed"] += 1
                
            except Exception as e:
                result["errors"].append(f"Fehler bei der Ausführung von {step_name}: {e}")
                if step.get("continue_on_error", False):
                    continue
                else:
                    result["success"] = False
                    break
        
        # Setze Ausgabevariablen
        for output_var in self.workflow_data.get("output", []):
            if output_var in variables:
                result["output"][output_var] = variables[output_var]
        
        return result
    
    def _execute_file_operation(self, step: Dict[str, Any], variables: Dict[str, Any], result: Dict[str, Any]) -> None:
        """
        Führt eine Dateioperation aus.
        
        Args:
            step (dict): Schritt-Definition.
            variables (dict): Workflow-Variablen.
            result (dict): Ergebnis-Dictionary.
        """
        operation = step.get("operation", "unknown")
        
        if operation == "copy":
            source = self._resolve_variable(step.get("source", ""), variables)
            target = self._resolve_variable(step.get("target", ""), variables)
            
            if not source or not target:
                result["errors"].append(f"Ungültige Parameter für copy-Operation: source={source}, target={target}")
                return
            
            shutil.copy2(source, target)
            
        elif operation == "move":
            source = self._resolve_variable(step.get("source", ""), variables)
            target = self._resolve_variable(step.get("target", ""), variables)
            
            if not source or not target:
                result["errors"].append(f"Ungültige Parameter für move-Operation: source={source}, target={target}")
                return
            
            shutil.move(source, target)
            
        elif operation == "delete":
            path = self._resolve_variable(step.get("path", ""), variables)
            
            if not path:
                result["errors"].append(f"Ungültiger Parameter für delete-Operation: path={path}")
                return
            
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            
        elif operation == "create_dir":
            path = self._resolve_variable(step.get("path", ""), variables)
            
            if not path:
                result["errors"].append(f"Ungültiger Parameter für create_dir-Operation: path={path}")
                return
            
            os.makedirs(path, exist_ok=True)
            
        else:
            result["errors"].append(f"Unbekannte Dateioperation: {operation}")
    
    def _execute_plugin_call(self, step: Dict[str, Any], variables: Dict[str, Any], result: Dict[str, Any]) -> None:
        """
        Führt einen Plugin-Aufruf aus.
        
        Args:
            step (dict): Schritt-Definition.
            variables (dict): Workflow-Variablen.
            result (dict): Ergebnis-Dictionary.
        """
        plugin_name = step.get("plugin", "")
        method = step.get("method", "execute")
        args = step.get("args", [])
        kwargs = step.get("kwargs", {})
        output_var = step.get("output_var", "")
        
        if not plugin_name:
            result["errors"].append("Kein Plugin-Name angegeben")
            return
        
        # Löse Variablen in Argumenten auf
        resolved_args = [self._resolve_variable(arg, variables) for arg in args]
        resolved_kwargs = {k: self._resolve_variable(v, variables) for k, v in kwargs.items()}
        
        # Hole Plugin-Manager aus dem Anwendungskontext
        plugin_manager = self.app_context.get("plugin_manager")
        if plugin_manager is None:
            result["errors"].append("Plugin-Manager nicht im Anwendungskontext gefunden")
            return
        
        # Hole Plugin
        plugin = plugin_manager.get_plugin(plugin_name)
        if plugin is None:
            result["errors"].append(f"Plugin {plugin_name} nicht gefunden")
            return
        
        # Führe Plugin-Methode aus
        if method == "execute":
            plugin_result = plugin.execute(*resolved_args, **resolved_kwargs)
        else:
            if not hasattr(plugin, method):
                result["errors"].append(f"Methode {method} nicht in Plugin {plugin_name} gefunden")
                return
            
            plugin_method = getattr(plugin, method)
            plugin_result = plugin_method(*resolved_args, **resolved_kwargs)
        
        # Speichere Ergebnis in Variable
        if output_var:
            variables[output_var] = plugin_result
    
    def _execute_condition(self, step: Dict[str, Any], variables: Dict[str, Any], result: Dict[str, Any]) -> None:
        """
        Führt eine Bedingung aus.
        
        Args:
            step (dict): Schritt-Definition.
            variables (dict): Workflow-Variablen.
            result (dict): Ergebnis-Dictionary.
        """
        condition = step.get("condition", "")
        if_steps = step.get("if_steps", [])
        else_steps = step.get("else_steps", [])
        
        # Werte Bedingung aus
        condition_result = self._evaluate_condition(condition, variables)
        
        # Führe entsprechende Schritte aus
        if condition_result:
            for if_step in if_steps:
                try:
                    step_type = if_step.get("type", "unknown")
                    
                    if step_type == "file_operation":
                        self._execute_file_operation(if_step, variables, result)
                    elif step_type == "plugin_call":
                        self._execute_plugin_call(if_step, variables, result)
                    elif step_type == "condition":
                        self._execute_condition(if_step, variables, result)
                    elif step_type == "loop":
                        self._execute_loop(if_step, variables, result)
                    else:
                        result["errors"].append(f"Unbekannter Schritttyp: {step_type}")
                        continue
                    
                    result["steps_executed"] += 1
                    
                except Exception as e:
                    result["errors"].append(f"Fehler bei der Ausführung eines if-Schritts: {e}")
                    if if_step.get("continue_on_error", False):
                        continue
                    else:
                        break
        else:
            for else_step in else_steps:
                try:
                    step_type = else_step.get("type", "unknown")
                    
                    if step_type == "file_operation":
                        self._execute_file_operation(else_step, variables, result)
                    elif step_type == "plugin_call":
                        self._execute_plugin_call(else_step, variables, result)
                    elif step_type == "condition":
                        self._execute_condition(else_step, variables, result)
                    elif step_type == "loop":
                        self._execute_loop(else_step, variables, result)
                    else:
                        result["errors"].append(f"Unbekannter Schritttyp: {step_type}")
                        continue
                    
                    result["steps_executed"] += 1
                    
                except Exception as e:
                    result["errors"].append(f"Fehler bei der Ausführung eines else-Schritts: {e}")
                    if else_step.get("continue_on_error", False):
                        continue
                    else:
                        break
    
    def _execute_loop(self, step: Dict[str, Any], variables: Dict[str, Any], result: Dict[str, Any]) -> None:
        """
        Führt eine Schleife aus.
        
        Args:
            step (dict): Schritt-Definition.
            variables (dict): Workflow-Variablen.
            result (dict): Ergebnis-Dictionary.
        """
        loop_type = step.get("loop_type", "unknown")
        loop_steps = step.get("steps", [])
        
        if loop_type == "for_each":
            items = self._resolve_variable(step.get("items", []), variables)
            item_var = step.get("item_var", "item")
            
            for item in items:
                # Setze Schleifenvariable
                variables[item_var] = item
                
                # Führe Schleifenschritte aus
                for loop_step in loop_steps:
                    try:
                        step_type = loop_step.get("type", "unknown")
                        
                        if step_type == "file_operation":
                            self._execute_file_operation(loop_step, variables, result)
                        elif step_type == "plugin_call":
                            self._execute_plugin_call(loop_step, variables, result)
                        elif step_type == "condition":
                            self._execute_condition(loop_step, variables, result)
                        elif step_type == "loop":
                            self._execute_loop(loop_step, variables, result)
                        else:
                            result["errors"].append(f"Unbekannter Schritttyp: {step_type}")
                            continue
                        
                        result["steps_executed"] += 1
                        
                    except Exception as e:
                        result["errors"].append(f"Fehler bei der Ausführung eines Schleifenschritts: {e}")
                        if loop_step.get("continue_on_error", False):
                            continue
                        else:
                            break
        
        elif loop_type == "while":
            condition = step.get("condition", "")
            max_iterations = step.get("max_iterations", 100)
            
            iteration = 0
            while self._evaluate_condition(condition, variables) and iteration < max_iterations:
                # Führe Schleifenschritte aus
                for loop_step in loop_steps:
                    try:
                        step_type = loop_step.get("type", "unknown")
                        
                        if step_type == "file_operation":
                            self._execute_file_operation(loop_step, variables, result)
                        elif step_type == "plugin_call":
                            self._execute_plugin_call(loop_step, variables, result)
                        elif step_type == "condition":
                            self._execute_condition(loop_step, variables, result)
                        elif step_type == "loop":
                            self._execute_loop(loop_step, variables, result)
                        else:
                            result["errors"].append(f"Unbekannter Schritttyp: {step_type}")
                            continue
                        
                        result["steps_executed"] += 1
                        
                    except Exception as e:
                        result["errors"].append(f"Fehler bei der Ausführung eines Schleifenschritts: {e}")
                        if loop_step.get("continue_on_error", False):
                            continue
                        else:
                            break
                
                iteration += 1
        
        else:
            result["errors"].append(f"Unbekannter Schleifentyp: {loop_type}")
    
    def _resolve_variable(self, value: Any, variables: Dict[str, Any]) -> Any:
        """
        Löst Variablen in einem Wert auf.
        
        Args:
            value: Wert, der Variablen enthalten kann.
            variables (dict): Workflow-Variablen.
            
        Returns:
            Any: Aufgelöster Wert.
        """
        if isinstance(value, str) and value.startswith("$"):
            var_name = value[1:]
            return variables.get(var_name, value)
        
        return value
    
    def _evaluate_condition(self, condition: str, variables: Dict[str, Any]) -> bool:
        """
        Wertet eine Bedingung aus.
        
        Args:
            condition (str): Bedingungsausdruck.
            variables (dict): Workflow-Variablen.
            
        Returns:
            bool: Ergebnis der Bedingungsauswertung.
        """
        # Einfache Bedingungsauswertung
        if not condition:
            return True
        
        # Ersetze Variablen
        for var_name, var_value in variables.items():
            placeholder = f"${var_name}"
            if placeholder in condition:
                if isinstance(var_value, str):
                    condition = condition.replace(placeholder, f"'{var_value}'")
                else:
                    condition = condition.replace(placeholder, str(var_value))
        
        try:
            # Werte Bedingung aus
            return bool(eval(condition))
        except Exception as e:
            logger.error(f"Fehler bei der Auswertung der Bedingung '{condition}': {e}")
            return False

# Beispiel für die Verwendung
if __name__ == "__main__":
    # Erstelle Plugin-Manager
    plugin_manager = PluginManager(["plugins"])
    
    # Setze Anwendungskontext
    app_context = {
        "plugin_manager": plugin_manager,
        "app_version": "0.1.0"
    }
    plugin_manager.set_app_context(app_context)
    
    # Suche nach verfügbaren Plugins
    discovered_plugins = plugin_manager.discover_plugins()
    print(f"Gefundene Plugins: {discovered_plugins}")
    
    # Registriere Plugins
    for plugin_name in discovered_plugins:
        plugin_manager.register_plugin(plugin_name)
    
    # Zeige registrierte Plugins
    plugins = plugin_manager.get_all_plugins()
    for name, plugin in plugins.items():
        print(f"Plugin: {name}, Info: {plugin.get_info()}")
    
    # Führe Plugins aus
    for name in plugins:
        result = plugin_manager.execute_plugin(name)
        print(f"Ergebnis von {name}: {result}")
