import ctypes
import random
import threading
import winsound
from pathlib import Path
from .constants import SUPPORTED_EXTENSIONS, SPI_SETDESKWALLPAPER, SPIF_UPDATE


def _play_sound(sound_file):
    if sound_file is None:
        return
    try:
        if sound_file == '':
            winsound.MessageBeep(winsound.MB_OK)
        else:
            winsound.PlaySound(sound_file, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT)
    except Exception:
        pass

def set_wallpaper(image_path: str) -> bool:
    abs_path = str(Path(image_path).resolve())
    return bool(ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, abs_path, SPIF_UPDATE
    ))

def get_images(folder: str) -> list:
    folder_path = Path(folder)
    images = []
    for f in folder_path.iterdir():
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS:
            images.append(str(f))
    return sorted(images)

class WallpaperRotator:
    def __init__(self):
        self.running = False
        self._stop_event = threading.Event()
        self._thread = None

    def start(self, folder, order, interval_type, fixed_secs, min_secs, max_secs, sound_file=None):
        if self.running:
            self.stop()
        images = get_images(folder)
        if not images:
            return 0

        self.running = True
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._loop,
            args=(images, order, interval_type, fixed_secs, min_secs, max_secs, sound_file),
            daemon=True,
        )
        self._thread.start()
        return len(images)

    def stop(self):
        self.running = False
        self._stop_event.set()

    def _loop(self, images, order, interval_type, fixed_secs, min_secs, max_secs, sound_file):
        if order == 'random':
            random.shuffle(images)

        idx = 0
        while not self._stop_event.is_set():
            if idx >= len(images):
                if order == 'random':
                    random.shuffle(images)
                idx = 0

            set_wallpaper(images[idx])
            _play_sound(sound_file)
            idx += 1

            wait = fixed_secs if interval_type == 'fixed' else random.uniform(min_secs, max_secs)
            self._stop_event.wait(wait)
