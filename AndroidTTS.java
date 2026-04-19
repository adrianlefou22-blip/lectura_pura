package com.lecturapura.app;

import android.content.Context;
import android.speech.tts.TextToSpeech;
import android.speech.tts.UtteranceProgressListener;
import android.speech.tts.Voice;
import android.webkit.JavascriptInterface;
import android.webkit.WebView;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Set;

public class AndroidTTS {

    private TextToSpeech tts;
    private WebView webView;
    private boolean ready = false;

    public AndroidTTS(Context context, WebView webView) {
        this.webView = webView;
        tts = new TextToSpeech(context, status -> {
            if (status == TextToSpeech.SUCCESS) {
                ready = true;
                tts.setOnUtteranceProgressListener(new UtteranceProgressListener() {
                    @Override public void onStart(String id) {}
                    @Override
                    public void onDone(String id) {
                        webView.post(() -> webView.evaluateJavascript(
                            "if(window.__ttsOnEnd)window.__ttsOnEnd();", null));
                    }
                    @Override
                    public void onError(String id) {
                        webView.post(() -> webView.evaluateJavascript(
                            "if(window.__ttsOnError)window.__ttsOnError('error');", null));
                    }
                });
            }
        });
    }

    // Devuelve JSON con todas las voces disponibles en el sistema
    @JavascriptInterface
    public String getVoices() {
        if (!ready) return "[]";
        try {
            Set<Voice> voices = tts.getVoices();
            if (voices == null) return "[]";
            List<String> items = new ArrayList<>();
            for (Voice v : voices) {
                String lang = v.getLocale().toLanguageTag();
                String name = v.getName();
                boolean local = !v.isNetworkConnectionRequired();
                // Solo incluir voces en español
                if (lang.startsWith("es")) {
                    items.add("{\"name\":\"" + name + "\",\"lang\":\"" + lang + "\",\"local\":" + local + "}");
                }
            }
            return "[" + String.join(",", items) + "]";
        } catch (Exception e) {
            return "[]";
        }
    }

    @JavascriptInterface
    public void speak(String text, String lang, String rate, String pitch, String voiceName) {
        if (!ready || text == null || text.trim().isEmpty()) return;
        try {
            // Intentar setear la voz específica si se provee
            if (voiceName != null && !voiceName.isEmpty()) {
                Set<Voice> voices = tts.getVoices();
                if (voices != null) {
                    for (Voice v : voices) {
                        if (v.getName().equals(voiceName)) {
                            tts.setVoice(v);
                            break;
                        }
                    }
                }
            } else {
                // Fallback por idioma
                String[] parts = lang.replace("-","_").split("_");
                Locale locale = parts.length >= 2 ? new Locale(parts[0], parts[1]) : new Locale(parts[0]);
                tts.setLanguage(locale);
            }
            tts.setSpeechRate(Float.parseFloat(rate));
            tts.setPitch(Float.parseFloat(pitch));
            android.os.Bundle params = new android.os.Bundle();
            params.putString(TextToSpeech.Engine.KEY_PARAM_UTTERANCE_ID, "u1");
            tts.speak(text, TextToSpeech.QUEUE_FLUSH, params, "u1");
        } catch (Exception e) {
            webView.post(() -> webView.evaluateJavascript(
                "if(window.__ttsOnError)window.__ttsOnError('speak-error');", null));
        }
    }

    @JavascriptInterface
    public void stop() {
        if (ready) tts.stop();
    }

    public void shutdown() {
        if (tts != null) { tts.stop(); tts.shutdown(); }
    }
}
