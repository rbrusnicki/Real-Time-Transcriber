import whisper
import pyaudio
import numpy as np
import threading
import queue
import time
import keyboard
from pynput.keyboard import Controller, Listener as KeyboardListener, Key
from pynput.mouse import Listener as MouseListener

# Initialize the Whisper model
# Using a smaller model for faster real-time transcription
print("Loading Whisper model...")
model = whisper.load_model("large")
print("Model loaded!")

# Initialize keyboard controller for typing
keyboard_controller = Controller()

# Audio recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 3  # Length of each recording chunk

# Create a queue to hold audio chunks
audio_queue = queue.Queue()
# Flags to control recording and transcription
recording = True
triggered = False
TRIGGER_PHRASE = "hey jarvis"
# Add a lock for thread safety
input_lock = threading.Lock()
# Time to wait after user input before allowing transcription to resume
INPUT_COOLDOWN = 2.0  # seconds
last_input_time = 0
# Flag to identify when the script is typing vs user typing
is_typing = False
# Flag to track if acknowledgment was typed and needs to be erased
acknowledgment_typed = False

def pause_transcription():
    """Function to pause transcription but keep recording"""
    global triggered
    if triggered:
        triggered = False
        print("Transcription paused. Say the trigger phrase to resume.")

def on_key_press(key):
    """Callback for when a key is pressed"""
    global triggered, last_input_time, is_typing
    # Only respond to keyboard events if the script is not currently typing
    if not is_typing:
        with input_lock:
            if triggered:
                triggered = False
                print("User keyboard activity detected. Transcription paused.")
            last_input_time = time.time()
    return True  # Continue listening

def on_mouse_click(x, y, button, pressed):
    """Callback for when a mouse button is clicked"""
    global triggered, last_input_time
    if pressed:
        with input_lock:
            if triggered:
                triggered = False
                print("User mouse activity detected. Transcription paused.")
            last_input_time = time.time()
    return True  # Continue listening

def type_with_flag(text):
    """Type text with is_typing flag set to prevent detecting own keystrokes"""
    global is_typing
    is_typing = True
    try:
        keyboard_controller.type(text)
    finally:
        is_typing = False

def erase_text(length):
    """Erase a specified number of characters by simulating backspace key presses"""
    global is_typing
    is_typing = True
    try:
        # Try method 1: Using pynput backspace
        for _ in range(length):
            keyboard_controller.press(Key.backspace)
            keyboard_controller.release(Key.backspace)
            time.sleep(0.05)  # Increased delay to ensure backspaces are registered
        
        # Wait a bit to ensure all backspaces have been processed
        time.sleep(0.1)
        
        # Alternatively, try an alternate method: select and delete
        # This can work better in some applications
        # Method 2: select and delete
        """
        # Uncomment this if the backspace method doesn't work reliably
        for _ in range(length):
            keyboard_controller.press(Key.shift)
            keyboard_controller.press(Key.left)
            keyboard_controller.release(Key.left)
            keyboard_controller.release(Key.shift)
        keyboard_controller.press(Key.delete)
        keyboard_controller.release(Key.delete)
        """
        
    finally:
        is_typing = False

def record_audio():
    """Function to record audio from microphone in chunks"""
    print("Starting microphone recording...")
    p = pyaudio.PyAudio()
    
    # Open microphone stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    print("Recording started. Speak into the microphone.")
    print(f"Say '{TRIGGER_PHRASE.title()}' to activate transcription.")
    print("Transcription will automatically pause when you use keyboard or mouse.")
    print("Press 'Esc' to stop recording and exit.")
    
    # Continue recording until stopped
    while recording:
        frames = []
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            if not recording:
                break
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
        
        # Convert audio data to numpy array and add to queue
        if frames and recording:
            audio_data = np.frombuffer(b''.join(frames), dtype=np.int16).astype(np.float32) / 32768.0
            audio_queue.put(audio_data)
    
    # Clean up
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Recording stopped.")

def process_audio():
    """Function to process audio chunks and transcribe using Whisper"""
    global triggered, last_input_time, is_typing, acknowledgment_typed
    last_text = ""
    
    while recording or not audio_queue.empty():
        if not audio_queue.empty():
            # Get audio chunk from queue
            audio_data = audio_queue.get()
            
            # Transcribe audio using Whisper
            try:
                # If not triggered, don't force language to better detect trigger phrase
                if not triggered:
                    # For trigger detection, use general language model (no forced language)
                    result = model.transcribe(audio_data, fp16=False)
                    transcription = result["text"].strip().lower()
                    
                    # Check if we're in the cooldown period after user input
                    with input_lock:
                        cooldown_active = (time.time() - last_input_time) < INPUT_COOLDOWN
                    
                    # Check for trigger phrase
                    if TRIGGER_PHRASE in transcription and not cooldown_active:
                        print("Trigger detected! Starting to transcribe...")
                        with input_lock:
                            triggered = True
                        
                        # Type "Sim?" as acknowledgment instead of robot emoji
                        acknowledgment = "Sim?"
                        type_with_flag(acknowledgment)
                        acknowledgment_typed = True
                        print("Typed acknowledgment: 'Sim?'")
                        
                        # No need to process the trigger phrase text further
                        continue
                    
                else:
                    # For actual transcription, force Portuguese
                    result = model.transcribe(audio_data, fp16=False, language="pt", task="transcribe")
                    transcription = result["text"].strip().lower()
                    
                    # Only process if triggered and we have non-empty transcription
                    if transcription and transcription != last_text:
                        print(f"Transcribed: {transcription}")
                        
                        # # Enhanced filter for English phrases (uncomment if needed)
                        # unwanted_phrases = ["thank you", "thanks", "thank", "you", "obrigado", "obrigada", "thanks for"]
                        # for phrase in unwanted_phrases:
                        #     if phrase in transcription.lower():
                        #         transcription = transcription.lower().replace(phrase, "").strip()
                        #         print(f"Removed unwanted phrase: '{phrase}'")
                        
                        # If transcription is empty after filtering, skip it
                        if not transcription.strip():
                            print("Transcription was empty after filtering, skipping")
                            continue
                        
                        # If we previously typed an acknowledgment, erase it before typing new text
                        if acknowledgment_typed:
                            # Use the actual length of the acknowledgment
                            acknowledgment_length = len("Sim?")
                            print(f"Erasing {acknowledgment_length} characters of acknowledgment")
                            erase_text(acknowledgment_length)
                            acknowledgment_typed = False
                            print("Erased acknowledgment text")
                        
                        # Debug print before typing
                        print(f"Going to type: '{transcription + ' '}'")
                        
                        # Type out the transcription
                        type_with_flag(transcription + " ")
                        
                        last_text = transcription
            except Exception as e:
                print(f"Transcription error: {e}")
                # Ensure typing flag is reset if an error occurs
                is_typing = False
            
            # Small delay to prevent CPU overuse
            time.sleep(0.1)
        else:
            # If queue is empty, wait a bit
            time.sleep(0.1)

def main():
    global recording, last_input_time
    
    # Set up keyboard hook to stop recording when Esc is pressed
    keyboard.add_hotkey('esc', lambda: stop_recording())
    
    # Initialize last input time
    last_input_time = time.time()
    
    # Start keyboard and mouse listeners in separate threads
    keyboard_listener = KeyboardListener(on_press=on_key_press)
    mouse_listener = MouseListener(on_click=on_mouse_click)
    
    keyboard_listener.start()
    mouse_listener.start()
    
    print("Initializing real-time speech transcription...")
    print("Focus on the window where you want the text to appear.")
    print("Wait 3 seconds...")
    time.sleep(3)
    
    # Start recording thread
    record_thread = threading.Thread(target=record_audio)
    record_thread.start()
    
    # Start processing thread
    process_thread = threading.Thread(target=process_audio)
    process_thread.start()
    
    # Wait for recording thread to finish
    record_thread.join()
    process_thread.join()
    
    # Stop listeners
    keyboard_listener.stop()
    mouse_listener.stop()

def stop_recording():
    global recording
    recording = False
    print("Stopping recording...")

if __name__ == "__main__":
    main() 