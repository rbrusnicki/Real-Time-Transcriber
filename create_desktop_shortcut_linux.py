import os
import sys
import platform
import subprocess

def create_desktop_shortcut():
    """Create a desktop shortcut for the transcription application on Linux"""
    # Get absolute paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, "gui_transcriber.py")
    icon_path = os.path.join(script_dir, "microphone.png")  # Use PNG for Linux
    
    # Get desktop path
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    
    # Create .desktop file content with absolute paths
    desktop_file_content = f"""[Desktop Entry]
Type=Application
Name=Real-Time Transcriber
Comment=Real-Time Speech Transcription using Whisper
Exec=python3 "{script_path}"
Icon={icon_path}
Terminal=false
Categories=Utility;AudioVideo;
Path={script_dir}
StartupNotify=true
"""
    
    # Write to desktop file
    desktop_file_path = os.path.join(desktop_path, "real-time-transcriber.desktop")
    with open(desktop_file_path, "w") as f:
        f.write(desktop_file_content)
    
    # Make the desktop file executable
    os.chmod(desktop_file_path, 0o755)
    
    print(f"Created desktop shortcut at: {desktop_file_path}")
    
    # Create application launcher in ~/.local/share/applications
    local_apps_dir = os.path.join(os.path.expanduser("~"), ".local", "share", "applications")
    if not os.path.exists(local_apps_dir):
        os.makedirs(local_apps_dir)
    
    local_desktop_path = os.path.join(local_apps_dir, "real-time-transcriber.desktop")
    with open(local_desktop_path, "w") as f:
        f.write(desktop_file_content)
    
    # Make the application launcher executable
    os.chmod(local_desktop_path, 0o755)
    
    # Update desktop database
    try:
        os.system("update-desktop-database ~/.local/share/applications")
    except:
        pass
    
    print(f"Created application launcher at: {local_desktop_path}")
    print("\nTo add to favorites/dock:")
    print("1. Open the application from the desktop shortcut or application menu")
    print("2. Right-click on the icon in the dock/dash")
    print("3. Select 'Add to Favorites' or equivalent option for your desktop environment")
    
    return desktop_file_path

if __name__ == "__main__":
    if platform.system() != "Linux":
        print("This script is for Linux only. Please use create_desktop_shortcut.py on Windows.")
        sys.exit(1)
        
    # First, make sure the icon exists
    if not os.path.exists("microphone.png"):
        print("Creating icon first...")
        import create_icon_linux
        create_icon_linux.create_microphone_icon()
    
    # Now create the shortcut
    shortcut_path = create_desktop_shortcut()
    print(f"Shortcut created at: {shortcut_path}")
    print("You can now start the transcriber by double-clicking the shortcut on your desktop.") 