import inspect
import ast
from typing import List, Dict, Any
import unittest

class TestGenerator:
    def __init__(self):
        self.test_cases = []
        
    def analyze_class(self, class_obj) -> Dict[str, Any]:
        """Analyze a class and its methods to generate test cases"""
        class_info = {
            'name': class_obj.__name__,
            'methods': {},
            'attributes': []
        }
        
        # Get all methods and their signatures
        for name, method in inspect.getmembers(class_obj, predicate=inspect.isfunction):
            if not name.startswith('_'):  # Skip private methods
                sig = inspect.signature(method)
                class_info['methods'][name] = {
                    'parameters': list(sig.parameters.keys()),
                    'return_annotation': sig.return_annotation,
                    'docstring': method.__doc__
                }
                
        # Get class attributes from __init__
        if hasattr(class_obj, '__init__'):
            init_src = inspect.getsource(class_obj.__init__)
            tree = ast.parse(init_src)
            for node in ast.walk(tree):
                if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
                    if node.value.id == 'self':
                        class_info['attributes'].append(node.attr)
                        
        return class_info
    
    def generate_test_class(self, class_info: Dict[str, Any]) -> str:
        """Generate a test class based on the analyzed class info"""
        test_code = f"""import unittest
from {class_info['name'].lower()} import {class_info['name']}

class Test{class_info['name']}(unittest.TestCase):
    def setUp(self):
        self.obj = {class_info['name']}()
        
"""
        # Generate test methods
        for method_name, method_info in class_info['methods'].items():
            test_code += self._generate_test_method(method_name, method_info)
            
        return test_code
    
    def _generate_test_method(self, method_name: str, method_info: Dict[str, Any]) -> str:
        """Generate a test method for a specific class method"""
        test_template = f"""    def test_{method_name}(self):
        \"\"\"Test {method_name} functionality\"\"\"
        # TODO: Add specific test cases
        # Parameters: {', '.join(method_info['parameters'])}
        # Expected behavior based on docstring:
        # {method_info['docstring']}
        
"""
        return test_template

class CodeAnalyzer:
    @staticmethod
    def check_code_quality(source_code: str) -> List[str]:
        """Analyze code for potential issues and best practices"""
        issues = []
        tree = ast.parse(source_code)
        
        # Check for error handling
        for node in ast.walk(tree):
            if isinstance(node, ast.Try):
                if not any(isinstance(handler.type, ast.Name) and handler.type.id == 'Exception' 
                          for handler in node.handlers):
                    issues.append("Consider adding general exception handling")
                    
            # Check for potential infinite loops
            if isinstance(node, ast.While):
                if not any(isinstance(child, ast.Break) for child in ast.walk(node)):
                    issues.append("Potential infinite loop detected")
                    
        return issues

class TestRunner:
    @staticmethod
    def run_tests(test_case_class) -> unittest.TestResult:
        """Run test cases and return results"""
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(test_case_class)
        runner = unittest.TextTestRunner(verbosity=2)
        return runner.run(suite) 