@echo off
echo ====================================================
echo Building Single-File Standalone Executable (.exe)...
echo ====================================================

taskkill /f /im TexasHoldemAI.exe 2>nul
timeout /t 1 /nobreak >nul

.\venv\Scripts\python.exe -c "import shutil; shutil.rmtree('build', ignore_errors=True); shutil.rmtree('dist', ignore_errors=True)" 2>nul

.\venv\Scripts\pyinstaller.exe --noconfirm --onefile --windowed --name "TexasHoldemAI" --collect-submodules "treys" --collect-submodules "pygame" main.py

if %ERRORLEVEL% EQU 0 (
    echo ====================================================
    echo SUCCESS! Single-File Executable built in: dist\TexasHoldemAI.exe
    echo You can send just this single TexasHoldemAI.exe file to your friend!
    echo ====================================================
) else (
    echo ====================================================
    echo BUILD ERROR: Please close TexasHoldemAI.exe if it is currently open and try again.
    echo ====================================================
)
pause
