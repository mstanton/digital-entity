from datetime import datetime, timedelta
import time
import random

class FocusAgent:
    """Digital Entity's focus management component"""
    def __init__(self):
        self.tasks = []
        self.focus_tips = [
            "Take a 5-minute break every 25 minutes of work",
            "Stay hydrated - drink some water",
            "Do some quick stretches to stay energized",
            "Clear your workspace of distractions",
            "Take a few deep breaths to recenter yourself"
        ]
        self.current_task = None
        self.work_duration = timedelta(minutes=25)  # Default Pomodoro duration
        
    def add_task(self, task_name, priority=1):
        """Add a new task to the focus list"""
        self.tasks.append({
            'name': task_name,
            'priority': priority,
            'completed': False,
            'start_time': None,
            'end_time': None
        })
        print(f"Added task: {task_name}")
        
    def start_focus_session(self):
        """Start a focused work session"""
        if not self.tasks:
            print("No tasks available. Please add tasks first.")
            return
            
        self.current_task = next((task for task in self.tasks if not task['completed']), None)
        if not self.current_task:
            print("All tasks completed!")
            return
            
        print(f"\nStarting focus session for: {self.current_task['name']}")
        print(f"Focus tip: {random.choice(self.focus_tips)}")
        
        self.current_task['start_time'] = datetime.now()
        end_time = datetime.now() + self.work_duration
        
        try:
            while datetime.now() < end_time:
                remaining = end_time - datetime.now()
                print(f"\rTime remaining: {remaining.seconds//60}:{remaining.seconds%60:02d}", end="")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\nSession interrupted!")
            
        self.current_task['end_time'] = datetime.now()
        print("\nSession completed!")
        
    def complete_task(self):
        """Mark the current task as completed"""
        if self.current_task:
            self.current_task['completed'] = True
            print(f"Completed task: {self.current_task['name']}")
            
    def get_progress_report(self):
        """Get a summary of completed and remaining tasks"""
        completed = sum(1 for task in self.tasks if task['completed'])
        total = len(self.tasks)
        
        print(f"\nProgress Report:")
        print(f"Completed: {completed}/{total} tasks")
        print("\nRemaining tasks:")
        for task in self.tasks:
            if not task['completed']:
                print(f"- {task['name']}") 