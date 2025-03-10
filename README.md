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

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Create the desktop shortcut:

```bash
python create_desktop_shortcut.py
```

This will create a microphone icon and a shortcut on your desktop that you can use to start the application.

## Usage

### Starting with Desktop Shortcut

1. Double-click the "Real-Time Transcriber" shortcut on your desktop.

2. The application window will open, showing the status and a log of detection attempts.

### Starting from Command Line

If you prefer to start from the command line, you can run:

```bash
python gui_transcriber.py
```

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

The application now has a graphical user interface that shows:

1. **Status Display**: Shows the current status of the transcription system (e.g., "Waiting for trigger", "Transcribing").

2. **Log Window**: Displays all detection attempts and transcription activities in real-time.

3. **Stop Button**: Allows you to stop the transcription process.

The GUI helps you monitor what the system is detecting and transcribing, making it easier to diagnose any issues with trigger phrase detection.

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

- Each recording segment is 3 seconds. You can adjust this by changing the `RECORD_SECONDS` variable.

- The cooldown period after keyboard/mouse activity is 2 seconds. You can adjust this by changing the `INPUT_COOLDOWN` variable.

## Notes

- The script uses the Whisper "large" model for improved accuracy.
- The trigger detection is language-agnostic to better recognize "Hey Jarvis" regardless of accent.
- The improved trigger detection can recognize various pronunciations and partial matches.
- All detection attempts are logged only during trigger detection (not during active transcription).
- After trigger detection, the script is configured to transcribe in Portuguese, but can be modified for other languages.
- The script adds a space after each transcription segment.
- For better performance, ensure you're in a quiet environment with clear speech. 