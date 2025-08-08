package com.example.app;

import android.util.Log;
import org.json.JSONArray;
import org.json.JSONObject;
import java.io.IOException;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class Gemini {

    private static final String API_KEY = "AIzaSyDxC8ngddv8j0B9yKCEz0tEaCG55hoLCMY";
    private static final String ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent";
    private final OkHttpClient client;

    public interface GeminiCallback {
        void onResponse(String answer);
    }

    public Gemini() {
        client = new OkHttpClient();
    }

    public void getOnlineReply(String prompt, GeminiCallback callback) {
        try {
            // JSON body setup
            JSONObject json = new JSONObject();
            JSONArray contents = new JSONArray();
            JSONObject content = new JSONObject();
            JSONArray parts = new JSONArray();
            JSONObject part = new JSONObject();

            part.put("text", prompt);
            parts.put(part);
            content.put("parts", parts);
            contents.put(content);
            json.put("contents", contents);

            RequestBody body = RequestBody.create(json.toString(), MediaType.parse("application/json"));
            Request request = new Request.Builder()
                    .url(ENDPOINT + "?key=" + API_KEY) // ✅ Correct way to append API key
                    .post(body)
                    .build();

            client.newCall(request).enqueue(new Callback() {
                @Override
                public void onFailure(Call call, IOException e) {
                    callback.onResponse("Failed to connect to Gemini.");
                }

                @Override
                public void onResponse(Call call, Response response) throws IOException {
                    if (!response.isSuccessful()) {
                        callback.onResponse("API Error: " + response.code());
                        return;
                    }

                    String resBody = response.body().string();
                    try {
                        JSONObject resJson = new JSONObject(resBody);
                        JSONArray candidates = resJson.getJSONArray("candidates");
                        JSONObject content = candidates.getJSONObject(0).getJSONObject("content");
                        JSONArray parts = content.getJSONArray("parts");
                        String text = parts.getJSONObject(0).getString("text");
                        callback.onResponse(text.trim());
                    } catch (Exception e) {
                        callback.onResponse("Error parsing response.");
                    }
                }
            });
        } catch (Exception e) {
            callback.onResponse("Error creating request.");
        }
    }
}
