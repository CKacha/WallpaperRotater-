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

# letting random hues be picked was a bad idea, too many of them suck sob 
# COLOR WHEEL I TRUST YOU 
_GOOD_HUES = [
    0.60,  # blue
    0.67,  # indigo
    0.75,  # purple
    0.83,  # violet
    0.93,  # rose
    0.00,  # red
    0.08,  # orange
    0.45,  # mint
    0.50,  # teal
    0.54,  # cyan
]

def generate_palette(hue=None) -> dict:
    if hue is None:
        base = random.choice(_GOOD_HUES)
        hue = (base + random.uniform(-0.02, 0.02)) % 1.0

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

def _luminance(color: str) -> float:
    color = color.lstrip('#')
    r, g, b = (int(color[i:i+2], 16) / 255 for i in (0, 2, 4))
    def lin(c): return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def _contrast(c1: str, c2: str) -> float:
    l1, l2 = _luminance(c1), _luminance(c2)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def _ensure_contrast(color: str, against: str, target: float = 4.5) -> str:
    """Brighten color until it meets the target contrast ratio against the bg."""
    h, s, v = colorsys.rgb_to_hsv(*(_luminance_decode(color)))
    for _ in range(20):
        if _contrast(color, against) >= target:
            break
        v = min(1.0, v + 0.04)
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        color = _hex(r, g, b)
    return color


def palette_from_color(hex_color: str) -> dict:
    r, g, b = _luminance_decode(hex_color)
    h, _, _ = colorsys.rgb_to_hsv(r, g, b)
    return generate_palette(hue=h)


def _luminance_decode(color: str):
    color = color.lstrip('#')
    return tuple(int(color[i:i+2], 16) / 255 for i in (0, 2, 4))
