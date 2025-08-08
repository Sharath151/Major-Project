package com.example.app;

import android.os.Bundle;
import android.widget.ProgressBar;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class ProgressActivity extends AppCompatActivity {

    TextView textLessonsCompleted, textScore;
    ProgressBar progressBarLessons;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_progress);

        textLessonsCompleted = findViewById(R.id.textLessonsCompleted);
        textScore = findViewById(R.id.textScore);
        progressBarLessons = findViewById(R.id.progressBarLessons);

        // Example static data – in real app, fetch from local DB
        int lessonsCompleted = 3;
        int totalLessons = 10;
        int score = 75;

        textLessonsCompleted.setText("Lessons Completed: " + lessonsCompleted + "/" + totalLessons);
        progressBarLessons.setProgress((lessonsCompleted * 100) / totalLessons);
        textScore.setText("Score: " + score + "%");
    }
}
