package com.example.app;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ToggleButton;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;
import java.util.List;

public class ChatbotActivity extends AppCompatActivity {

    private RecyclerView chatRecyclerView;
    private EditText messageEditText;
    private Button sendButton;
    private ToggleButton toggleModeButton;

    private ChatAdapter adapter;
    private ArrayList<ChatMessage> messageList;

    private searchOptimize searchOptimize;
    private Gemini gemini;

    private boolean isOnlineMode = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chatbot);

        chatRecyclerView = findViewById(R.id.chatRecyclerView);
        messageEditText = findViewById(R.id.messageEditText);
        sendButton = findViewById(R.id.sendButton);
        toggleModeButton = findViewById(R.id.toggleModeButton);

        messageList = new ArrayList<>();
        adapter = new ChatAdapter(messageList);
        chatRecyclerView.setLayoutManager(new LinearLayoutManager(this));
        chatRecyclerView.setAdapter(adapter);

        // Load offline questions and initialize smart search
        List<QuestionAnswer> qaList = JsonUtils.loadQuestionsFromAsset(this);
        searchOptimize = new searchOptimize(qaList);

        // online chatbot
        gemini = new Gemini();

        // Toggle between modes
        toggleModeButton.setOnCheckedChangeListener((buttonView, isChecked) -> {
            isOnlineMode = isChecked;
            showSystemMessage("Switched to " + (isOnlineMode ? "Online" : "Offline") + " Mode");
        });

        sendButton.setOnClickListener(v -> {
            String userMsg = messageEditText.getText().toString().trim();
            if (!userMsg.isEmpty()) {
                messageList.add(new ChatMessage(userMsg, true));
                adapter.notifyItemInserted(messageList.size() - 1);
                chatRecyclerView.scrollToPosition(messageList.size() - 1);
                messageEditText.setText("");

                if (isOnlineMode) {
                    // Online Mode
                    gemini.getOnlineReply(userMsg, reply -> runOnUiThread(() -> {
                        messageList.add(new ChatMessage(reply, false));
                        adapter.notifyItemInserted(messageList.size() - 1);
                        chatRecyclerView.scrollToPosition(messageList.size() - 1);
                    }));
                } else {
                    // Offline Mode
                    String reply = searchOptimize.getBestAnswer(userMsg);
                    messageList.add(new ChatMessage(reply, false));
                    adapter.notifyItemInserted(messageList.size() - 1);
                    chatRecyclerView.scrollToPosition(messageList.size() - 1);
                }
            }
        });
    }

    private void showSystemMessage(String msg) {
        messageList.add(new ChatMessage(msg, false));
        adapter.notifyItemInserted(messageList.size() - 1);
        chatRecyclerView.scrollToPosition(messageList.size() - 1);
    }
}
