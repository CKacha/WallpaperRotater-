## WallpaperRotater
Rotate yo wallpapers on Windows!

> Currently only works for Windows. Linux/Mac support is not planned but maybe someday idk.

Exactly what it sounds like: I have lots of different cool pieces of art, and I want to rotate between them for my wallpapers :p


## Using the project

Download the `.exe` from releases & run it!


## Running from root
**Requirements:** Python 3.9+

Install dependencies:
(Running from within the downloaded folder)

```
pip install -r requirements.txt
python main.py
```

## Building the executable
(Running from within the downloaded folder)

```
build.bat
```

This installs dependencies and builds a standalone `WallpaperRotator.exe` into the `dist\` folder!

## What can ya do
- Sequential/random rotation order
- Fixed/randomized interval between wallpaper changes
- Runs as a background process - you can close the tab after activating it!
- Make the system beep or use a custom `.wav` file each time the wallpaper switches
- Randomize the color scheme/pick a specific color

## Supported file formats atm:
`.jpg` `.jpeg` `.png` `.bmp` `.gif` `.tiff` `.tif` `.dib`
