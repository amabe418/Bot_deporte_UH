
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown
from admin import solo_admins
import deporte

# Estados para operaciones de admin
admin_deporte_estado = {}


def generar_teclado_deportes_admin(pagina: int, elementos_por_pagina: int = 5, accion="modificar"):
    """Genera teclado de deportes para admin con paginación"""
    deportes = list(deporte.deportes_info.keys())
    total_paginas = (len(deportes) + elementos_por_pagina - 1) // elementos_por_pagina

    inicio = pagina * elementos_por_pagina
    fin = inicio + elementos_por_pagina
    deportes_pagina = deportes[inicio:fin]

    botones = [
        [InlineKeyboardButton(nombre, callback_data=f"admin_{accion}_deporte_{nombre}")]
        for nombre in deportes_pagina
    ]

    botones_navegacion = []
    if pagina > 0:
        botones_navegacion.append(InlineKeyboardButton("⬅️ Anterior", callback_data=f"admin_pagina_{accion}_deportes_{pagina - 1}"))
    if pagina < total_paginas - 1:
        botones_navegacion.append(InlineKeyboardButton("Siguiente ➡️", callback_data=f"admin_pagina_{accion}_deportes_{pagina + 1}"))

    if botones_navegacion:
        botones.append(botones_navegacion)
    
    botones.append([InlineKeyboardButton("🔙 Volver", callback_data="admin_menu_deportes")])

    return InlineKeyboardMarkup(botones)


@solo_admins
async def agregar_deporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia el flujo para agregar un nuevo deporte"""
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)
    admin_deporte_estado[user_id] = {"accion": "agregar", "estado": "esperando_nombre"}
    context.user_data.clear()

    await query.edit_message_text("📝 ¿Cuál es el nombre del nuevo deporte?")


@solo_admins
async def listar_deportes_para_modificar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lista deportes para seleccionar cuál modificar"""
    query = update.callback_query
    await query.answer()

    if not deporte.deportes_info:
        await query.edit_message_text(
            "❌ No hay deportes registrados.\n\n🔙 Volver al menú de deportes.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Volver", callback_data="admin_menu_deportes")]
            ])
        )
        return

    reply_markup = generar_teclado_deportes_admin(pagina=0, accion="modificar")
    await query.edit_message_text(
        "✏️ Selecciona el deporte que deseas modificar:",
        reply_markup=reply_markup
    )


@solo_admins
async def listar_deportes_para_eliminar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lista deportes para seleccionar cuál eliminar"""
    query = update.callback_query
    await query.answer()

    if not deporte.deportes_info:
        await query.edit_message_text(
            "❌ No hay deportes registrados.\n\n🔙 Volver al menú de deportes.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Volver", callback_data="admin_menu_deportes")]
            ])
        )
        return

    reply_markup = generar_teclado_deportes_admin(pagina=0, accion="eliminar")
    await query.edit_message_text(
        "🗑️ Selecciona el deporte que deseas eliminar:",
        reply_markup=reply_markup
    )


@solo_admins
async def listar_deportes_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lista todos los deportes con opciones de edición"""
    query = update.callback_query
    await query.answer()

    if not deporte.deportes_info:
        await query.edit_message_text(
            "❌ No hay deportes registrados.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Volver", callback_data="admin_menu_deportes")]
            ])
        )
        return

    reply_markup = generar_teclado_deportes_admin(pagina=0, accion="ver")
    await query.edit_message_text(
        "📋 Selecciona un deporte para ver detalles:",
        reply_markup=reply_markup
    )


@solo_admins
async def seleccionar_campo_modificar_deporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra los campos que se pueden modificar de un deporte"""
    query = update.callback_query
    await query.answer()

    # Extraer nombre del deporte del callback_data
    partes = query.data.split("_deporte_", 1)
    if len(partes) < 2:
        await query.answer("Error al procesar la solicitud", show_alert=True)
        return

    nombre_deporte = partes[1]
    info = deporte.deportes_info.get(nombre_deporte)

    if not info:
        await query.answer("Deporte no encontrado", show_alert=True)
        return

    user_id = str(query.from_user.id)
    admin_deporte_estado[user_id] = {
        "accion": "modificar",
        "deporte": nombre_deporte,
        "estado": "seleccionando_campo"
    }
    context.user_data["deporte_modificar"] = nombre_deporte

    mensaje = f"✏️ <b>Modificar Deporte: {nombre_deporte}</b>\n\n"
    mensaje += f"📋 <b>Información actual:</b>\n"
    mensaje += f"👨‍🏫 Profesor: {info.get('profesor', 'No disponible')}\n"
    mensaje += f"📞 Contacto: {info.get('contacto', 'No disponible')}\n"
    mensaje += f"📅 Días: {info.get('dias', 'No disponible')}\n"
    mensaje += f"🕒 Horario: {info.get('horario', 'No disponible')}\n"
    lugares = info.get('lugar', [])
    lugares_str = ', '.join(lugares) if isinstance(lugares, list) else lugares
    mensaje += f"📍 Lugar: {lugares_str}\n\n"
    mensaje += "¿Qué campo deseas modificar?"

    keyboard = [
        [InlineKeyboardButton("📝 Nombre", callback_data=f"admin_modificar_campo_deporte_{nombre_deporte}_nombre")],
        [InlineKeyboardButton("👨‍🏫 Profesor", callback_data=f"admin_modificar_campo_deporte_{nombre_deporte}_profesor")],
        [InlineKeyboardButton("📞 Contacto", callback_data=f"admin_modificar_campo_deporte_{nombre_deporte}_contacto")],
        [InlineKeyboardButton("📅 Días", callback_data=f"admin_modificar_campo_deporte_{nombre_deporte}_dias")],
        [InlineKeyboardButton("🕒 Horario", callback_data=f"admin_modificar_campo_deporte_{nombre_deporte}_horario")],
        [InlineKeyboardButton("📍 Lugar", callback_data=f"admin_modificar_campo_deporte_{nombre_deporte}_lugar")],
        [InlineKeyboardButton("🔙 Volver", callback_data="admin_menu_deportes")]
    ]

    await query.edit_message_text(mensaje, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))


@solo_admins
async def iniciar_modificacion_campo_deporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia la modificación de un campo específico"""
    query = update.callback_query
    await query.answer()

    # Formato: admin_modificar_campo_deporte_NOMBRE_CAMPO
    # Separar por "_deporte_" primero
    partes = query.data.split("_deporte_", 1)
    if len(partes) < 2:
        await query.answer("Error al procesar", show_alert=True)
        return

    # El resto contiene: NOMBRE_CAMPO
    resto = partes[1]
    # Los campos posibles son: nombre, profesor, contacto, dias, horario, lugar
    # Extraer el campo (último elemento después del último _)
    campos_posibles = ["nombre", "profesor", "contacto", "dias", "horario", "lugar"]
    campo = None
    nombre_deporte = None
    
    # Buscar el campo al final
    for campo_posible in campos_posibles:
        if resto.endswith(f"_{campo_posible}"):
            campo = campo_posible
            nombre_deporte = resto[:-len(f"_{campo_posible}")]
            break
    
    if not campo:
        await query.answer("Error: Campo no reconocido", show_alert=True)
        return

    user_id = str(query.from_user.id)
    admin_deporte_estado[user_id] = {
        "accion": "modificar",
        "deporte": nombre_deporte,
        "campo": campo,
        "estado": f"esperando_nuevo_{campo}"
    }
    context.user_data["deporte_modificar"] = nombre_deporte
    context.user_data["campo_modificar"] = campo

    campo_nombres = {
        "nombre": "nombre del deporte",
        "profesor": "nombre del profesor",
        "contacto": "contacto del profesor",
        "dias": "días de práctica",
        "horario": "horario",
        "lugar": "lugar(es) de práctica (separados por coma)"
    }

    nombre_campo = campo_nombres.get(campo, campo)
    await query.edit_message_text(f"📝 Ingresa el nuevo {nombre_campo}:")


@solo_admins
async def confirmar_eliminar_deporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Confirma la eliminación de un deporte"""
    query = update.callback_query
    await query.answer()

    # Extraer nombre del deporte
    partes = query.data.split("_deporte_", 1)
    if len(partes) < 2:
        await query.answer("Error al procesar", show_alert=True)
        return

    nombre_deporte = partes[1]
    info = deporte.deportes_info.get(nombre_deporte)

    if not info:
        await query.answer("Deporte no encontrado", show_alert=True)
        return

    user_id = str(query.from_user.id)
    admin_deporte_estado[user_id] = {
        "accion": "eliminar",
        "deporte": nombre_deporte,
        "estado": "confirmando"
    }
    context.user_data["deporte_eliminar"] = nombre_deporte

    mensaje = f"⚠️ <b>Confirmar eliminación</b>\n\n"
    mensaje += f"¿Estás seguro de que deseas eliminar el deporte:\n<b>{nombre_deporte}</b>?\n\n"
    mensaje += "Esta acción no se puede deshacer."

    keyboard = [
        [
            InlineKeyboardButton("✅ Sí, eliminar", callback_data=f"admin_confirmar_eliminar_deporte_{nombre_deporte}"),
            InlineKeyboardButton("❌ Cancelar", callback_data="admin_menu_deportes")
        ]
    ]

    await query.edit_message_text(mensaje, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))


@solo_admins
async def ejecutar_eliminar_deporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ejecuta la eliminación del deporte"""
    query = update.callback_query
    await query.answer()

    partes = query.data.split("_deporte_", 1)
    if len(partes) < 2:
        await query.answer("Error al procesar", show_alert=True)
        return

    nombre_deporte = partes[1]

    if nombre_deporte in deporte.deportes_info:
        del deporte.deportes_info[nombre_deporte]
        deporte.guardar_deportes(deporte.deportes_info)
        
        user_id = str(query.from_user.id)
        admin_deporte_estado.pop(user_id, None)
        context.user_data.pop("deporte_eliminar", None)

        await query.edit_message_text(
            f"✅ Deporte <b>{nombre_deporte}</b> eliminado exitosamente.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Volver al menú", callback_data="admin_menu_deportes")]
            ])
        )
    else:
        await query.answer("Deporte no encontrado", show_alert=True)


@solo_admins
async def ver_deporte_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra los detalles de un deporte con opciones de edición"""
    query = update.callback_query
    await query.answer()

    partes = query.data.split("_deporte_")
    if len(partes) < 2:
        await query.answer("Error", show_alert=True)
        return

    nombre_deporte = partes[1]
    info = deporte.deportes_info.get(nombre_deporte)

    if not info:
        await query.answer("Deporte no encontrado", show_alert=True)
        return

    mensaje = f"🏅 <b>{nombre_deporte}</b>\n\n"
    mensaje += f"👨‍🏫 <b>Profesor:</b> {info.get('profesor', 'No disponible')}\n"
    mensaje += f"📞 <b>Contacto:</b> {info.get('contacto', 'No disponible')}\n"
    mensaje += f"📅 <b>Días:</b> {info.get('dias', 'No disponible')}\n"
    mensaje += f"🕒 <b>Horario:</b> {info.get('horario', 'No disponible')}\n"
    lugares = info.get('lugar', [])
    lugares_str = ', '.join(lugares) if isinstance(lugares, list) else lugares
    mensaje += f"📍 <b>Lugar:</b> {lugares_str}"

    keyboard = [
        [
            InlineKeyboardButton("✏️ Modificar", callback_data=f"admin_modificar_deporte_{nombre_deporte}"),
            InlineKeyboardButton("🗑️ Eliminar", callback_data=f"admin_eliminar_deporte_{nombre_deporte}")
        ],
        [InlineKeyboardButton("🔙 Volver", callback_data="admin_listar_deportes")]
    ]

    await query.edit_message_text(mensaje, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))


async def cambiar_pagina_deportes_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cambia la página en la lista de deportes del admin"""
    query = update.callback_query
    await query.answer()

    # Formato: admin_pagina_ACCION_deportes_NUMERO
    partes = query.data.split("_deportes_", 1)
    if len(partes) < 2:
        await query.answer("Error", show_alert=True)
        return

    pagina = int(partes[1])
    # Extraer la acción del prefijo
    prefijo = partes[0]  # admin_pagina_ACCION
    accion = prefijo.split("_")[-1] if "_" in prefijo else "ver"  # modificar, eliminar, ver

    context.user_data['pagina_deportes_admin'] = pagina

    reply_markup = generar_teclado_deportes_admin(pagina=pagina, accion=accion)

    mensajes = {
        "modificar": "✏️ Selecciona el deporte que deseas modificar:",
        "eliminar": "🗑️ Selecciona el deporte que deseas eliminar:",
        "ver": "📋 Selecciona un deporte para ver detalles:"
    }

    await query.edit_message_text(
        text=mensajes.get(accion, "Selecciona un deporte:"),
        reply_markup=reply_markup
    )


@solo_admins
async def manejar_respuesta_modificacion_deporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja las respuestas durante la modificación de un deporte"""
    user_id = str(update.effective_user.id)
    
    if user_id not in admin_deporte_estado:
        return

    estado_info = admin_deporte_estado[user_id]
    
    if estado_info.get("accion") != "modificar":
        return

    texto = update.message.text.strip()
    nombre_deporte = estado_info.get("deporte")
    campo = estado_info.get("campo")

    if nombre_deporte not in deporte.deportes_info:
        await update.message.reply_text("❌ Error: Deporte no encontrado.")
        admin_deporte_estado.pop(user_id, None)
        return

    # Aplicar la modificación
    if campo == "nombre":
        # Si se cambia el nombre, crear nuevo y eliminar el viejo
        nuevo_nombre = texto
        if nuevo_nombre != nombre_deporte:
            deporte.deportes_info[nuevo_nombre] = deporte.deportes_info[nombre_deporte].copy()
            del deporte.deportes_info[nombre_deporte]
            nombre_deporte = nuevo_nombre
    elif campo == "lugar":
        # Lugar puede ser lista o string
        lugares = [l.strip() for l in texto.split(",")]
        deporte.deportes_info[nombre_deporte][campo] = lugares
    else:
        deporte.deportes_info[nombre_deporte][campo] = texto

    deporte.guardar_deportes(deporte.deportes_info)
    admin_deporte_estado.pop(user_id, None)
    context.user_data.pop("deporte_modificar", None)
    context.user_data.pop("campo_modificar", None)

    await update.message.reply_text(
        f"✅ Campo <b>{campo}</b> del deporte <b>{nombre_deporte}</b> modificado exitosamente.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Volver al menú", callback_data="admin_menu_deportes")]
        ])
    )


@solo_admins
async def manejar_respuesta_agregar_deporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja las respuestas durante la adición de un nuevo deporte"""
    user_id = str(update.effective_user.id)
    
    if user_id not in admin_deporte_estado:
        return

    estado_info = admin_deporte_estado[user_id]
    
    if estado_info.get("accion") != "agregar":
        return

    texto = update.message.text.strip()
    estado_actual = estado_info.get("estado")

    if estado_actual == "esperando_nombre":
        context.user_data["nombre"] = texto
        admin_deporte_estado[user_id]["estado"] = "esperando_profesor"
        await update.message.reply_text("👨‍🏫 Inserta el nombre del profesor que imparte este deporte:")

    elif estado_actual == "esperando_profesor":
        context.user_data["profesor"] = texto
        admin_deporte_estado[user_id]["estado"] = "esperando_contacto"
        await update.message.reply_text("📞 ¿Cuál es el contacto del profesor?")

    elif estado_actual == "esperando_contacto":
        context.user_data["contacto"] = texto
        admin_deporte_estado[user_id]["estado"] = "esperando_dias"
        await update.message.reply_text("📅 ¿Qué días se imparten las clases?")

    elif estado_actual == "esperando_dias":
        context.user_data["dias"] = texto
        admin_deporte_estado[user_id]["estado"] = "esperando_horarios"
        await update.message.reply_text("⏰ ¿En qué horarios se imparten?")

    elif estado_actual == "esperando_horarios":
        context.user_data["horario"] = texto
        admin_deporte_estado[user_id]["estado"] = "esperando_lugar"
        await update.message.reply_text("📍 ¿Dónde se imparten las clases? (puedes poner varios separados por coma)")

    elif estado_actual == "esperando_lugar":
        lugares = [l.strip() for l in texto.split(",")]
        context.user_data["lugar"] = lugares
        admin_deporte_estado[user_id]["estado"] = "confirmacion"

        resumen = (
            f"⚽️ *Resumen del nuevo deporte:*\n\n"
            f"*Nombre:* {context.user_data['nombre']}\n"
            f"*Profesor:* {context.user_data['profesor']}\n"
            f"*Contacto:* {context.user_data['contacto']}\n"
            f"*Días:* {context.user_data['dias']}\n"
            f"*Horario:* {context.user_data['horario']}\n"
            f"*Lugar:* {', '.join(lugares)}\n\n"
            "¿Quieres confirmar y guardar este deporte? ✅"
        )

        teclado_confirmacion = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Confirmar", callback_data="admin_confirmar_agregar_deporte"),
                InlineKeyboardButton("❌ Cancelar", callback_data="admin_cancelar_agregar_deporte")
            ]
        ])

        await update.message.reply_text(resumen, reply_markup=teclado_confirmacion, parse_mode="Markdown")


@solo_admins
async def confirmar_agregar_deporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Confirma y guarda el nuevo deporte"""
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)
    
    if user_id not in admin_deporte_estado:
        await query.answer("Error: No hay operación en curso", show_alert=True)
        return

    deporte.guardar_deporte_completo(context)
    admin_deporte_estado.pop(user_id, None)

    await query.edit_message_text(
        "✅ *¡Deporte agregado exitosamente!*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Volver al menú", callback_data="admin_menu_deportes")]
        ])
    )


@solo_admins
async def cancelar_agregar_deporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancela la adición de un nuevo deporte"""
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)
    admin_deporte_estado.pop(user_id, None)
    context.user_data.clear()

    await query.edit_message_text(
        "❌ Operación cancelada. No se guardó ningún dato.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Volver al menú", callback_data="admin_menu_deportes")]
        ])
    )

