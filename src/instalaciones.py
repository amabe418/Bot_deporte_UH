

import json
from telegram import Update
from telegram.ext import ContextTypes
from usuarios import usuario_registrado

instalaciones = {}

def cargar_instalaciones():
    global instalaciones
    with open("../BD/instalaciones.json", "r", encoding="utf-8") as f:
        instalaciones = json.load(f)


@usuario_registrado
async def listar_instalaciones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = "🏟️ *INSTALACIONES DEPORTIVAS*\n\n"
    
    for instalacion in instalaciones:
        mensaje += f"{instalacion}\n"
    
    await update.message.reply_text(mensaje, parse_mode='Markdown')

