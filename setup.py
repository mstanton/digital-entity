from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="digital-entity",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A digital entity that helps manage focus and productivity",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/digital-entity",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Time Management",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "SpeechRecognition>=3.8.1",
        "pyttsx3>=2.90",
        "pyaudio>=0.2.11",
        "matplotlib>=3.5.0",
    ],
    entry_points={
        "console_scripts": [
            "digital-entity=digital_entity.main:main",
        ],
    },
) 