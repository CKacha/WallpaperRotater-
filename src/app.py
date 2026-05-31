import threading
import tkinter as tk
from tkinter import messagebox, ttk

try:
    import pystray
    from PIL import Image, ImageDraw
    HAS_TRAY = True
except ImportError:
    HAS_TRAY = False

from .rotator import WallpaperRotator
from .color_theme import save_original
from .main_tab import MainTab
from .settings_tab import SettingsTab

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Wallpaper Rotator")
        self.root.resizable(False, False)
        save_original(self.root)
        self.rotator = WallpaperRotator()
        self.tray_icon = None
        self._build_ui()
        self._center()
        if HAS_TRAY:
            self._start_tray()

    def _build_ui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=8, pady=8)

        self.settings_tab = SettingsTab(notebook, self.root)
        self.main_tab = MainTab(notebook, self.rotator, on_start=self._handle_start,
                                sound_getter=lambda: self.settings_tab.sound_file)

        notebook.add(self.main_tab,     text="  Rotator  ")
        notebook.add(self.settings_tab, text="  Settings  ")

    def _center(self):
        self.root.update_idletasks()
        w, h = self.root.winfo_width(), self.root.winfo_height()
        x = (self.root.winfo_screenwidth()  - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f'{w}x{h}+{x}+{y}')

    def _handle_start(self, count: int):
        if HAS_TRAY:
            messagebox.showinfo(
                "Running",
                f"Rotating {count} image(s).\n\nThe app will keep running in your system tray.",
            )
            self.root.withdraw()
        else:
            messagebox.showinfo("Running", f"Rotating {count} image(s).\nClose this window to stop.")

    def _make_tray_image(self):
        img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.rectangle([2,  2,  62, 62], fill=(30, 120, 220), outline=(255, 255, 255), width=3)
        d.rectangle([6,  6,  58, 36], fill=(180, 215, 255))
        d.ellipse(  [18, 40, 46, 58], fill=(255, 255, 255))
        return img

    def _start_tray(self):
        menu = pystray.Menu(
            pystray.MenuItem("Wallpaper Rotator", None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Open", self._show_window, default=True),
            pystray.MenuItem(
                "Stop Rotating",
                self._stop_rotating,
                enabled=lambda item: self.rotator.running,
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", self._quit),
        )
        self.tray_icon = pystray.Icon(
            "WallpaperRotator", self._make_tray_image(), "Wallpaper Rotator", menu
        )
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def _show_window(self, icon=None, item=None):
        self.root.after(0, self.root.deiconify)

    def _stop_rotating(self, icon=None, item=None):
        self.rotator.stop()

    def _on_close(self):
        if HAS_TRAY:
            self.root.withdraw()
        else:
            self._quit()

    def _quit(self, icon=None, item=None):
        self.rotator.stop()
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.after(0, self.root.destroy)

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.mainloop()
