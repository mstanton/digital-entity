from focus_agent import FocusAgent
from voice_assistant import VoiceAssistant
from ui_manager import FocusAssistantUI

def main():
    """Initialize and run the Digital Entity"""
    agent = FocusAgent()
    voice = VoiceAssistant()
    ui = FocusAssistantUI(agent, voice)
    ui.run()

if __name__ == "__main__":
    main() 