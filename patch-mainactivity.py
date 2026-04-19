#!/usr/bin/env python3
import os, sys, shutil

SRC = "AndroidTTS.java"
DST = "android/app/src/main/java/com/lecturapura/app/AndroidTTS.java"
os.makedirs(os.path.dirname(DST), exist_ok=True)
shutil.copy(SRC, DST)
print("✅ AndroidTTS.java copiado")

MAIN = "android/app/src/main/java/com/lecturapura/app/MainActivity.java"

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
    public void onDestroy() {
        super.onDestroy();
        if (androidTTS != null) androidTTS.shutdown();
    }
}
'''

with open(MAIN, 'w') as f:
    f.write(nuevo)
print("✅ MainActivity.java reescrito")
