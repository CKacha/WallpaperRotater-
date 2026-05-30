import colorsys
import random
import tkinter as tk
from tkinter import ttk

_original_theme = None
_original_bg = None

def save_original(root: tk.Tk):
    global _original_theme, _original_bg
    _original_theme = ttk.Style(root).theme_use()
    _original_bg = root.cget('bg')

def generate_palette() -> dict:
    hue = random.random()

    r, g, b = colorsys.hsv_to_rgb(hue, 0.15, 0.18)
    bg = _hex(r, g, b)

    r, g, b = colorsys.hsv_to_rgb(hue, 0.12, 0.26)
    field_bg = _hex(r, g, b)

    r, g, b = colorsys.hsv_to_rgb(hue, 0.80, 0.92)
    accent = _hex(r, g, b)

    r, g, b = colorsys.hsv_to_rgb(hue, 0.50, 0.38)
    btn_bg = _hex(r, g, b)

    return {'bg': bg, 'fg': '#e8e8f0', 'field_bg': field_bg, 'accent': accent, 'btn_bg': btn_bg}

def apply_theme(root: tk.Tk, palette: dict):
    bg = palette['bg']
    fg = palette['fg']
    field_bg = palette['field_bg']
    accent = palette['accent']
    btn_bg = palette['btn_bg']

    root.configure(bg=bg)
    s = ttk.Style(root)
    s.theme_use('clam')

    s.configure('.',
                background=bg, foreground=fg, fieldbackground=field_bg,
                troughcolor=bg, bordercolor=field_bg, darkcolor=bg, lightcolor=field_bg,
    )
    s.configure('TFrame', background=bg)
    s.configure('TLabel', background=bg, foreground=fg)
    s.configure('TButton', background=btn_bg, foreground=fg, borderwidth=0, padding=6)
    s.map('TButton',
          background=[('active', accent), ('pressed', accent)],
          foreground=[('active',  bg)],
    )
    s.configure('TLabelframe', background=bg, bordercolor=accent)
    s.configure('TLabelframe.Label', background=bg, foreground=accent, font=('Segoe UI', 9, 'bold'))
    s.configure('TEntry', fieldbackground=field_bg, foreground=fg)
    s.configure('TSpinbox', fieldbackground=field_bg, foreground=fg, arrowcolor=fg)
    s.configure('TRadiobutton', background=bg, foreground=fg, focuscolor=bg)
    s.configure('TCheckbutton', background=bg, foreground=fg, focuscolor=bg)
    s.configure('TNotebook', background=bg, bordercolor=field_bg)
    s.configure('TNotebook.Tab', background=field_bg, foreground=fg, padding=[10, 4])
    s.map('TNotebook.Tab',
          background=[('selected', bg)],
          foreground=[('selected', accent)],
    )

def reset_theme(root: tk.Tk):
    s = ttk.Style(root)
    theme = _original_theme or 'default'
    try:
        s.theme_use(theme)
    except tk.TclError:
        s.theme_use('default')
    if _original_bg:
        root.configure(bg=_original_bg)

def _hex(r, g, b) -> str:
    return '#{:02x}{:02x}{:02x}'.format(int(r * 255), int(g * 255), int(b * 255))
