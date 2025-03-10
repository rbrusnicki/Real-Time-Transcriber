# Real-Time Speech Transcription

This script uses OpenAI's Whisper model to transcribe speech from your microphone in real-time and type it into any window you choose. The script uses a two-step approach: language-agnostic detection for the trigger phrase, followed by Portuguese language transcription.

## Requirements

- Python 3.7+
- OpenAI Whisper (already installed)
- PyAudio
- NumPy
- Keyboard
- Pynput
- Pystray (for system tray icon)
- Pillow (for icon image creation)

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Starting with System Tray Icon

1. Run the tray icon application:
   ```bash
   python tray_icon.py
   ```

2. A microphone icon will appear in your system tray (notification area).

3. Right-click the icon and select "Start Transcription" to launch the transcription tool.

4. To exit the tray icon application, right-click the icon and select "Exit".

### Using the Transcription Tool

1. When the transcription tool starts, it will load the Whisper model (this may take a moment).

2. Focus on the window where you want the text to appear.

3. Say the trigger phrase "Hey Jarvis" to activate transcription mode. The script can recognize variations like "Ei Jarvis" or even detect just the word "Jarvis".

4. The script will type "Sim?" to acknowledge it heard you.

5. Start speaking in Portuguese, and the script will:
   - Erase the "Sim?" acknowledgment
   - Type your transcribed speech in its place

6. **The transcription will automatically pause when you use your keyboard or mouse.** This prevents interference with your manual typing.

7. To resume transcription after using keyboard/mouse, say the trigger phrase "Hey Jarvis" again.

8. Press the `Esc` key to stop the recording and exit the script completely.

## Trigger Detection Logging

The script logs detection attempts only when it's waiting for the trigger phrase (not during active transcription). Every time you speak:

- The script records what was actually detected by Whisper
- It logs whether the trigger was successfully recognized or missed
- All logs are stored in `whisper_detection_log.txt` with timestamps
- This helps identify common misinterpretations for future improvement

The log file format is:
```
[TIMESTAMP] DETECTED (variation): transcribed text
[TIMESTAMP] MISSED: transcribed text
```

## Customization

- **Language Settings**: The script is currently configured to transcribe in Portuguese, but you can change it to any language by modifying the `language` parameter in the `model.transcribe()` function in the `process_audio()` method. For example:
  ```python
  # For English:
  result = model.transcribe(audio_data, fp16=False, language="en", task="transcribe")

  # For German:
  result = model.transcribe(audio_data, fp16=False, language="de", task="transcribe")

  # For French:
  result = model.transcribe(audio_data, fp16=False, language="fr", task="transcribe")
  
  # For Italian:
  result = model.transcribe(audio_data, fp16=False, language="it", task="transcribe")
  
  # For Spanish:
  result = model.transcribe(audio_data, fp16=False, language="es", task="transcribe")
  ```

- **Trigger Phrase Settings**: The script now recognizes multiple variations of the trigger phrase. You can modify or add more variations by editing the `TRIGGER_VARIATIONS` list in the script:
  ```python
  TRIGGER_VARIATIONS = ["hey jarvis", "ei jarvis", "hey service", "hey travis", "a jarvis", "hey jarbas", "hey davis"]
  ```

- **Tray Icon Appearance**: You can modify the appearance of the tray icon by editing the `create_image` function in `tray_icon.py`.

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