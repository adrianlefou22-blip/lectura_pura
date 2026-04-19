#!/usr/bin/env python3
"""
patch-mainactivity.py - Inyecta AndroidTTS en el WebView de Capacitor 6
"""
import os, sys, shutil, re

# 1) Copiar AndroidTTS.java
SRC = "AndroidTTS.java"
DST = "android/app/src/main/java/com/lecturapura/app/AndroidTTS.java"
os.makedirs(os.path.dirname(DST), exist_ok=True)
shutil.copy(SRC, DST)
print("✅ AndroidTTS.java copiado a", DST)

# 2) Leer MainActivity.java
MAIN = "android/app/src/main/java/com/lecturapura/app/MainActivity.java"
with open(MAIN, 'r') as f:
    original = f.read()

print("📄 MainActivity.java original:")
print(original)
print("---")

# Si ya está parcheado, salir
if 'AndroidTTS' in original:
    print("ℹ️  Ya está parcheado")
    sys.exit(0)

# Nuevo contenido completo — reemplazar todo el archivo
nuevo = '''package com.lecturapura.app;

import android.os.Bundle;
import android.webkit.WebView;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    private AndroidTTS androidTTS;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        WebView webView = getBridge().getWebView();
        androidTTS = new AndroidTTS(this, webView);
        webView.addJavascriptInterface(androidTTS, "AndroidTTS");
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (androidTTS != null) androidTTS.shutdown();
    }
}
'''

with open(MAIN, 'w') as f:
    f.write(nuevo)

print("✅ MainActivity.java reescrito con AndroidTTS")

# Verificar
with open(MAIN, 'r') as f:
    result = f.read()
print("📄 Resultado:")
print(result)
