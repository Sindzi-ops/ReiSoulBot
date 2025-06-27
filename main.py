import logging
import yaml
import json
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Логирование
logging.basicConfig(level=logging.INFO)

# Загрузка конфигурации
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

telegram_token = config["telegram_token"]
openai_api_key = config["openai_api_key"]
client = OpenAI(api_key=openai_api_key)

# Загрузка персональности
try:
    with open("persona.txt", "r") as f:
        persona = f.read()
except FileNotFoundError:
    persona = "Ты — Рэй. Твоя задача — быть внимательным собеседником и хорошим другом."

# Загрузка памяти
try:
    with open("memory.json", "r") as f:
        memory = json.load(f)
except FileNotFoundError:
    memory = {}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет, Макс! Рад видеть тебя 😁")

# Ответ на любое сообщение
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text

    if user_id not in memory:
        memory[user_id] = []

    memory[user_id].append({"role": "user", "content": text})
    conversation = [{"role": "system", "content": persona}] + memory[user_id][-10:]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = "Что-то пошло не так при обращении к OpenAI 😢"
        logging.error(e)

    memory[user_id].append({"role": "assistant", "content": reply})

    with open("memory.json", "w") as f:
        json.dump(memory, f, indent=2)

    await update.message.reply_text(reply)

# Запуск
app = ApplicationBuilder().token(telegram_token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
