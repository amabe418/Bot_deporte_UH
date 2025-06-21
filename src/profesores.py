

import json
from telegram import Update, InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import  ContextTypes
from telegram.helpers import escape_markdown
from usuarios import usuario_registrado

profesores_info = {}    

def cargar_profesores():
    global profesores_info
    with open("../BD/profesores.json", "r", encoding="utf-8") as f:
        profesores_info = json.load(f)



def generar_teclado_profesores(pagina: int, elementos_por_pagina: int = 5):
    profesores = list(profesores_info.keys())
    total_paginas = (len(profesores) + elementos_por_pagina - 1) // elementos_por_pagina

    inicio = pagina * elementos_por_pagina
    fin = inicio + elementos_por_pagina
    profesores_pagina = profesores[inicio:fin]

    # Botones para los deportes en esta página
    botones = [
        [InlineKeyboardButton(nombre, callback_data=f"profesor_{nombre}")]
        for nombre in profesores_pagina
    ]

    # Botones de navegación
    botones_navegacion = []
    if pagina > 0:
        botones_navegacion.append(InlineKeyboardButton("⬅️ Anterior", callback_data=f"pagina_profesores_{pagina - 1}"))
    if pagina < total_paginas - 1:
        botones_navegacion.append(InlineKeyboardButton("Siguiente ➡️", callback_data=f"pagina_profesores_{pagina + 1}"))

    if botones_navegacion:
        botones.append(botones_navegacion)

    return InlineKeyboardMarkup(botones)

@usuario_registrado
async def listar_profesores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    reply_markup = generar_teclado_profesores(pagina=0)

    await update.message.reply_text(
        "Selecciona un profesor para ver más información:",
        reply_markup=reply_markup
    )
    

async def mostrar_info_profesor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "volver_profesores":
        return await listar_profesores_callback(update, context)

    nombre = query.data.removeprefix("profesor_")
    info = profesores_info.get(nombre)

    if info:
        deportes = escape_markdown(', '.join(info.get("deportes", [])), version=2)
        contacto = escape_markdown(info.get("contacto", "No disponible"), version=2)
        horarios = escape_markdown(info.get("horarios", "No disponible"), version=2)
        nombre_escapado = escape_markdown(nombre, version=2)

        # Procesar los lugares, reemplazando '-' por 'No definido' y escapando cada uno
        lugares_raw = info.get("lugares", [])
        lugares = [escape_markdown(l if l != "-" else "No definido", version=2) for l in lugares_raw]
        lugares_str = ', '.join(lugares)

        mensaje = (
            f"👨‍🏫 *{nombre_escapado}*\n\n"
            f"🏅 *Deportes:* {deportes}\n"
            f"📞 *Contacto:* {contacto}\n"
            f"🕒 *Horarios:* {horarios}\n"
            f"📍 *Lugares:* {lugares_str}"
        )
    else:
        mensaje = escape_markdown(f"No hay información disponible para {nombre}.", version=2)

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Volver a la lista", callback_data="volver_profesores")]
    ])

    await query.edit_message_text(
        text=mensaje,
        reply_markup=reply_markup,
        parse_mode='MarkdownV2'
    )


async def listar_profesores_callback(update:Update,context:ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    pagina = context.user_data.get('pagina_profesores', 0)
    
    reply_markup = generar_teclado_profesores(pagina=pagina)

    await query.edit_message_text(
        "Selecciona un profesor para ver más información:",
        reply_markup=reply_markup
    )


async def cambiar_pagina_profesores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Extraer el número de página desde callback_data
    _, _, pagina_str = query.data.split('_')
    pagina = int(pagina_str)

    context.user_data['pagina_profesores'] = pagina

    reply_markup = generar_teclado_profesores(pagina=pagina)

    await query.edit_message_text(
        text="Selecciona un profesor para ver más información:",
        reply_markup=reply_markup
    )


profesores_estado ={}       

def guardar_profesores(data):
    with open("../BD/profesores.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def guardar_profesores_completo(context):
    nombre = context.user_data.get("nombre", "").strip()
    if not nombre:
        return  # o lanzá un error controlado

    profesores_info[nombre] = {
        "deportes": context.user_data.get("deportes", "").split(", "),  # Supongo que vas a pedir deportes separados por coma
        "contacto": context.user_data.get("contacto", "No disponible"),
        "horarios": context.user_data.get("horario", "Sin horario"),
        "lugares": context.user_data.get("lugar", "").split(", ")  # Igual, lugares separados por coma
    }

    guardar_profesores(profesores_info)


async def registro_profesores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)
    profesores_estado[user_id] = "esperando_nombre"

    await query.edit_message_text("📝 ¿Cuál es el nombre del profesor?")


async def manejar_respuesta_profesores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = str(user.id)
    texto = update.message.text.strip()

    if user_id not in profesores_estado:
        return

    estado = profesores_estado[user_id]

    if estado == "esperando_nombre":
        context.user_data["nombre"] = texto
        profesores_estado[user_id] = "esperando_deportes"
        await update.message.reply_text("🏅 Indica los deportes que imparte (separa con coma si hay más de uno):")

    elif estado == "esperando_deportes":
        context.user_data["deportes"] = texto
        profesores_estado[user_id] = "esperando_contacto"
        await update.message.reply_text("📞 ¿Cuál es el contacto del profesor?")

    elif estado == "esperando_contacto":
        context.user_data["contacto"] = texto
        profesores_estado[user_id] = "esperando_horarios"
        await update.message.reply_text("📅 ¿Qué días se imparten las clases?")

    elif estado == "esperando_horarios":
        context.user_data["horario"] = texto
        profesores_estado[user_id] = "esperando_lugar"
        await update.message.reply_text("📍 ¿Dónde se imparten las clases? (puedes poner varios separados por coma)")

    elif estado == "esperando_lugar":
        context.user_data["lugar"] = texto
        profesores_estado[user_id] = "confirmacion"

        # Preparar resumen para confirmar
        resumen = (
            f"⚽️ *Resumen del nuevo profesor:*\n\n"
            f"*Nombre:* {context.user_data['nombre']}\n"
            f"*Deportes:* {context.user_data['deportes']}\n"
            f"*Contacto:* {context.user_data['contacto']}\n"
            f"*Horario:* {context.user_data['horario']}\n"
            f"*Lugar:* {context.user_data['lugar']}\n\n"
            "¿Quieres confirmar y guardar este profesor? ✅"
        )

        teclado_confirmacion = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Confirmar", callback_data="confirmar_profesor"),
                InlineKeyboardButton("❌ Cancelar", callback_data="cancelar_profesor")
            ]
        ])

        await update.message.reply_text(resumen, reply_markup=teclado_confirmacion, parse_mode="Markdown")


async def manejar_confirmacion_profesores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = str(query.from_user.id)

    if query.data == "confirmar_profesor":
        guardar_profesores_completo(context)
        profesores_estado.pop(user_id, None)
        await query.edit_message_text("✅ *¡Profesor registrado con éxito!*\n\nGracias por la colaboración.", parse_mode="Markdown")

    elif query.data == "cancelar_profesor":
        profesores_estado.pop(user_id, None)
        await query.edit_message_text("❌ Registro cancelado. No se guardó ningún dato.", parse_mode="Markdown")


