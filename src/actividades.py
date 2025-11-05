


import json
from telegram import Update, InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import ContextTypes
import usuarios
import deporte

actividades = {}
def cargar_actividades():
    global actividades
    with open("../BD/noticias.json","r",encoding="utf-8") as f:
        actividades = json.load(f)

@usuarios.usuario_registrado
async def actividades(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton(nombre_deporte, callback_data=f"actividad_{nombre_deporte}")]
        for nombre_deporte in deporte.deportes_info.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🏅 Selecciona una actividad para ver detalles:",
        reply_markup=reply_markup
    )

@usuarios.usuario_registrado
async def mostrar_noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not actividades:
        await update.message.reply_text("No hay actividades disponibles en este momento.")
        return

    mensaje = "📰 *Noticias y Actividades Próximas:*\n\n"
    for noticia in actividades:
        mensaje += f"🔹 *{noticia['titulo']}* ({noticia['fecha']})\n"
        mensaje += f"{noticia['descripcion']}\n\n"

    await update.message.reply_text(mensaje, parse_mode="Markdown")

@usuarios.usuario_registrado
async def actividades_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton(nombre_deporte, callback_data=f"actividad_{nombre_deporte}")]
        for nombre_deporte in deporte.deportes_info.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="🏅 Selecciona una actividad para ver detalles:",
        reply_markup=reply_markup
    )
