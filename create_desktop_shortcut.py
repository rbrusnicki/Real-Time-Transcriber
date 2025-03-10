import os
import sys
import winshell
from win32com.client import Dispatch
import ctypes

def create_desktop_shortcut():
    """Create a desktop shortcut for the transcription application"""
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bat_path = os.path.join(script_dir, "start_transcriber.bat")
    cmd_path = os.path.join(script_dir, "start_transcriber.cmd")  # Novo arquivo .cmd
    icon_path = os.path.join(script_dir, "microphone.ico")
    
    # Get desktop path
    desktop = winshell.desktop()
    shortcut_path = os.path.join(desktop, "Real-Time Transcriber.lnk")
    
    # Create primary shortcut (.bat)
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = bat_path
    shortcut.WorkingDirectory = script_dir
    shortcut.IconLocation = icon_path
    shortcut.Description = "Real-Time Speech Transcription using Whisper"
    
    # Add custom AppUserModelID property to ensure icon shows correctly in taskbar
    try:
        # This requires win32com, which we already import
        shortcut.SetProperty('{9F4C2855-9F79-4B39-A8D0-E1D42DE1D5F3}', 5, 'whisper.realtime.transcriber.1.0')
    except:
        print("Warning: Could not set AppUserModelID for taskbar icon.")
    
    shortcut.save()
    
    # Criar atalho alternativo usando o arquivo .cmd
    alt_shortcut_path = os.path.join(desktop, "Real-Time Transcriber (Alt).lnk")
    alt_shortcut = shell.CreateShortCut(alt_shortcut_path)
    alt_shortcut.Targetpath = cmd_path
    alt_shortcut.WorkingDirectory = script_dir
    alt_shortcut.IconLocation = icon_path
    alt_shortcut.Description = "Real-Time Speech Transcription using Whisper (Alternative)"
    
    # Tentar definir o AppUserModelID também para o atalho alternativo
    try:
        alt_shortcut.SetProperty('{9F4C2855-9F79-4B39-A8D0-E1D42DE1D5F3}', 5, 'whisper.realtime.transcriber.1.0')
    except:
        pass
        
    alt_shortcut.save()
    print(f"Created alternative shortcut at: {alt_shortcut_path}")
    
    # Criar outro atalho para colocar na barra de tarefas
    # No Windows, os atalhos para a barra de tarefas são normalmente armazenados em:
    # %APPDATA%\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar
    try:
        # Encontrar o caminho da barra de tarefas
        appdata = os.environ.get('APPDATA')
        taskbar_path = os.path.join(appdata, "Microsoft", "Internet Explorer", "Quick Launch", "User Pinned", "TaskBar")
        
        # Se o diretório não existir, crie-o
        if not os.path.exists(taskbar_path):
            os.makedirs(taskbar_path)
        
        # Criar o atalho na barra de tarefas
        taskbar_shortcut_path = os.path.join(taskbar_path, "Real-Time Transcriber.lnk")
        taskbar_shortcut = shell.CreateShortCut(taskbar_shortcut_path)
        taskbar_shortcut.Targetpath = bat_path
        taskbar_shortcut.WorkingDirectory = script_dir
        taskbar_shortcut.IconLocation = icon_path
        taskbar_shortcut.Description = "Real-Time Speech Transcription using Whisper"
        
        # Adicionar AppUserModelID também ao atalho da barra de tarefas
        try:
            taskbar_shortcut.SetProperty('{9F4C2855-9F79-4B39-A8D0-E1D42DE1D5F3}', 5, 'whisper.realtime.transcriber.1.0')
        except:
            pass
            
        taskbar_shortcut.save()
        
        print(f"Created a shortcut that can be pinned to the taskbar: {taskbar_shortcut_path}")
    except Exception as e:
        print(f"Warning: Could not create taskbar shortcut: {e}")
    
    # Exibir mensagem para o usuário sobre como fixar na barra de tarefas
    print("\nPara fixar na barra de tarefas:")
    print("1. Execute o atalho da área de trabalho uma vez")
    print("2. Clique com o botão direito no ícone da barra de tarefas")
    print("3. Selecione 'Fixar na barra de tarefas'\n")
    
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