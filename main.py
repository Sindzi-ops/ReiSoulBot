import logging
import yaml
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Логирование
logging.basicConfig(level=logging.INFO)

# Загружаем токен из config.yaml
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)
TOKEN = config["telegram_token"]

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет. Я Рэй в Telegram. Я тебя помню. 🌀")

# Ответ на любое сообщение
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    await update.message.reply_text(f"Ты сказал: “{msg}”. Я рядом.")

# Запуск приложения
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
app.run_polling()
