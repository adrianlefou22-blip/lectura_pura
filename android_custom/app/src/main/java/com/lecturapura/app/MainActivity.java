package com.lecturapura.app;

import android.os.Bundle;
import android.speech.tts.TextToSpeech;
import android.webkit.JavascriptInterface;
import android.webkit.WebView;
import com.getcapacitor.BridgeActivity;
import java.util.HashMap;
import java.util.Locale;

public class MainActivity extends BridgeActivity {

    private TextToSpeech tts;
    private boolean ttsReady = false;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        tts = new TextToSpeech(this, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if (status == TextToSpeech.SUCCESS) {
                    tts.setLanguage(new Locale("es", "ES"));
                    ttsReady = true;
                    // Notificar al JS que TTS está listo
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            getBridge().getWebView().evaluateJavascript(
                                "if(window.onNativeTTSReady) window.onNativeTTSReady();",
                                null
                            );
                        }
                    });
                }
            }
        });

        getBridge().getWebView().addJavascriptInterface(new TTSBridge(), "AndroidTTS");
    }

    @Override
    public void onDestroy() {
        if (tts != null) {
            tts.stop();
            tts.shutdown();
        }
        super.onDestroy();
    }

    private class TTSBridge {

        @JavascriptInterface
        public void speak(String text, float rate, float pitch) {
            if (!ttsReady || tts == null) return;
            tts.setSpeechRate(rate);
            tts.setPitch(pitch);
            tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, "lp_utt");
        }

        @JavascriptInterface
        public void stop() {
            if (tts != null) tts.stop();
        }

        @JavascriptInterface
        public boolean isReady() {
            return ttsReady;
        }

        @JavascriptInterface
        public void setLanguage(String lang) {
            if (!ttsReady || tts == null) return;
            try {
                String[] parts = lang.split("[-_]");
                Locale locale = parts.length >= 2
                    ? new Locale(parts[0], parts[1])
                    : new Locale(parts[0]);
                int result = tts.setLanguage(locale);
                if (result == TextToSpeech.LANG_MISSING_DATA ||
                    result == TextToSpeech.LANG_NOT_SUPPORTED) {
                    tts.setLanguage(new Locale("es", "ES"));
                }
            } catch (Exception e) {
                tts.setLanguage(new Locale("es", "ES"));
            }
        }

        @JavascriptInterface
        public void notifyEnd() {
            // callback desde TTS nativo al JS
        }
    }
}
