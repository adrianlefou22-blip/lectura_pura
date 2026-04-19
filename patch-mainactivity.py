#!/usr/bin/env python3
"""
patch-mainactivity.py
Inyecta AndroidTTS en el WebView de Capacitor.
Se corre DESPUÉS de 'npx cap add android'.
"""
import os, sys, shutil

# 1) Copiar AndroidTTS.java al paquete correcto
SRC_JAVA = "AndroidTTS.java"
DST_JAVA = "android/app/src/main/java/com/lecturapura/app/AndroidTTS.java"

os.makedirs(os.path.dirname(DST_JAVA), exist_ok=True)
shutil.copy(SRC_JAVA, DST_JAVA)
print("✅ AndroidTTS.java copiado")

# 2) Parchear MainActivity.java
MAIN = "android/app/src/main/java/com/lecturapura/app/MainActivity.java"

with open(MAIN, 'r') as f:
    content = f.read()

# Agregar import si no está
if 'import android.webkit.WebView' not in content:
    content = content.replace(
        'import com.getcapacitor.BridgeActivity;',
        'import com.getcapacitor.BridgeActivity;\nimport android.webkit.WebView;\nimport android.os.Bundle;'
    )

# Reemplazar clase vacía con la versión que inyecta AndroidTTS
if 'AndroidTTS' not in content:
    old = 'public class MainActivity extends BridgeActivity {}'
    new = '''public class MainActivity extends BridgeActivity {
    private AndroidTTS androidTTS;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Inyectar TTS nativo en el WebView de Capacitor
        WebView webView = getBridge().getWebView();
        androidTTS = new AndroidTTS(this, webView);
        webView.addJavascriptInterface(androidTTS, "AndroidTTS");
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (androidTTS != null) androidTTS.shutdown();
    }
}'''
    if old in content:
        content = content.replace(old, new)
        print("✅ MainActivity.java parcheado (clase vacía)")
    else:
        # Puede que tenga llaves con contenido, buscar de otra forma
        import re
        content = re.sub(
            r'public class MainActivity extends BridgeActivity \{[^}]*\}',
            new,
            content
        )
        print("✅ MainActivity.java parcheado (regex)")
else:
    print("ℹ️  MainActivity.java ya tiene AndroidTTS")

with open(MAIN, 'w') as f:
    f.write(content)

print("\n✅ Listo — AndroidTTS inyectado en WebView")
