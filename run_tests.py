import unittest
from tests.test_helper import TestGenerator, CodeAnalyzer, TestRunner
from tests.test_focus_agent import TestFocusAgent, TestFocusAgentIntegration
import sys
import os

def run_all_tests():
    """Run all test cases and analyze code"""
    # Run unit tests
    test_classes = [TestFocusAgent, TestFocusAgentIntegration]
    
    for test_class in test_classes:
        print(f"\nRunning tests for {test_class.__name__}")
        result = TestRunner.run_tests(test_class)
        
        if not result.wasSuccessful():
            print(f"❌ {test_class.__name__} tests failed!")
        else:
            print(f"✅ {test_class.__name__} tests passed!")
            
    # Analyze code quality
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.py') and not file.startswith('test_'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    source = f.read()
                    issues = CodeAnalyzer.check_code_quality(source)
                    if issues:
                        print(f"\nPotential issues in {file}:")
                        for issue in issues:
                            print(f"- {issue}")

if __name__ == '__main__':
    run_all_tests() 