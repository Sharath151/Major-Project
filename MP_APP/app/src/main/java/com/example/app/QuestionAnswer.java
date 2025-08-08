package com.example.app;

public class QuestionAnswer {
    private final String question;
    private final String answer;

    // Constructor
    public QuestionAnswer(String question, String answer) {
        this.question = question;
        this.answer = answer;
    }

    // Getter for question
    public String getQuestion() {
        return question;
    }

    // Getter for answer
    public String getAnswer() {
        return answer;
    }
}
