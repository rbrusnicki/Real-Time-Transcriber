@echo off
setlocal enabledelayedexpansion

:: Obtém o diretório atual
set "SCRIPT_DIR=%~dp0"

:: Usa o ícone personalizado
start "" /HIGH "%SCRIPT_DIR%gui_transcriber.py" "microphone.ico"

endlocal 