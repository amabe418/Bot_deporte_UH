

import json
from telegram import Update, InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown
from usuarios import usuario_registrado


deportes_info = {}

def cargar_deportes():
    global deportes_info
    with open("../BD/deportes.json", "r", encoding="utf-8") as f:
        deportes_info = json.load(f)



def generar_teclado_deportes(pagina: int, elementos_por_pagina: int = 5):
    deportes = list(deportes_info.keys())
    total_paginas = (len(deportes) + elementos_por_pagina - 1) // elementos_por_pagina

    inicio = pagina * elementos_por_pagina
    fin = inicio + elementos_por_pagina
    deportes_pagina = deportes[inicio:fin]

    # Botones para los deportes en esta página
    botones = [
        [InlineKeyboardButton(nombre, callback_data=f"deporte_{nombre}")]
        for nombre in deportes_pagina
    ]

    # Botones de navegación
    botones_navegacion = []
    if pagina > 0:
        botones_navegacion.append(InlineKeyboardButton("⬅️ Anterior", callback_data=f"pagina_deportes_{pagina - 1}"))
    if pagina < total_paginas - 1:
        botones_navegacion.append(InlineKeyboardButton("Siguiente ➡️", callback_data=f"pagina_deportes_{pagina + 1}"))

    if botones_navegacion:
        botones.append(botones_navegacion)

    return InlineKeyboardMarkup(botones)

@usuario_registrado
async def listar_deportes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    reply_markup = generar_teclado_deportes(pagina=0)

    await update.message.reply_text(
        "Selecciona un deportes para ver más información:",
        reply_markup=reply_markup
    )

@usuario_registrado
async def mostrar_info_deporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "volver_deportes":
        return await listar_deportes_callback(update, context)

    nombre = query.data.removeprefix("deporte_")
    info = deportes_info.get(nombre)

    if info:
        profesor = escape_markdown(info.get("profesor", "No disponible"), version=2)
        contacto = escape_markdown(info.get("contacto", "No disponible"), version=2)
        dias = escape_markdown(info.get("dias","No disponible"),version =2)
        horarios = escape_markdown(info.get("horario", "No disponible"), version=2)
        nombre_escapado = escape_markdown(nombre, version=2)

        # Procesar los lugares, reemplazando '-' por 'No definido' y escapando cada uno
        lugares_raw = info.get("lugar", [])
        lugares = [escape_markdown(l if l != "-" else "No definido", version=2) for l in lugares_raw]
        lugares_str = ', '.join(lugares)

        mensaje = (
            f"🏅 *{nombre_escapado}*\n\n"
            f"👨‍🏫 *Profesor:* {profesor}\n"
            f"📞 *Contacto:* {contacto}\n"
            f"📅 *Dias:* {dias}\n"
            f"🕒 *Horarios:* {horarios}\n"
            f"📍 *Lugares:* {lugares_str}"
        )
    else:
        mensaje = escape_markdown(f"No hay información disponible para {nombre}.", version=2)

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Volver a la lista", callback_data="volver_deportes")]
    ])

    await query.edit_message_text(
        text=mensaje,
        reply_markup=reply_markup,
        parse_mode='MarkdownV2'
    )

async def listar_deportes_callback(update:Update,context:ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    pagina = context.user_data.get('pagina_deportes', 0)
    
    reply_markup = generar_teclado_deportes(pagina=pagina)

    await query.edit_message_text(
        "Selecciona un deporte para ver más información:",
        reply_markup=reply_markup
    )


async def cambiar_pagina_deportes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Extraer el número de página desde callback_data
    _, _, pagina_str = query.data.split('_')
    pagina = int(pagina_str)

    context.user_data['pagina_deportes'] = pagina

    reply_markup = generar_teclado_deportes(pagina=pagina)

    await query.edit_message_text(
        text="Selecciona un deporte para ver más información:",
        reply_markup=reply_markup
    )

deporte_estado={}

def guardar_deportes(data):
    with open("../BD/deportes.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def guardar_deporte_completo(context):
    nombre = context.user_data.get("nombre", "").strip()
    if not nombre:
        return  # o lanzá un error controlado

    deportes_info[nombre] = {
        "profesor": context.user_data.get("profesor", "Desconocido"),
        "contacto": context.user_data.get("contacto", "No disponible"),
        "dias": context.user_data.get("dias", "Por definir"),
        "horario": context.user_data.get("horario", "Sin horario"),
        "lugar": context.user_data.get("lugar", ["-"]) if isinstance(context.user_data.get("lugar"), list) else [context.user_data.get("lugar", "-")]
    }

    guardar_deportes(deportes_info)



async def registro_deporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)
    deporte_estado[user_id] = "esperando_nombre"

    await query.edit_message_text("¿Cuál es el nombre del deporte?")

async def manejar_respuesta_deporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    deporte_id = str(user.id)
    texto = update.message.text.strip()

    if deporte_id not in deporte_estado:
        return

    estado = deporte_estado[deporte_id]

    if estado == "esperando_nombre":
        context.user_data["nombre"] = texto
        deporte_estado[deporte_id] = "esperando_profesor"
        await update.message.reply_text("🏅 Inserta el nombre del profesor que imparte este deporte:")

    elif estado == "esperando_profesor":
        context.user_data["profesor"] = texto
        deporte_estado[deporte_id] = "esperando_contacto"
        await update.message.reply_text("📞 ¿Cuál es el contacto del profesor?")

    elif estado == "esperando_contacto":
        context.user_data["contacto"] = texto
        deporte_estado[deporte_id] = "esperando_dias"
        await update.message.reply_text("📅 ¿Qué días se imparten las clases?")

    elif estado == "esperando_dias":
        context.user_data["dias"] = texto
        deporte_estado[deporte_id] = "esperando_horarios"
        await update.message.reply_text("⏰ ¿En qué horarios se imparten?")

    elif estado == "esperando_horarios":
        context.user_data["horario"] = texto
        deporte_estado[deporte_id] = "esperando_lugar"
        await update.message.reply_text("📍 ¿Dónde se imparten las clases?")

    elif estado == "esperando_lugar":
        context.user_data["lugar"] = texto
        deporte_estado[deporte_id] = "confirmacion"

        # Armar el resumen bonito para mostrar
        resumen = (
            f"⚽️ *Resumen del nuevo deporte:*\n\n"
            f"*Nombre:* {context.user_data['nombre']}\n"
            f"*Profesor:* {context.user_data['profesor']}\n"
            f"*Contacto:* {context.user_data['contacto']}\n"
            f"*Días:* {context.user_data['dias']}\n"
            f"*Horario:* {context.user_data['horario']}\n"
            f"*Lugar:* {context.user_data['lugar']}\n\n"
            "¿Quieres confirmar y guardar este deporte? ✅"
        )

        teclado_confirmacion = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Confirmar", callback_data="confirmar_deporte"),
                InlineKeyboardButton("❌ Cancelar", callback_data="cancelar_deporte")
            ]
        ])

        await update.message.reply_text(resumen, reply_markup=teclado_confirmacion, parse_mode="Markdown")

async def manejar_confirmacion_deporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = str(query.from_user.id)

    if query.data == "confirmar_deporte":
        guardar_deporte_completo(context)
        deporte_estado.pop(user_id, None)
        await query.edit_message_text("✅ *¡Deporte registrado con éxito!*\n\nGracias por la colaboración.", parse_mode="Markdown")

    elif query.data == "cancelar_deporte":
        deporte_estado.pop(user_id, None)
        await query.edit_message_text("❌ Registro cancelado. No se guardó ningún dato.", parse_mode="Markdown")
