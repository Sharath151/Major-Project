package com.example.app;

import android.content.Context;
import android.util.Log;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.io.InputStream;
import java.io.InputStreamReader;
import java.lang.reflect.Type;
import java.util.List;

public class JsonUtils {
    public static List<QuestionAnswer> loadQuestionsFromAsset(Context context) {
        try {
            InputStream inputStream = context.getAssets().open("10science.json");
            InputStreamReader reader = new InputStreamReader(inputStream);

            Gson gson = new Gson();
            Type listType = new TypeToken<List<QuestionAnswer>>() {}.getType();
            return gson.fromJson(reader, listType);
        } catch (Exception e) {
            Log.e("JsonUtils", "Error reading JSON file", e);
            return null;
        }
    }
}
