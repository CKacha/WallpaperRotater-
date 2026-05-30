@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Building executable...
pyinstaller ^
    --onefile ^
    --windowed ^
    --name WallpaperRotator ^
    --hidden-import=pystray._win32 ^
    --hidden-import=PIL._tkinter_finder ^
    main.py

echo.
echo Done! Your exe is in the dist\ folder.
pause
