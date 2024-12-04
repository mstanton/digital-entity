import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from focus_agent import FocusAgent

class TestFocusAgent(unittest.TestCase):
    def setUp(self):
        self.agent = FocusAgent()
        
    def test_add_task(self):
        """Test adding tasks with different priorities"""
        # Test adding a task with valid priority
        self.agent.add_task("Test task", 1)
        self.assertEqual(len(self.agent.tasks), 1)
        self.assertEqual(self.agent.tasks[0]['name'], "Test task")
        self.assertEqual(self.agent.tasks[0]['priority'], 1)
        
        # Test adding a task with invalid priority
        with self.assertRaises(ValueError):
            self.agent.add_task("Invalid task", 0)
            
    def test_start_focus_session(self):
        """Test focus session functionality"""
        # Mock datetime and time.sleep for testing
        with patch('focus_agent.datetime') as mock_datetime:
            mock_datetime.now.side_effect = [
                datetime(2024, 1, 1, 12, 0),  # Start time
                datetime(2024, 1, 1, 12, 25)   # End time
            ]
            
            # Add a task and start session
            self.agent.add_task("Test task", 1)
            with patch('focus_agent.time.sleep'):  # Prevent actual sleeping
                self.agent.start_focus_session()
                
            # Verify session timing
            self.assertIsNotNone(self.agent.current_task['start_time'])
            self.assertIsNotNone(self.agent.current_task['end_time'])
            
    def test_complete_task(self):
        """Test task completion"""
        self.agent.add_task("Test task", 1)
        self.agent.current_task = self.agent.tasks[0]
        self.agent.complete_task()
        
        self.assertTrue(self.agent.tasks[0]['completed'])
        
    def test_get_progress_report(self):
        """Test progress reporting"""
        # Add multiple tasks
        self.agent.add_task("Task 1", 1)
        self.agent.add_task("Task 2", 2)
        
        # Complete one task
        self.agent.current_task = self.agent.tasks[0]
        self.agent.complete_task()
        
        # Capture printed output
        with patch('builtins.print') as mock_print:
            self.agent.get_progress_report()
            mock_print.assert_any_call("Completed: 1/2 tasks")

class TestFocusAgentIntegration(unittest.TestCase):
    """Integration tests for FocusAgent"""
    
    def test_full_workflow(self):
        """Test complete workflow of adding, starting, and completing tasks"""
        agent = FocusAgent()
        
        # Add multiple tasks
        agent.add_task("Task 1", 1)
        agent.add_task("Task 2", 2)
        
        # Start and complete sessions
        with patch('focus_agent.time.sleep'):
            agent.start_focus_session()
            agent.complete_task()
            agent.start_focus_session()
            agent.complete_task()
            
        # Verify all tasks completed
        completed_tasks = sum(1 for task in agent.tasks if task['completed'])
        self.assertEqual(completed_tasks, 2) 