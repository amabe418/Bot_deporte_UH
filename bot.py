# hupper -m bot.py
import os
import threading
from flask import Flask
from telegram import Update
from google.oauth2.service_account import Credentials
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# region Metodos
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola, te doy la bienvenida al bot de deportes de la Universidad de la Habana!")

async def horario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Los horarios aún no están disponibles, pero pronto lo estarán.")

# endregion

# region Principal
app = Flask(__name__)

token = "7906733724:AAHvuyxL5t9lr5_NZpnphckAeL1Zj3Ogw10"
application = ApplicationBuilder().token(token).build()
application.add_handler( CommandHandler("start", welcome ))
application.add_handler(CommandHandler("horario", horario))
# application.run_polling(allowed_updates=Update.ALL_TYPES)

@app.route('/')
def home():
    return "El bot de Telegram está funcionando."

def start_telegram_bot():
    application.run_polling(allowed_updates=Update.ALL_TYPES)

thread = threading.Thread(target=start_telegram_bot)
thread.start()
# endregion


#endregion