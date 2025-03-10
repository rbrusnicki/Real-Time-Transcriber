import os
import sys
import winshell
from win32com.client import Dispatch

def create_desktop_shortcut():
    """Create a desktop shortcut for the transcription application"""
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bat_path = os.path.join(script_dir, "start_transcriber.bat")
    icon_path = os.path.join(script_dir, "microphone.ico")
    
    # Get desktop path
    desktop = winshell.desktop()
    shortcut_path = os.path.join(desktop, "Real-Time Transcriber.lnk")
    
    # Create shortcut
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = bat_path
    shortcut.WorkingDirectory = script_dir
    shortcut.IconLocation = icon_path
    shortcut.save()
    
    return shortcut_path

if __name__ == "__main__":
    # First, make sure the icon exists
    if not os.path.exists("microphone.ico"):
        print("Creating icon first...")
        import create_icon
        create_icon.create_microphone_icon()
    
    # Now create the shortcut
    shortcut_path = create_desktop_shortcut()
    print(f"Shortcut created at: {shortcut_path}")
    print("You can now start the transcriber by double-clicking the shortcut on your desktop.") 