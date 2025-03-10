# Real-Time Speech Transcription

This script uses OpenAI's Whisper model to transcribe speech from your microphone in real-time and type it into any window you choose. The application supports multiple languages and provides visual feedback during transcription.

## Features

- Real-time speech transcription using OpenAI's Whisper model
- Multi-language support with interface localization
- Visual feedback during active transcription
- Optional detection logging
- Cross-platform support (Windows and Linux)
- Automatic language detection option

## Requirements

- Python 3.7+
- OpenAI Whisper
- PyAudio
- NumPy
- Pynput
- Pillow (for icon creation)
- Tkinter (for GUI)

### Platform-specific Requirements
- Windows: Pywin32 and Winshell (for desktop shortcut creation)
- Linux: portaudio19-dev (for PyAudio)

## Installation

### Windows Installation

1. Run the setup script:
```bash
python setup.py
```

### Ubuntu/Linux Installation

1. Install system dependencies:
```bash
sudo apt-get update
sudo apt-get install -y portaudio19-dev python3-dev python3-tk
```

2. Run the setup script:
```bash
python3 setup.py
```

## Usage

### Interface Features

1. **Language Selection**:
   - Choose from multiple supported languages including:
     - English
     - Portuguese
     - Chinese
     - German
     - Spanish
     - French
     - Italian
     - Japanese
     - Korean
     - Russian
   - Auto-detect option available
   - Interface language updates automatically with selection

2. **Detection Logging**:
   - Toggle logging on/off using the checkbox
   - When enabled, shows all detection attempts and transcriptions
   - Logs are saved to `whisper_detection_log.txt`

3. **Visual Feedback**:
   - Interface changes color during active transcription
   - Returns to normal color when transcription is paused/stopped

4. **Status Display**:
   - Shows current status and model loading progress
   - Displays first-time download information
   - Indicates when ready for trigger phrase

### Basic Operation

1. Start the application using the desktop shortcut or command line
2. Select your preferred transcription language
3. Enable/disable logging as needed
4. Say "Hey Jarvis" to activate transcription
5. Speak your text to be transcribed
6. Uses any mouse/keyboard input to stop current transcription

### Stopping Transcription Program

You can stop the transcription program by:
- Clicking the Stop button
- Closing the application window

## Notes

- First-time startup will download the Whisper model large (about 2.9GB)
- The trigger detection is language-agnostic for better recognition
- Transcription automatically pauses when keyboard/mouse is used
- Interface language changes affect all text elements including acknowledgments
- Log toggle affects only detection logging, not status messages

## Troubleshooting

### Ubuntu/Linux Issues

1. **PyAudio Installation**:
   ```bash
   sudo apt-get install -y portaudio19-dev python3-dev
   pip3 install pyaudio
   ```

2. **Desktop Shortcut**:
   ```bash
   chmod +x ~/Desktop/real-time-transcriber.desktop
   ```

### Windows Issues

1. **Icon Not Showing**: Try running as administrator once
2. **Desktop Shortcut**: Verify all paths in the shortcut are correct 