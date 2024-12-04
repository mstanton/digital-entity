import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import queue
import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import os

class FocusAssistantUI:
    def __init__(self, focus_agent, voice_assistant):
        self.root = tk.Tk()
        self.root.title("AI Focus Assistant")
        self.root.geometry("1200x800")
        
        self.focus_agent = focus_agent
        self.voice_assistant = voice_assistant
        self.message_queue = queue.Queue()
        
        # Load interaction history
        self.interaction_history = self.load_history()
        
        self.setup_ui()
        self.setup_graphs()
        
        # Start message processing thread
        self.processing = True
        self.message_thread = threading.Thread(target=self.process_messages)
        self.message_thread.start()
        
    def setup_ui(self):
        """Setup the main UI components"""
        # Create main frames
        left_frame = ttk.Frame(self.root)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        right_frame = ttk.Frame(self.root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Task management section
        task_frame = ttk.LabelFrame(left_frame, text="Task Management")
        task_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(task_frame, text="Task:").pack(side=tk.LEFT, padx=5)
        self.task_entry = ttk.Entry(task_frame)
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        ttk.Label(task_frame, text="Priority:").pack(side=tk.LEFT, padx=5)
        self.priority_var = tk.StringVar(value="1")
        priority_spin = ttk.Spinbox(task_frame, from_=1, to=3, width=5, 
                                  textvariable=self.priority_var)
        priority_spin.pack(side=tk.LEFT, padx=5)
        
        add_button = ttk.Button(task_frame, text="Add Task", 
                              command=self.add_task)
        add_button.pack(side=tk.LEFT, padx=5)
        
        # Task list
        task_list_frame = ttk.LabelFrame(left_frame, text="Tasks")
        task_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.task_list = ttk.Treeview(task_list_frame, columns=("Priority", "Status"))
        self.task_list.heading("#0", text="Task")
        self.task_list.heading("Priority", text="Priority")
        self.task_list.heading("Status", text="Status")
        self.task_list.pack(fill=tk.BOTH, expand=True)
        
        # Timer section
        timer_frame = ttk.LabelFrame(left_frame, text="Focus Timer")
        timer_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.timer_label = ttk.Label(timer_frame, text="25:00", 
                                   font=("Arial", 24))
        self.timer_label.pack(pady=10)
        
        timer_buttons = ttk.Frame(timer_frame)
        timer_buttons.pack(fill=tk.X)
        
        ttk.Button(timer_buttons, text="Start Session", 
                  command=self.start_session).pack(side=tk.LEFT, expand=True)
        ttk.Button(timer_buttons, text="Complete Task", 
                  command=self.complete_task).pack(side=tk.LEFT, expand=True)
        
        # Interaction log
        log_frame = ttk.LabelFrame(right_frame, text="Interaction Log")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Voice control
        voice_frame = ttk.LabelFrame(right_frame, text="Voice Control")
        voice_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(voice_frame, text="Toggle Voice", 
                  command=self.toggle_voice).pack(fill=tk.X)
        
    def setup_graphs(self):
        """Setup visualization graphs"""
        graph_frame = ttk.LabelFrame(self.root, text="Analytics")
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create figure with subplots
        self.fig = Figure(figsize=(12, 4))
        self.task_progress = self.fig.add_subplot(131)
        self.focus_time = self.fig.add_subplot(132)
        self.priority_dist = self.fig.add_subplot(133)
        
        # Add canvas to window
        canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def update_graphs(self):
        """Update visualization graphs"""
        # Clear previous plots
        self.task_progress.clear()
        self.focus_time.clear()
        self.priority_dist.clear()
        
        # Task progress
        completed = sum(1 for task in self.focus_agent.tasks if task['completed'])
        total = len(self.focus_agent.tasks)
        self.task_progress.pie([completed, total-completed], 
                             labels=['Completed', 'Remaining'])
        self.task_progress.set_title('Task Progress')
        
        # Focus time distribution
        times = []
        for task in self.focus_agent.tasks:
            if task['start_time'] and task['end_time']:
                duration = (task['end_time'] - task['start_time']).total_seconds() / 60
                times.append(duration)
        if times:
            self.focus_time.hist(times, bins=10)
            self.focus_time.set_title('Focus Session Duration (minutes)')
        
        # Priority distribution
        priorities = [task['priority'] for task in self.focus_agent.tasks]
        if priorities:
            self.priority_dist.hist(priorities, bins=3, range=(1, 4))
            self.priority_dist.set_title('Task Priority Distribution')
        
        self.fig.canvas.draw()
        
    def add_task(self):
        """Add a new task"""
        task_name = self.task_entry.get()
        priority = int(self.priority_var.get())
        
        if task_name:
            self.focus_agent.add_task(task_name, priority)
            self.task_list.insert("", "end", text=task_name, 
                                values=(priority, "Pending"))
            self.task_entry.delete(0, tk.END)
            self.log_interaction(f"Added task: {task_name} (Priority: {priority})")
            self.update_graphs()
            
    def start_session(self):
        """Start a focus session"""
        threading.Thread(target=self.focus_session_thread).start()
        
    def focus_session_thread(self):
        """Handle focus session in separate thread"""
        self.focus_agent.start_focus_session()
        self.update_graphs()
        
    def complete_task(self):
        """Mark current task as complete"""
        self.focus_agent.complete_task()
        if self.focus_agent.current_task:
            task_name = self.focus_agent.current_task['name']
            for item in self.task_list.get_children():
                if self.task_list.item(item)['text'] == task_name:
                    self.task_list.set(item, "Status", "Completed")
            self.log_interaction(f"Completed task: {task_name}")
        self.update_graphs()
        
    def toggle_voice(self):
        """Toggle voice control"""
        # Implementation depends on voice_assistant setup
        pass
        
    def log_interaction(self, message):
        """Log user interaction"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
        # Save to history
        self.interaction_history.append({
            'timestamp': timestamp,
            'message': message
        })
        self.save_history()
        
    def load_history(self):
        """Load interaction history from file"""
        try:
            with open('interaction_history.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
            
    def save_history(self):
        """Save interaction history to file"""
        with open('interaction_history.json', 'w') as f:
            json.dump(self.interaction_history, f)
            
    def process_messages(self):
        """Process messages from queue"""
        while self.processing:
            try:
                message = self.message_queue.get(timeout=0.1)
                self.log_interaction(message)
            except queue.Empty:
                continue
                
    def run(self):
        """Start the UI"""
        self.root.mainloop()
        self.processing = False
        self.message_thread.join() 