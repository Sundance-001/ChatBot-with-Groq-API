# telegram bot that uses Groq's Llama 3 model to chat with users
import os
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("groq_api_key")
TELEGRAM_BOT_TOKEN = os.getenv("bot_token")
NAME, AGE, LANGUAGE, CHAT = range(4)
def groq_llama_chat(messages):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": messages
    }

    res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"]
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["chat_history"] = [{"role": "system", "content": "You're a helpful assistant."}]
    await update.message.reply_text("Hi! What's your name?")
    return NAME
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text
    context.user_data["name"] = name
    await update.message.reply_text(f"Nice to meet you, {name}! How old are you?")
    return AGE
async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    age = update.message.text
    context.user_data["age"] = age
    await update.message.reply_text("Cool! What's your favorite programming language?")
    return LANGUAGE
async def get_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = update.message.text
    name = context.user_data["name"]
    age = context.user_data["age"]
    context.user_data["language"] = lang

    intro = (
        f"The user is named {name}, is {age} years old, and likes {lang}.\n"
        f"Start a friendly conversation with them!"
    )
    context.user_data["chat_history"].append({"role": "user", "content": intro})

    try:
        response = groq_llama_chat(context.user_data["chat_history"])
        context.user_data["chat_history"].append({"role": "assistant", "content": response})
        await update.message.reply_text(response)
        return CHAT
    except Exception as e:
        print("Error:", e)
        await update.message.reply_text("Sorry, I had trouble starting the conversation.")
        return ConversationHandler.END
async def chat_loop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    context.user_data["chat_history"].append({"role": "user", "content": user_input})
    try:
        response = groq_llama_chat(context.user_data["chat_history"])
        context.user_data["chat_history"].append({"role": "assistant", "content": response})
        await update.message.reply_text(response)
        return CHAT
    except Exception as e:
        print("Error:", e)
        await update.message.reply_text("Oops! Something went wrong.")
        return ConversationHandler.END
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Conversation cancelled. Bye!")
    return ConversationHandler.END
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
        LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_language)],
        CHAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, chat_loop)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
app.add_handler(conv_handler)
app.run_polling()
