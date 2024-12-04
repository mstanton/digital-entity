# Digital Entity Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

#### 1. Package Installation Failures
```bash
# Error: Failed to install dependencies
pip install -r requirements.txt
```

Solutions:
- Update pip: `python -m pip install --upgrade pip`
- Install system dependencies:
  ```bash
  # Ubuntu/Debian
  sudo apt-get install python3-dev portaudio19-dev
  sudo apt-get install espeak
  
  # macOS
  brew install portaudio
  brew install espeak
  
  # Windows
  # Install Visual C++ Build Tools
  ```

#### 2. Tkinter Missing
Error: `ModuleNotFoundError: No module named 'tkinter'`

Solutions:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS
brew install python-tk@3.8  # Replace 3.8 with your Python version

# Windows
# Reinstall Python with tcl/tk option checked
```

### Voice Recognition Issues

#### 1. Microphone Access
Error: `pyaudio.PyAudioError: No Default Input Device Found`

Solutions:
- Check system microphone settings
- Grant microphone permissions to Python
- Test microphone:
```python
import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Microphone working!")
```

#### 2. Speech Recognition Failures
Error: `speech_recognition.UnknownValueError`

Solutions:
- Check internet connection (needed for Google Speech Recognition)
- Reduce background noise
- Adjust microphone sensitivity:
```python
# In voice_assistant.py
with sr.Microphone() as source:
    self.recognizer.adjust_for_ambient_noise(source, duration=1)
```

### UI Display Issues

#### 1. Matplotlib Rendering
Error: `RuntimeError: main thread is not in main loop`

Solutions:
```python
# In ui_manager.py
import matplotlib
matplotlib.use('TkAgg')  # Set backend before other imports
```

#### 2. Window Scaling Issues
Problem: UI elements too large/small

Solutions:
```python
# In ui_manager.py
class FocusAssistantUI:
    def __init__(self):
        self.root.tk.call('tk', 'scaling', 1.0)  # Adjust scaling
```

### Performance Issues

#### 1. High CPU Usage
Problem: Application consuming excessive resources

Solutions:
```python
# In focus_agent.py
def start_focus_session(self):
    time.sleep(0.1)  # Add small delay in loops
```

#### 2. Memory Leaks
Problem: Growing memory usage

Solutions:
- Clear matplotlib figures:
```python
# In ui_manager.py
def update_graphs(self):
    plt.close('all')  # Clear old figures
```

### Data Persistence Issues

#### 1. File Permission Errors
Error: `PermissionError: [Errno 13] Permission denied`

Solutions:
```python
# Use proper file paths
import os

def save_history(self):
    file_path = os.path.join(os.path.expanduser('~'), '.digital_entity', 'history.json')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(self.interaction_history, f)
```

#### 2. Corrupted Data Files
Problem: JSON decode errors

Solutions:
```python
def load_history(self):
    try:
        with open('interaction_history.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return empty history on error
```

## Development Environment Issues

### 1. Testing Environment
Problem: Tests failing in tox

Solutions:
```ini
# In tox.ini
[testenv]
deps = 
    -r requirements-dev.txt
setenv =
    PYTHONPATH = {toxinidir}
commands =
    pytest {posargs:tests}
```

### 2. Pre-commit Hook Issues
Problem: Pre-commit hooks failing

Solutions:
```yaml
# In .pre-commit-config.yaml
repos:
-   repo: local
    hooks:
    -   id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
```

## Debugging Tips

### 1. Enable Debug Logging
```python
# Add to main.py
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='digital_entity.log'
)
```

### 2. UI Debugging
```python
# In ui_manager.py
def __init__(self):
    self.root.bind('<Control-d>', self.show_debug_info)

def show_debug_info(self, event=None):
    """Display debug information window"""
    debug_window = tk.Toplevel(self.root)
    debug_window.title("Debug Info")
    
    info = f"""
    Tasks: {len(self.focus_agent.tasks)}
    Current Task: {self.focus_agent.current_task}
    Memory Usage: {self.get_memory_usage()}
    """
    
    ttk.Label(debug_window, text=info).pack(padx=10, pady=10)
```

## System-Specific Issues

### Windows
- Path separator issues
- Audio device selection
- Font rendering

### macOS
- Microphone permissions
- tkinter on M1 chips
- Voice synthesis

### Linux
- Missing system dependencies
- Audio configuration
- Display scaling

## Getting Help

1. Check the logs:
```bash
cat digital_entity.log
```

2. Generate system info:
```python
def get_system_info():
    import platform
    import sys
    
    return {
        'os': platform.system(),
        'python': sys.version,
        'packages': pip.freeze(),
    }
```

3. Report issues:
- Include system info
- Provide error logs
- Describe steps to reproduce

## Contributing Solutions

Found a fix? Please:
1. Document the solution
2. Add test cases
3. Update this guide
4. Submit a pull request 