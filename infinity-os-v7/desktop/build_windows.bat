@echo off
setlocal
py -3 -m pip install --upgrade pyinstaller
py -3 -m PyInstaller --noconfirm --clean --windowed --name "Infinity OS V7" main.py
if errorlevel 1 exit /b 1
echo Build complete: dist\Infinity OS V7\Infinity OS V7.exe
