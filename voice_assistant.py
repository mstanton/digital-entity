import speech_recognition as sr
import pyttsx3
from datetime import datetime

class VoiceAssistant:
    """Digital Entity's voice interaction component"""
    def __init__(self):
        # Initialize the text-to-speech engine
        self.engine = pyttsx3.init()
        # Initialize the speech recognizer
        self.recognizer = sr.Recognizer()
        
    def speak(self, text):
        """Convert text to speech"""
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
        
    def listen(self):
        """Listen for voice input and convert to text"""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text.lower()
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                print("Could not understand audio")
                return ""
            except sr.RequestError:
                print("Could not request results")
                return ""

    def process_command(self, command, focus_agent):
        """Process voice commands and interact with the focus agent"""
        if "add task" in command:
            self.speak("What task would you like to add?")
            task_name = self.listen()
            if task_name:
                self.speak("What priority level? 1, 2, or 3?")
                priority = self.listen()
                try:
                    priority = int(priority)
                    if 1 <= priority <= 3:
                        focus_agent.add_task(task_name, priority)
                        self.speak(f"Added task: {task_name}")
                    else:
                        self.speak("Invalid priority level")
                except ValueError:
                    self.speak("Invalid priority level")
                    
        elif "start session" in command or "start focus" in command:
            self.speak("Starting focus session")
            focus_agent.start_focus_session()
            
        elif "complete task" in command or "finish task" in command:
            focus_agent.complete_task()
            self.speak("Task marked as complete")
            
        elif "progress report" in command or "show progress" in command:
            focus_agent.get_progress_report()
            
        elif "exit" in command or "quit" in command:
            self.speak("Goodbye!")
            return "exit"
            
        return "continue" 