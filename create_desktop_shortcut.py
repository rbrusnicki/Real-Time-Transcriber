import os
import sys
import winshell
from win32com.client import Dispatch
import ctypes
import subprocess

def get_python_executable():
    """Tenta encontrar o caminho para o executável pythonw.exe"""
    # Tente obter o caminho do sys.executable
    python_path = sys.executable
    
    # Se terminar com python.exe, tente encontrar pythonw.exe
    if python_path.endswith("python.exe"):
        pythonw_path = python_path.replace("python.exe", "pythonw.exe")
        if os.path.exists(pythonw_path):
            return pythonw_path
    
    # Tente encontrar o pythonw.exe usando o PATH
    try:
        pythonw_path = subprocess.check_output("where pythonw", shell=True).decode().strip().split("\r\n")[0]
        if os.path.exists(pythonw_path):
            return pythonw_path
    except:
        pass
    
    # Tente caminhos comuns
    common_paths = [
        "C:\\Python310\\pythonw.exe",
        "C:\\Python39\\pythonw.exe",
        os.path.join(os.environ.get('LOCALAPPDATA', ''), "Programs", "Python", "Python310", "pythonw.exe"),
        os.path.join(os.environ.get('LOCALAPPDATA', ''), "Programs", "Python", "Python39", "pythonw.exe")
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    return None

def create_desktop_shortcut():
    """Create a desktop shortcut for the transcription application"""
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bat_path = os.path.join(script_dir, "start_transcriber.bat")
    cmd_path = os.path.join(script_dir, "start_transcriber.cmd")
    alt_bat_path = os.path.join(script_dir, "start_alt.bat")
    icon_path = os.path.join(script_dir, "microphone.ico")
    script_path = os.path.join(script_dir, "gui_transcriber.py")
    
    # Get pythonw path
    pythonw_path = get_python_executable()
    
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
    
    # Criar atalho alternativo usando o arquivo .bat alternativo
    alt_shortcut_path = os.path.join(desktop, "Real-Time Transcriber (Alt 1).lnk")
    alt_shortcut = shell.CreateShortCut(alt_shortcut_path)
    alt_shortcut.Targetpath = alt_bat_path
    alt_shortcut.WorkingDirectory = script_dir
    alt_shortcut.IconLocation = icon_path
    alt_shortcut.Description = "Real-Time Speech Transcription using Whisper (Alternative 1)"
    
    # Tentar definir o AppUserModelID também para o atalho alternativo
    try:
        alt_shortcut.SetProperty('{9F4C2855-9F79-4B39-A8D0-E1D42DE1D5F3}', 5, 'whisper.realtime.transcriber.1.0')
    except:
        pass
        
    alt_shortcut.save()
    print(f"Created alternative shortcut 1 at: {alt_shortcut_path}")
    
    # Criar atalho alternativo usando o arquivo .cmd
    alt_shortcut_path2 = os.path.join(desktop, "Real-Time Transcriber (Alt 2).lnk")
    alt_shortcut2 = shell.CreateShortCut(alt_shortcut_path2)
    alt_shortcut2.Targetpath = cmd_path
    alt_shortcut2.WorkingDirectory = script_dir
    alt_shortcut2.IconLocation = icon_path
    alt_shortcut2.Description = "Real-Time Speech Transcription using Whisper (Alternative 2)"
    
    # Tentar definir o AppUserModelID também para o atalho alternativo
    try:
        alt_shortcut2.SetProperty('{9F4C2855-9F79-4B39-A8D0-E1D42DE1D5F3}', 5, 'whisper.realtime.transcriber.1.0')
    except:
        pass
        
    alt_shortcut2.save()
    print(f"Created alternative shortcut 2 at: {alt_shortcut_path2}")
    
    # Se encontramos o pythonw.exe, criar atalho direto para o script Python
    if pythonw_path:
        direct_shortcut_path = os.path.join(desktop, "Real-Time Transcriber (Direct).lnk")
        direct_shortcut = shell.CreateShortCut(direct_shortcut_path)
        direct_shortcut.Targetpath = pythonw_path
        direct_shortcut.Arguments = f'"{script_path}"'
        direct_shortcut.WorkingDirectory = script_dir
        direct_shortcut.IconLocation = icon_path
        direct_shortcut.Description = "Real-Time Speech Transcription using Whisper (Direct Python)"
        
        # Tentar definir o AppUserModelID
        try:
            direct_shortcut.SetProperty('{9F4C2855-9F79-4B39-A8D0-E1D42DE1D5F3}', 5, 'whisper.realtime.transcriber.1.0')
        except:
            pass
            
        direct_shortcut.save()
        print(f"Created direct pythonw shortcut at: {direct_shortcut_path}")
    
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
        
        # Se temos o pythonw.exe, use-o diretamente para melhor compatibilidade
        if pythonw_path:
            taskbar_shortcut.Targetpath = pythonw_path
            taskbar_shortcut.Arguments = f'"{script_path}"'
        else:
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
    
    print("\nSe um atalho não funcionar, tente outro dos atalhos alternativos criados.")
    
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