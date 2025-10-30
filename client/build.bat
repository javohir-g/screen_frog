@echo off
cd /d %~dp0
echo Building client.exe...
pyinstaller --onefile --noconsole --clean --name "ScreenAI-Client" main.py
echo.
echo Build complete! Executable: dist\ScreenAI-Client.exe
echo.
echo Before distributing:
echo 1. Update client\config.json with server IP address
echo 2. Copy config.json to the same folder as .exe
echo.
pause