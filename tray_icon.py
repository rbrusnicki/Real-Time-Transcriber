import pystray
from PIL import Image, ImageDraw
import subprocess
import os
import sys
import threading
import tempfile

def create_image(width, height, color1, color2):
    """Create a simple icon image with two colors"""
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    
    # Draw a microphone-like icon
    dc.rectangle(
        (width//3, height//3, 2*width//3, 2*height//3),
        fill=color2
    )
    dc.rectangle(
        (width//2 - width//10, height//3, width//2 + width//10, 3*height//4),
        fill=color2
    )
    
    return image

def start_transcription():
    """Start the real_time_transcriber.py script"""
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    transcriber_path = os.path.join(script_dir, "real_time_transcriber.py")
    
    # Create a temporary .bat file to launch in a new window
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.bat')
    try:
        with open(temp_file.name, 'w') as f:
            f.write(f'@echo off\n')
            f.write(f'cd /d "{script_dir}"\n')
            f.write(f'python "{transcriber_path}"\n')
            f.write(f'pause\n')
        
        # Execute the bat file
        subprocess.Popen(temp_file.name, shell=True)
    except Exception as e:
        print(f"Error starting transcription: {e}")

def setup(icon):
    """Setup function for the icon"""
    icon.visible = True

def exit_action(icon):
    """Exit the application"""
    icon.stop()

def main():
    """Main function to run the tray icon application"""
    # Create a simple image for the icon
    image = create_image(64, 64, 'blue', 'white')
    
    # Create the icon
    icon = pystray.Icon(
        "Real-Time Transcriber",
        image,
        "Real-Time Transcriber",
        menu=pystray.Menu(
            pystray.MenuItem("Start Transcription", start_transcription),
            pystray.MenuItem("Exit", exit_action)
        )
    )
    
    # Run the icon
    icon.run(setup)

if __name__ == "__main__":
    main() 