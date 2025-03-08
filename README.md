# Real-Time Speech Transcription

This script uses OpenAI's Whisper model to transcribe speech from your microphone in real-time and type it into any window you choose. The script uses a two-step approach: language-agnostic detection for the trigger phrase, followed by Portuguese language transcription.

## Requirements

- Python 3.7+
- OpenAI Whisper (already installed)
- PyAudio
- NumPy
- Keyboard
- Pynput

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the script:
   ```bash
   python real_time_transcriber.py
   ```

2. The script will load the Whisper model (this may take a moment).

3. When prompted, focus on the window where you want the text to appear.

4. Say the trigger phrase "Hey Jarvis" to activate transcription mode. The script can recognize variations like "Ei Jarvis" or even detect just the word "Jarvis".

5. The script will type "Sim?" to acknowledge it heard you.

6. Start speaking in Portuguese, and the script will:
   - Erase the "Sim?" acknowledgment
   - Type your transcribed speech in its place

7. **The transcription will automatically pause when you use your keyboard or mouse.** This prevents interference with your manual typing.

8. To resume transcription after using keyboard/mouse, say the trigger phrase "Hey Jarvis" again.

9. Press the `Esc` key to stop the recording and exit the script completely.

## Trigger Detection Logging

The script now logs all trigger detection attempts to help improve accuracy. Every time you speak:

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

- Each recording segment is 3 seconds. You can adjust this by changing the `RECORD_SECONDS` variable.

- The cooldown period after keyboard/mouse activity is 2 seconds. You can adjust this by changing the `INPUT_COOLDOWN` variable.

## Notes

- The script uses the Whisper "large" model for improved accuracy.
- The trigger detection is language-agnostic to better recognize "Hey Jarvis" regardless of accent.
- The improved trigger detection can recognize various pronunciations and partial matches.
- All detection attempts are logged to help improve future recognition.
- After trigger detection, the script is configured to transcribe in Portuguese, but can be modified for other languages.
- The script adds a space after each transcription segment.
- For better performance, ensure you're in a quiet environment with clear speech. 