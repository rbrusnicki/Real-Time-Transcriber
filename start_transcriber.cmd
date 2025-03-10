@echo off
setlocal enabledelayedexpansion

:: Obtém o diretório atual
set "SCRIPT_DIR=%~dp0"

:: Encontra o pythonw.exe no PATH
for %%i in (pythonw.exe) do set "PYTHONW_PATH=%%~$PATH:i"

:: Use o caminho completo para o pythonw.exe e o script
if defined PYTHONW_PATH (
    start "" "!PYTHONW_PATH!" "!SCRIPT_DIR!gui_transcriber.py"
) else (
    :: Tenta caminhos comuns do Python
    if exist "C:\Python310\pythonw.exe" (
        start "" "C:\Python310\pythonw.exe" "!SCRIPT_DIR!gui_transcriber.py"
    ) else if exist "C:\Python39\pythonw.exe" (
        start "" "C:\Python39\pythonw.exe" "!SCRIPT_DIR!gui_transcriber.py"
    ) else if exist "%LOCALAPPDATA%\Programs\Python\Python310\pythonw.exe" (
        start "" "%LOCALAPPDATA%\Programs\Python\Python310\pythonw.exe" "!SCRIPT_DIR!gui_transcriber.py"
    ) else (
        :: Tenta última alternativa usando python normal
        start "" python "!SCRIPT_DIR!gui_transcriber.py"
    )
)

endlocal 