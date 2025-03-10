import os
import sys
import subprocess
import importlib.util

def check_module(module_name):
    """Check if a Python module is installed"""
    return importlib.util.find_spec(module_name) is not None

def install_dependencies():
    """Install required dependencies"""
    print("Checking and installing dependencies...")
    
    try:
        # Install required packages using pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully.")
        return True
    except Exception as e:
        print(f"Error installing dependencies: {e}")
        return False

def create_icon():
    """Create the application icon"""
    print("Creating application icon...")
    
    if not os.path.exists("microphone.ico"):
        try:
            import create_icon
            icon_path = create_icon.create_microphone_icon()
            print(f"Icon created at: {icon_path}")
        except Exception as e:
            print(f"Error creating icon: {e}")
            return False
    else:
        print("Icon already exists.")
    
    return True

def create_shortcut():
    """Create desktop shortcut"""
    print("Creating desktop shortcut...")
    
    try:
        import create_desktop_shortcut
        shortcut_path = create_desktop_shortcut.create_desktop_shortcut()
        print(f"Shortcut created at: {shortcut_path}")
        return True
    except Exception as e:
        print(f"Error creating shortcut: {e}")
        return False

def main():
    """Main setup function"""
    print("Starting Real-Time Transcriber setup...")
    
    # Install dependencies
    if not install_dependencies():
        print("Failed to install dependencies. Please try installing them manually.")
        return
    
    # Create icon
    if not create_icon():
        print("Failed to create icon.")
        return
    
    # Create shortcut
    if not create_shortcut():
        print("Failed to create desktop shortcut.")
        return
    
    print("\nSetup completed successfully!")
    print("You can now start the application by double-clicking the 'Real-Time Transcriber' icon on your desktop.")
    
    # Ask if user wants to run the application now
    response = input("Do you want to start the application now? (y/n): ")
    if response.lower() == 'y':
        print("Starting application...")
        os.system("python gui_transcriber.py")

if __name__ == "__main__":
    main() 