package com.lecturapura.app;

import android.content.Context;
import android.speech.tts.TextToSpeech;
import android.speech.tts.UtteranceProgressListener;
import android.webkit.JavascriptInterface;
import android.webkit.WebView;
import java.util.HashMap;
import java.util.Locale;

public class AndroidTTS {

    private TextToSpeech tts;
    private WebView webView;
    private Context context;
    private boolean ready = false;

    public AndroidTTS(Context context, WebView webView) {
        this.context = context;
        this.webView = webView;

        tts = new TextToSpeech(context, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if (status == TextToSpeech.SUCCESS) {
                    tts.setLanguage(new Locale("es", "ES"));
                    ready = true;
                    tts.setOnUtteranceProgressListener(new UtteranceProgressListener() {
                        @Override public void onStart(String id) {}
                        @Override
                        public void onDone(String id) {
                            webView.post(new Runnable() {
                                public void run() {
                                    webView.evaluateJavascript(
                                        "if(window.__ttsOnEnd) window.__ttsOnEnd();", null);
                                }
                            });
                        }
                        @Override
                        public void onError(String id) {
                            webView.post(new Runnable() {
                                public void run() {
                                    webView.evaluateJavascript(
                                        "if(window.__ttsOnError) window.__ttsOnError('tts-error');", null);
                                }
                            });
                        }
                    });
                }
            }
        });
    }

    @JavascriptInterface
    public void speak(String text, String lang, String rate, String pitch) {
        if (!ready) return;
        try {
            float r = Float.parseFloat(rate);
            float p = Float.parseFloat(pitch);
            // Intentar setear el idioma pedido
            Locale locale = new Locale(lang.replace("-","_").split("_")[0],
                                       lang.contains("-") ? lang.split("-")[1] : "ES");
            int res = tts.isLanguageAvailable(locale);
            if (res >= TextToSpeech.LANG_AVAILABLE) {
                tts.setLanguage(locale);
            }
            tts.setSpeechRate(r);
            tts.setPitch(p);
            HashMap<String, String> params = new HashMap<>();
            params.put(TextToSpeech.Engine.KEY_PARAM_UTTERANCE_ID, "tts1");
            tts.speak(text, TextToSpeech.QUEUE_FLUSH, params);
        } catch (Exception e) {
            webView.post(new Runnable() {
                public void run() {
                    webView.evaluateJavascript(
                        "if(window.__ttsOnError) window.__ttsOnError('speak-exception');", null);
                }
            });
        }
    }

    @JavascriptInterface
    public void stop() {
        if (ready) {
            tts.stop();
        }
    }

    public void shutdown() {
        if (tts != null) {
            tts.stop();
            tts.shutdown();
        }
    }
}
