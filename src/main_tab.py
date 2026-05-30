import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from .constants import SUPPORTED_EXTENSIONS
from .rotator import WallpaperRotator

class MainTab(ttk.Frame):
    def __init__(self, parent, rotator: WallpaperRotator, on_start, **kwargs):
        super().__init__(parent, **kwargs)
        self._rotator = rotator
        self._on_start = on_start
        self._build()

    def _build(self):
        folder_frame = ttk.LabelFrame(self, text="Image Folder", padding=10)
        folder_frame.pack(fill='x', padx=12, pady=(12, 5))

        self.folder_var = tk.StringVar()
        ttk.Entry(folder_frame, textvariable=self.folder_var, width=42).pack(side='left', fill='x', expand=True)
        ttk.Button(folder_frame, text="Browse…", command=self._browse).pack(side='left', padx=(6, 0))

        order_frame = ttk.LabelFrame(self, text="Rotation Order", padding=10)
        order_frame.pack(fill='x', padx=12, pady=5)

        self.order_var = tk.StringVar(value='sequential')
        ttk.Radiobutton(order_frame, text="Sequential", variable=self.order_var, value='sequential').pack(side='left', padx=8)
        ttk.Radiobutton(order_frame, text="Random",     variable=self.order_var, value='random').pack(side='left', padx=8)

        interval_frame = ttk.LabelFrame(self, text="Change Interval", padding=10)
        interval_frame.pack(fill='x', padx=12, pady=5)

        self.interval_var = tk.StringVar(value='fixed')

        fixed_row = ttk.Frame(interval_frame)
        fixed_row.pack(fill='x', pady=3)
        ttk.Radiobutton(fixed_row, text="Fixed:", variable=self.interval_var, value='fixed', command=self._toggle).pack(side='left')
        self.fixed_var = tk.StringVar(value='5')
        self.fixed_spin = ttk.Spinbox(fixed_row, from_=1, to=1440, textvariable=self.fixed_var, width=6)
        self.fixed_spin.pack(side='left', padx=6)
        ttk.Label(fixed_row, text="minutes").pack(side='left')

        rand_row = ttk.Frame(interval_frame)
        rand_row.pack(fill='x', pady=3)
        ttk.Radiobutton(rand_row, text="Random:", variable=self.interval_var, value='random', command=self._toggle).pack(side='left')
        self.min_var = tk.StringVar(value='1')
        self.max_var = tk.StringVar(value='10')
        self.min_spin = ttk.Spinbox(rand_row, from_=1, to=1440, textvariable=self.min_var, width=6, state='disabled')
        self.min_spin.pack(side='left', padx=6)
        ttk.Label(rand_row, text="to").pack(side='left')
        self.max_spin = ttk.Spinbox(rand_row, from_=1, to=1440, textvariable=self.max_var, width=6, state='disabled')
        self.max_spin.pack(side='left', padx=6)
        ttk.Label(rand_row, text="minutes").pack(side='left')

        ttk.Button(self, text="Start Rotating", command=self._start).pack(pady=12)

    def _toggle(self):
        fixed = self.interval_var.get() == 'fixed'
        self.fixed_spin.config(state='normal'  if fixed else 'disabled')
        self.min_spin.config( state='disabled' if fixed else 'normal')
        self.max_spin.config( state='disabled' if fixed else 'normal')

    def _browse(self):
        folder = filedialog.askdirectory(title="Select Image Folder")
        if folder:  
            self.folder_var.set(folder)

    def _start(self):
        folder = self.folder_var.get().strip()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please select a valid folder.")
            return

        try:
            if self.interval_var.get() == 'fixed':
                fixed_secs = int(self.fixed_var.get()) * 60
                min_secs = max_secs = fixed_secs
                if fixed_secs <= 0:
                    raise ValueError
            else:
                min_secs = int(self.min_var.get()) * 60
                max_secs = int(self.max_var.get()) * 60
                fixed_secs = min_secs
                if min_secs <= 0 or max_secs <= 0:
                    raise ValueError
                if min_secs >= max_secs:
                    messagebox.showerror("Error", "Random interval: min must be less than max.")
                    return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid interval (positive whole number).")
            return

        count = self._rotator.start(
            folder=folder,
            order=self.order_var.get(),
            interval_type=self.interval_var.get(),
            fixed_secs=fixed_secs,
            min_secs=min_secs,
            max_secs=max_secs,
        )

        if count == 0:
            exts = ', '.join(sorted(SUPPORTED_EXTENSIONS))
            messagebox.showerror("Error", f"No supported images found.\n\nSupported formats: {exts}")
            return

        self._on_start(count)
