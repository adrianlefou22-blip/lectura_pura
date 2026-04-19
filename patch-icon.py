#!/usr/bin/env python3
"""
patch-icon.py — Copia icono a todas las carpetas mipmap de Android
Método manual directo, sin dependencias externas a Pillow.
"""
import os, shutil, subprocess, sys

# Instalar Pillow si no está
try:
    from PIL import Image
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Pillow', '--break-system-packages', '-q'])
    from PIL import Image

SRC = "resources/icon.png"
BASE = "android/app/src/main/res"

SIZES = {
    "mipmap-mdpi":    48,
    "mipmap-hdpi":    72,
    "mipmap-xhdpi":   96,
    "mipmap-xxhdpi":  144,
    "mipmap-xxxhdpi": 192,
}

img = Image.open(SRC).convert("RGBA")
print(f"Icono fuente: {img.size[0]}x{img.size[1]}")

for folder, size in SIZES.items():
    dst_dir = os.path.join(BASE, folder)
    os.makedirs(dst_dir, exist_ok=True)
    resized = img.resize((size, size), Image.LANCZOS)
    resized.save(os.path.join(dst_dir, "ic_launcher.png"), "PNG")
    resized.save(os.path.join(dst_dir, "ic_launcher_round.png"), "PNG")
    resized.save(os.path.join(dst_dir, "ic_launcher_foreground.png"), "PNG")
    print(f"  ✅ {folder}: {size}x{size}")

# También copiar al directorio drawable por si acaso
drawable = os.path.join(BASE, "drawable")
os.makedirs(drawable, exist_ok=True)
img.resize((512, 512), Image.LANCZOS).save(os.path.join(drawable, "ic_launcher.png"), "PNG")

print("\n✅ Iconos aplicados correctamente")
