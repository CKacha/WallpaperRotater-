import tkinter as tk
from tkinter import ttk
from .color_theme import generate_palette, apply_theme, reset_theme

class SettingsTab(ttk.Frame):
    def __init__(self, parent, root: tk.Tk, **kwargs):
        super().__init__(parent, **kwargs)
        self._root = root
        self._palette = None
        self._build()

    def _build(self):
        color_frame = ttk.LabelFrame(self, text="UI Color Theme", padding=12)
        color_frame.pack(fill='x', padx=12, pady=(12, 5))

        self._enabled_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            color_frame,
            text="Enable random color theme",
            variable=self._enabled_var,
            command=self._on_toggle,
        ).pack(anchor='w', pady=(0, 8))

        self._preview = tk.Canvas(color_frame, height=20, bd=0, highlightthickness=0)
        self._preview.pack(fill='x', pady=(0, 10))
        self._preview.bind('<Configure>', lambda _: self._draw_preview())

        btn_row = ttk.Frame(color_frame)
        btn_row.pack(fill='x')
        ttk.Button(btn_row, text="Randomize Now",   command=self._randomize).pack(side='left', padx=(0, 8))
        ttk.Button(btn_row, text="Reset to Default", command=self._reset).pack(side='left')

    def _on_toggle(self):
        if self._enabled_var.get():
            self._randomize()
        else:
            self._reset()

    def _randomize(self):
        self._palette = generate_palette()
        apply_theme(self._root, self._palette)
        self._preview.configure(bg=self._palette['field_bg'])
        self._draw_preview()

    def _reset(self):
        self._palette = None
        reset_theme(self._root)
        self._preview.configure(bg='')
        self._draw_preview()

    def _draw_preview(self):
        self._preview.delete('all')
        w = self._preview.winfo_width()
        h = self._preview.winfo_height()
        if w <= 1:
            return

        if self._palette is None:
            self._preview.create_rectangle(0, 0, w, h, fill='#cccccc', outline='')
            self._preview.create_text(w // 2, h // 2, text='default theme', fill='#666666', font=('Segoe UI', 8))
        else:
            colors = [
                self._palette['bg'],
                self._palette['field_bg'],
                self._palette['btn_bg'],
                self._palette['accent'],
                self._palette['fg'],
            ]
            sw = w / len(colors)
            for i, c in enumerate(colors):
                self._preview.create_rectangle(i * sw, 0, (i + 1) * sw, h, fill=c, outline='')
