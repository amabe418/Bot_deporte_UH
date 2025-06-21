

import json
from telegram import Update
from telegram.ext import ContextTypes
from usuarios import usuario_registrado

@usuario_registrado
async def horario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Los horarios aún no están disponibles, pero pronto lo estarán.")


