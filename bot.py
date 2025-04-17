from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import hupper

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola, te doy la bienvenida al bot de deportes de la Universidad de la Habana!")

async def horario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Los horarios aún no están disponibles, pero pronto lo estarán.")

application = ApplicationBuilder().token("7906733724:AAHvuyxL5t9lr5_NZpnphckAeL1Zj3Ogw10").build()
application.add_handler( CommandHandler("start", welcome ))
application.add_handler(CommandHandler("horario", horario))
application.run_polling(allowed_updates=Update.ALL_TYPES)