#!/usr/bin/env python3
"""
patch-icon.py
Copia el icono a todas las carpetas mipmap de Android
en los tamaños correctos usando PIL.
"""
import os, sys, shutil

try:
    from PIL import Image
except ImportError:
    os.system("pip install Pillow --break-system-packages -q")
    from PIL import Image

SRC = "resources/icon.png"
BASE = "android/app/src/main/res"

# Tamaños oficiales de Android por carpeta mipmap
SIZES = {
    "mipmap-mdpi":    48,
    "mipmap-hdpi":    72,
    "mipmap-xhdpi":   96,
    "mipmap-xxhdpi":  144,
    "mipmap-xxxhdpi": 192,
}

img = Image.open(SRC).convert("RGBA")

for folder, size in SIZES.items():
    dst_dir = os.path.join(BASE, folder)
    os.makedirs(dst_dir, exist_ok=True)
    resized = img.resize((size, size), Image.LANCZOS)
    dst = os.path.join(dst_dir, "ic_launcher.png")
    resized.save(dst, "PNG")
    # También ic_launcher_round
    dst_r = os.path.join(dst_dir, "ic_launcher_round.png")
    resized.save(dst_r, "PNG")
    print(f"✅ {folder}: {size}x{size}")

print("\n✅ Iconos copiados a todas las carpetas mipmap")
