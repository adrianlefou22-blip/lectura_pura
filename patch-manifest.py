#!/usr/bin/env python3
"""
patch-manifest.py
Agrega permisos nativos de Android al AndroidManifest.xml
generado por Capacitor. Se ejecuta en GitHub Actions antes del build.

Permisos que agrega:
- WAKE_LOCK: evita que la CPU se duerma mientras reproduce
- FOREGROUND_SERVICE: permite correr servicio en primer plano
- FOREGROUND_SERVICE_MEDIA_PLAYBACK: tipo específico para audio
- REQUEST_IGNORE_BATTERY_OPTIMIZATIONS: evita que batería mate la app
"""

import re
import sys

MANIFEST_PATH = "android/app/src/main/AndroidManifest.xml"

PERMISOS = [
    '<uses-permission android:name="android.permission.WAKE_LOCK" />',
    '<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />',
    '<uses-permission android:name="android.permission.FOREGROUND_SERVICE_MEDIA_PLAYBACK" />',
    '<uses-permission android:name="android.permission.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS" />',
]

SERVICIO = '''
    <service
        android:name=".AudioForegroundService"
        android:foregroundServiceType="mediaPlayback"
        android:exported="false" />'''

try:
    with open(MANIFEST_PATH, 'r') as f:
        content = f.read()

    # Agregar permisos antes de <application
    for permiso in PERMISOS:
        if permiso not in content:
            content = content.replace(
                '<application',
                permiso + '\n    <application',
                1
            )
            print(f"✅ Agregado: {permiso[:60]}...")

    # Agregar servicio antes del cierre </application>
    if 'AudioForegroundService' not in content:
        content = content.replace(
            '</application>',
            SERVICIO + '\n</application>'
        )
        print("✅ Agregado: AudioForegroundService")

    # Agregar android:usesCleartextTraffic en application tag
    if 'usesCleartextTraffic' not in content:
        content = content.replace(
            'android:hardwareAccelerated="true"',
            'android:hardwareAccelerated="true"\n        android:usesCleartextTraffic="true"'
        )
        print("✅ Agregado: usesCleartextTraffic")

    with open(MANIFEST_PATH, 'w') as f:
        f.write(content)

    print("\n✅ AndroidManifest.xml parcheado correctamente")
    print("   ForegroundService + WAKE_LOCK activos")

except FileNotFoundError:
    print(f"❌ No se encontró: {MANIFEST_PATH}")
    print("   Asegurate de correr 'npx cap add android' primero")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
