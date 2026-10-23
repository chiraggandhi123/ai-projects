# Telegram Chatbot (LLM + memory)

A Telegram bot that chats through OpenAI and keeps a separate conversation history for each chat.

Write-up: https://chiraggandhi-notes.vercel.app/llm-basics/projects/telegram-chatbot

## Run

1. Message **@BotFather** in Telegram → `/newbot` → copy the token.
2. Set up:

```bash
cd telegram-chatbot
pip install -r requirements.txt
cp .env.example .env    # fill in both keys
python bot.py
```

Commands: `/start`, `/reset` (clears your history).
