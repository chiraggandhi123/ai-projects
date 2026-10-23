import os
from collections import defaultdict

import openai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()
client = openai.AsyncOpenAI()

MODEL = "gpt-4o-mini"            # fast + cheap is fine for chat
SYSTEM = "You are a helpful, friendly assistant on Telegram. Keep replies short."
MAX_MESSAGES = 20

histories: dict[int, list[dict]] = defaultdict(list)   # chat_id -> messages


def trimmed(messages):
    recent = messages[-MAX_MESSAGES:]
    while recent and recent[0]["role"] != "user":
        recent = recent[1:]
    return recent


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Ask me anything. /reset clears our chat.")


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    histories.pop(update.effective_chat.id, None)
    await update.message.reply_text("Memory cleared.")


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    history = histories[chat_id]
    history.append({"role": "user", "content": update.message.text})

    await context.bot.send_chat_action(chat_id, "typing")
    try:
        response = await client.chat.completions.create(
            model=MODEL,
            max_completion_tokens=1024,
            messages=[{"role": "system", "content": SYSTEM}, *trimmed(history)],
        )
    except openai.APIError:
        history.pop()
        await update.message.reply_text("Sorry, something went wrong. Try again.")
        return

    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})
    await update.message.reply_text(reply)


def main():
    app = Application.builder().token(os.environ["TELEGRAM_BOT_TOKEN"]).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()


if __name__ == "__main__":
    main()
