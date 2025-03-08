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

3. When prompted, focus on the window where you want the transcribed text to appear.

4. Say the trigger phrase "Hey Jarvis" to activate transcription mode.

5. The script will type "Sim?" to acknowledge it heard you.

6. Start speaking in Portuguese, and the script will:
   - Erase the "Sim?" acknowledgment
   - Type your transcribed speech in its place

7. **The transcription will automatically pause when you use your keyboard or mouse.** This prevents interference with your manual typing.

8. To resume transcription after using keyboard/mouse, say the trigger phrase "Hey Jarvis" again.

9. Press the `Esc` key to stop the recording and exit the script completely.

## Customization

- **Language Settings**: The script is currently configured to transcribe in Portuguese, but you can change it to any language by modifying the `language` parameter in the `model.transcribe()` function in the `process_audio()` method. For example:
  ```python
  # For Spanish:
  result = model.transcribe(audio_data, fp16=False, language="es", task="transcribe")
  
  # For English:
  result = model.transcribe(audio_data, fp16=False, language="en", task="transcribe")
  
  # For French:
  result = model.transcribe(audio_data, fp16=False, language="fr", task="transcribe")
  ```

- The default trigger phrase is "Hey Jarvis". You can change it by modifying the `TRIGGER_PHRASE` variable in the script.

- Each recording segment is 3 seconds. You can adjust this by changing the `RECORD_SECONDS` variable.

- The cooldown period after keyboard/mouse activity is 2 seconds. You can adjust this by changing the `INPUT_COOLDOWN` variable.

## Notes

- The script uses the Whisper "large" model for improved accuracy.
- The trigger detection is language-agnostic to better recognize "Hey Jarvis" regardless of accent.
- After trigger detection, the script is configured to transcribe in Portuguese, but can be modified for any language.
- Common English phrases like "thank you" are automatically filtered out.
- The script adds a space after each transcription segment.
- For better performance, ensure you're in a quiet environment with clear speech. 