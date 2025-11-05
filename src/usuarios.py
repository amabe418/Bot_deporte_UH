import json
from telegram import Update, InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime
import admin

registro_estado = {}
usuarios = {}

def cargar_usuarios():  
    global usuarios
    try:
        with open("../BD/usuarios.json", "r", encoding="utf-8") as f:
            usuarios=json.load(f)
    except FileNotFoundError:
        usuarios={}

def usuario_registrado(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = str(update.effective_user.id)
        if user_id not in usuarios:
            # Manejar tanto mensajes como callbacks
            if update.message:
                await update.message.reply_text("🚫 Debes registrarte antes de usar este comando.")
            elif update.callback_query:
                await update.callback_query.answer("🚫 Debes registrarte antes de usar este comando.", show_alert=True)
            return
        return await func(update, context)
    return wrapper


def guardar_usuarios(usuarios):
    with open("../BD/usuarios.json", "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)

def guardar_admins(admin_ids):
    with open("../BD/admins.json", "w", encoding="utf-8") as f:
        json.dump({"admins": admin_ids}, f, indent=4, ensure_ascii=False)

def guardar_usuario_completo(user_id, username, context):
    
    usuarios[user_id] = {
        "nombre": context.user_data.get("nombre", ""),
        "username": username if username else "No disponible",
        "fecha_registro": str(datetime.now()),
        "tipo": context.user_data.get("tipo", ""),
        "info_adicional": {
            "carrera": context.user_data.get("carrera", ""),
            "año": context.user_data.get("año", "")
        }
    }
    guardar_usuarios(usuarios)
    # Solo hacer admin al primer usuario si no hay ningún admin registrado
    if not admin.ADMIN_IDS or len(admin.ADMIN_IDS) == 0:
        admin.ADMIN_IDS = [user_id]
        guardar_admins(admin.ADMIN_IDS)


async def registro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    registro_estado[user_id] = "esperando_nombre"
    await update.message.reply_text("¿Cuál es tu nombre completo?")



async def manejar_tipo_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    tipo = query.data.split("_")[1]
    user_id = str(query.from_user.id)
    context.user_data["tipo"] = tipo

    if tipo == "profesor":
        guardar_usuario_completo(user_id, query.from_user.username, context)
        await query.edit_message_text("¡Gracias! Has sido registrado como profesor.")
        registro_estado.pop(user_id, None)
    else:
        registro_estado[user_id] = "esperando_carrera"
        await query.edit_message_text("¿Cuál es tu carrera?")





async def manejar_respuesta_registro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = str(user.id)
    texto = update.message.text.strip()

    if user_id not in registro_estado:
        return

    estado = registro_estado[user_id]

    if estado == "esperando_nombre":
        context.user_data["nombre"] = texto
        registro_estado[user_id] = "esperando_tipo"
        keyboard = [
            [InlineKeyboardButton("Profesor", callback_data="tipo_profesor")],
            [InlineKeyboardButton("Estudiante", callback_data="tipo_estudiante")]
        ]
        await update.message.reply_text("¿Eres profesor o estudiante?", reply_markup=InlineKeyboardMarkup(keyboard))

    elif estado == "esperando_carrera":
        context.user_data["carrera"] = texto
        registro_estado[user_id] = "esperando_año"
        await update.message.reply_text("¿Qué año cursas?")

    elif estado == "esperando_año":
        context.user_data["año"] = texto
        guardar_usuario_completo(user_id, user.username, context)
        del registro_estado[user_id]
        await update.message.reply_text(
            "✅ *¡Registro completado con éxito!*\n\n"
            "Ya puedes comenzar a usar el bot y explorar las actividades deportivas 🏀🏐🏊",
            parse_mode="Markdown"
        )
        


