package com.lecturapura.app;

import android.content.Context;
import android.speech.tts.TextToSpeech;
import android.speech.tts.UtteranceProgressListener;
import android.webkit.JavascriptInterface;
import android.webkit.WebView;
import java.util.Locale;

public class AndroidTTS {

    private TextToSpeech tts;
    private WebView webView;
    private boolean ready = false;

    public AndroidTTS(Context context, WebView webView) {
        this.webView = webView;
        tts = new TextToSpeech(context, status -> {
            if (status == TextToSpeech.SUCCESS) {
                tts.setLanguage(new Locale("es", "ES"));
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

    @JavascriptInterface
    public void speak(String text, String lang, String rate, String pitch) {
        if (!ready || text == null || text.trim().isEmpty()) return;
        try {
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
