package com.example.app;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import java.util.List;

public class ChatAdapter extends RecyclerView.Adapter<RecyclerView.ViewHolder> {

    private List<ChatMessage> chatList;

    public ChatAdapter(List<ChatMessage> chatList) {
        this.chatList = chatList;
    }

    @Override
    public int getItemViewType(int position) {
        return chatList.get(position).isUser() ? 0 : 1;
    }

    @NonNull
    @Override
    public RecyclerView.ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        if (viewType == 0) {
            View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_user, parent, false);
            return new UserViewHolder(view);
        } else {
            View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_bot, parent, false);
            return new BotViewHolder(view);
        }
    }

    @Override
    public void onBindViewHolder(@NonNull RecyclerView.ViewHolder holder, int position) {
        ChatMessage message = chatList.get(position);
        if (holder instanceof UserViewHolder) {
            ((UserViewHolder) holder).userText.setText(message.getMessage());
        } else if (holder instanceof BotViewHolder) {
            ((BotViewHolder) holder).botText.setText(message.getMessage());
        }
    }

    @Override
    public int getItemCount() {
        return chatList.size();
    }

    static class UserViewHolder extends RecyclerView.ViewHolder {
        TextView userText;

        public UserViewHolder(@NonNull View itemView) {
            super(itemView);
            userText = itemView.findViewById(R.id.text_user);
        }
    }

    static class BotViewHolder extends RecyclerView.ViewHolder {
        TextView botText;

        public BotViewHolder(@NonNull View itemView) {
            super(itemView);
            botText = itemView.findViewById(R.id.text_bot);
        }
    }
}

