  ╭──────────────────────────────╮
  │     Digital Entity 🤖        │
  │                              │
  │         ⏰ (◕‿◕) ☕          │
  │        /||\  ||  /||\        │
  │    Task List  ||  Done!      │
  │                              │
  │  "Your digital companion!"   │
  ╰──────────────────────────────╯
```

# Digital Entity

A modern, intelligent digital companion that helps you stay productive using the Pomodoro Technique. This application combines task management, voice interaction, and visual analytics to enhance your productivity.

## Features

- 🎯 Task management with priority levels
- ⏲️ Visual Pomodoro timer
- 💡 AI-powered focus tips
- 📊 Real-time analytics and visualization
- 🗣️ Voice command support
- 📝 Interactive task list
- 📈 Progress tracking
- 📋 Interaction logging

## Screenshots

[Consider adding screenshots of your UI here]

## Project Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- virtualenv or venv (recommended)
- System audio support (for voice features)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-focus-assistant.git
cd ai-focus-assistant
```

2. Create and activate a virtual environment:
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install development dependencies (optional):
```bash
pip install -r requirements-dev.txt
```

## Usage

### Starting the Application

Run the application:
```bash
python -m ai_focus_assistant
```

### User Interface

The application features a modern graphical interface with several key areas:

1. **Task Management Panel** (Left)
   - Add new tasks with priorities (1-3)
   - View and manage task list
   - Start focus sessions
   - Mark tasks as complete

2. **Focus Timer** (Center)
   - Visual countdown timer
   - Session controls
   - Current task display

3. **Analytics Dashboard** (Bottom)
   - Task completion pie chart
   - Focus session duration histogram
   - Priority distribution graph

4. **Interaction Log** (Right)
   - Real-time activity logging
   - Session history
   - Voice command feedback

### Voice Commands

Toggle voice control using the dedicated button. Available commands:

- "Add task" - Create a new task
- "Start session" - Begin a focus session
- "Complete task" - Mark current task as done
- "Show progress" - View task statistics

### Analytics

The application provides real-time visualization of:

1. **Task Progress**
   - Completed vs. remaining tasks
   - Success rate tracking
   - Priority distribution

2. **Focus Metrics**
   - Session duration patterns
   - Productivity trends
   - Task completion rates

3. **Time Analysis**
   - Focus session distribution
   - Priority-based time allocation
   - Daily/weekly patterns

## Project Structure

```
digital-entity/
├── digital_entity/            # Main package directory
│   ├── __init__.py
│   ├── focus_agent.py        # Core focus tracking
│   ├── voice_assistant.py    # Voice interaction
│   ├── ui_manager.py        # UI components
│   └── main.py              # Entry point
├── tests/                   # Test suite
├── docs/                    # Documentation
└── [config files]          # Configuration files
```

## Development

### Setting Up Development Environment

1. Install development tools:
```bash
pip install -r requirements-dev.txt
pre-commit install
```

2. Run tests:
```bash
pytest
```

3. Check code quality:
```bash
tox -e lint
```

### Key Components

1. **FocusAgent** (`focus_agent.py`)
   - Task management
   - Focus session timing
   - Progress tracking

2. **VoiceAssistant** (`voice_assistant.py`)
   - Speech recognition
   - Voice command processing
   - Audio feedback

3. **FocusAssistantUI** (`ui_manager.py`)
   - Tkinter-based interface
   - Real-time visualization
   - Event handling
   - Data persistence

### Adding New Features

1. UI Components:
```python
def add_new_feature(self):
    feature_frame = ttk.LabelFrame(self.root, text="New Feature")
    # Add your UI components
    self.update_graphs()  # Refresh analytics
```

2. Voice Commands:
```python
def process_new_command(self, command):
    if "new feature" in command:
        self.handle_new_feature()
```

## Testing

Run the test suite:
```bash
# Run all tests
pytest

# Run specific tests
pytest tests/test_focus_agent.py
pytest tests/test_ui_manager.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Implement your changes
5. Run tests and quality checks
6. Submit a pull request

## Troubleshooting

### Common Issues

1. **Voice Recognition Problems**
   - Check microphone settings
   - Verify audio dependencies
   - Test in quiet environment

2. **UI Display Issues**
   - Check tkinter installation
   - Verify matplotlib version
   - Update display drivers

3. **Performance Concerns**
   - Monitor resource usage
   - Check interaction history size
   - Clear cached data

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Pomodoro Technique
- Python tkinter community
- Matplotlib visualization library
- Speech recognition contributors

## Support

For issues and feature requests:
1. Check existing issues
2. Run diagnostic tests
3. Provide system information
4. Submit detailed bug reports
