package com.example.app;

import java.util.*;

public class searchOptimize {
    private List<QuestionAnswer> qaList;

    public searchOptimize(List<QuestionAnswer> qaList) {
        this.qaList = qaList;
    }

    public String getBestAnswer(String userQuestion) {
        userQuestion = userQuestion.toLowerCase();
        double bestScore = 0;
        String bestAnswer = "Sorry, I don't know the answer to that.";

        for (QuestionAnswer qa : qaList) {
            double score = getSimilarity(userQuestion, qa.getQuestion().toLowerCase());
            if (score > bestScore) {
                bestScore = score;
                bestAnswer = qa.getAnswer();
            }
        }

        return bestAnswer;
    }

    private double getSimilarity(String s1, String s2) {
        Set<String> words = new HashSet<>();
        List<String> tokens1 = Arrays.asList(s1.split("\\s+"));
        List<String> tokens2 = Arrays.asList(s2.split("\\s+"));
        words.addAll(tokens1);
        words.addAll(tokens2);

        int[] vec1 = new int[words.size()];
        int[] vec2 = new int[words.size()];
        int i = 0;

        for (String word : words) {
            vec1[i] = Collections.frequency(tokens1, word);
            vec2[i] = Collections.frequency(tokens2, word);
            i++;
        }

        return cosine(vec1, vec2);
    }

    private double cosine(int[] vec1, int[] vec2) {
        int dot = 0, mag1 = 0, mag2 = 0;
        for (int i = 0; i < vec1.length; i++) {
            dot += vec1[i] * vec2[i];
            mag1 += vec1[i] * vec1[i];
            mag2 += vec2[i] * vec2[i];
        }
        return (mag1 == 0 || mag2 == 0) ? 0 : dot / (Math.sqrt(mag1) * Math.sqrt(mag2));
    }
}
