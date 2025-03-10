# Real-Time Speech Transcription

This script uses OpenAI's Whisper model to transcribe speech from your microphone in real-time and type it into any window you choose. The script uses a two-step approach: language-agnostic detection for the trigger phrase, followed by Portuguese language transcription.

## Requirements

- Python 3.7+
- OpenAI Whisper (already installed)
- PyAudio
- NumPy
- Keyboard
- Pynput
- Pillow (for icon creation)
- Tkinter (for GUI)
- Pywin32 and Winshell (for desktop shortcut creation)

## Installation

1. The easiest way to set everything up is to run the setup script:

```bash
python setup.py
```

This will:
- Install all required dependencies
- Create the application icon
- Create a desktop shortcut

2. Alternatively, you can install the components individually:

```bash
# Install dependencies
pip install -r requirements.txt

# Create desktop shortcut
python create_desktop_shortcut.py
```

## Usage

### Starting with Desktop Shortcut

1. Double-click the "Real-Time Transcriber" shortcut on your desktop.

2. The application window will open, showing the status and a log of detection attempts.

### Alternative Shortcuts

If the main shortcut doesn't work or you have issues with the icon in the taskbar, several alternative shortcuts are created for you:

- **Real-Time Transcriber (Alt 1)** - Uses a simplified .bat file
- **Real-Time Transcriber (Alt 2)** - Uses a .cmd file that tries to find Python in multiple locations
- **Real-Time Transcriber (Direct)** - Calls pythonw.exe directly with the script as an argument

Try each of these alternatives if you encounter problems with the main shortcut.

### Pinning to Taskbar

To pin the application to your taskbar for easy access:

1. Start the application once using one of the desktop shortcuts
2. Right-click on the application icon in the taskbar
3. Select "Pin to taskbar"

Now you can launch the application directly from your taskbar.

> **Note About Taskbar Icon:** If the icon in the taskbar appears as a generic Python icon instead of the microphone icon, try using one of the alternative shortcuts instead. These shortcuts use different methods that may work better with the Windows taskbar.

### Starting from Command Line

If you prefer to start from the command line, you can run:

```bash
pythonw gui_transcriber.py
```

The `pythonw` command runs the script without showing a terminal window.

### Using the Transcription Tool

1. When the application starts, it will load the Whisper model (this may take a moment).

2. Once loaded, the application will show "Aguardando comando 'Hey Jarvis'" (Waiting for 'Hey Jarvis' command).

3. Focus on the window where you want the text to appear.

4. Say the trigger phrase "Hey Jarvis" to activate transcription mode. The script can recognize variations like "Ei Jarvis" or even detect just the word "Jarvis".

5. The script will type "Sim?" to acknowledge it heard you.

6. Start speaking in Portuguese, and the script will:
   - Erase the "Sim?" acknowledgment
   - Type your transcribed speech in its place

7. **The transcription will automatically pause when you use your keyboard or mouse.** This prevents interference with your manual typing.

8. To resume transcription after using keyboard/mouse, say the trigger phrase "Hey Jarvis" again.

9. You can stop the transcription by:
   - Clicking the "Parar" (Stop) button in the application window
   - Pressing the `Esc` key
   - Closing the application window

## Graphical User Interface

The application has an improved graphical user interface that shows:

1. **Status Display**: Shows the current status of the transcription system (e.g., "Waiting for trigger", "Transcribing").

2. **Log Window**: Displays all detection attempts and transcription activities in real-time.

3. **Stop Button**: A large, easy-to-click button that allows you to stop the transcription process.

The window can be resized as needed, and no terminal window appears when launching from the shortcut.

## Trigger Detection Logging

The script logs detection attempts only when it's waiting for the trigger phrase (not during active transcription). Every time you speak:

- The script records what was actually detected by Whisper
- It logs whether the trigger was successfully recognized or missed
- All logs are stored in `whisper_detection_log.txt` with timestamps and shown in the GUI
- This helps identify common misinterpretations for future improvement

## Customization

- **Language Settings**: The script is currently configured to transcribe in Portuguese, but you can change it to any language by modifying the `language` parameter in the `model.transcribe()` function in the `process_audio()` method. For example:
  ```python
  # For English:
  result = self.model.transcribe(audio_data, fp16=False, language="en", task="transcribe")

  # For German:
  result = self.model.transcribe(audio_data, fp16=False, language="de", task="transcribe")

  # For Italian:
  result = self.model.transcribe(audio_data, fp16=False, language="it", task="transcribe")
  ```

- **Trigger Phrase Settings**: The script recognizes multiple variations of the trigger phrase. You can modify or add more variations by editing the `TRIGGER_VARIATIONS` list in the script.

- **Window Size**: The default window size is 600x400 pixels, but you can resize it as needed or modify the default size in the `gui_transcriber.py` file.

- Each recording segment is 3 seconds. You can adjust this by changing the `RECORD_SECONDS` variable.

- The cooldown period after keyboard/mouse activity is 2 seconds. You can adjust this by changing the `INPUT_COOLDOWN` variable.

## Troubleshooting

### Shortcut Issues

If you're having trouble with the shortcuts:

1. Try running the script directly from the command line:
   ```
   pythonw gui_transcriber.py
   ```

2. If the shortcuts ask how to open the file, make sure:
   - Python is installed correctly
   - The file associations for .bat and .cmd files are set to command processor
   - The Python installation directory is in your PATH environment variable

3. Try each of the alternative shortcuts to see which works best on your system.

## Notes

- The script uses the Whisper "large" model for improved accuracy.
- The trigger detection is language-agnostic to better recognize "Hey Jarvis" regardless of accent.
- The improved trigger detection can recognize various pronunciations and partial matches.
- All detection attempts are logged only during trigger detection (not during active transcription).
- After trigger detection, the script is configured to transcribe in Portuguese, but can be modified for other languages.
- The script adds a space after each transcription segment.
- For better performance, ensure you're in a quiet environment with clear speech. 