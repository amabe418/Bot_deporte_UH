
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown
from admin import solo_admins
import profesores

# Estados para operaciones de admin
admin_profesor_estado = {}


def generar_teclado_profesores_admin(pagina: int, elementos_por_pagina: int = 5, accion="modificar"):
    """Genera teclado de profesores para admin con paginación"""
    profesores_lista = list(profesores.profesores_info.keys())
    total_paginas = (len(profesores_lista) + elementos_por_pagina - 1) // elementos_por_pagina

    inicio = pagina * elementos_por_pagina
    fin = inicio + elementos_por_pagina
    profesores_pagina = profesores_lista[inicio:fin]

    botones = [
        [InlineKeyboardButton(nombre, callback_data=f"admin_{accion}_profesor_{nombre}")]
        for nombre in profesores_pagina
    ]

    botones_navegacion = []
    if pagina > 0:
        botones_navegacion.append(InlineKeyboardButton("⬅️ Anterior", callback_data=f"admin_pagina_{accion}_profesores_{pagina - 1}"))
    if pagina < total_paginas - 1:
        botones_navegacion.append(InlineKeyboardButton("Siguiente ➡️", callback_data=f"admin_pagina_{accion}_profesores_{pagina + 1}"))

    if botones_navegacion:
        botones.append(botones_navegacion)
    
    botones.append([InlineKeyboardButton("🔙 Volver", callback_data="admin_menu_profesores")])

    return InlineKeyboardMarkup(botones)


@solo_admins
async def agregar_profesor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia el flujo para agregar un nuevo profesor"""
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)
    admin_profesor_estado[user_id] = {"accion": "agregar", "estado": "esperando_nombre"}
    context.user_data.clear()

    await query.edit_message_text("📝 ¿Cuál es el nombre del nuevo profesor?")


@solo_admins
async def listar_profesores_para_modificar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lista profesores para seleccionar cuál modificar"""
    query = update.callback_query
    await query.answer()

    if not profesores.profesores_info:
        await query.edit_message_text(
            "❌ No hay profesores registrados.\n\n🔙 Volver al menú de profesores.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Volver", callback_data="admin_menu_profesores")]
            ])
        )
        return

    reply_markup = generar_teclado_profesores_admin(pagina=0, accion="modificar")
    await query.edit_message_text(
        "✏️ Selecciona el profesor que deseas modificar:",
        reply_markup=reply_markup
    )


@solo_admins
async def listar_profesores_para_eliminar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lista profesores para seleccionar cuál eliminar"""
    query = update.callback_query
    await query.answer()

    if not profesores.profesores_info:
        await query.edit_message_text(
            "❌ No hay profesores registrados.\n\n🔙 Volver al menú de profesores.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Volver", callback_data="admin_menu_profesores")]
            ])
        )
        return

    reply_markup = generar_teclado_profesores_admin(pagina=0, accion="eliminar")
    await query.edit_message_text(
        "🗑️ Selecciona el profesor que deseas eliminar:",
        reply_markup=reply_markup
    )


@solo_admins
async def listar_profesores_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lista todos los profesores con opciones de edición"""
    query = update.callback_query
    await query.answer()

    if not profesores.profesores_info:
        await query.edit_message_text(
            "❌ No hay profesores registrados.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Volver", callback_data="admin_menu_profesores")]
            ])
        )
        return

    reply_markup = generar_teclado_profesores_admin(pagina=0, accion="ver")
    await query.edit_message_text(
        "📋 Selecciona un profesor para ver detalles:",
        reply_markup=reply_markup
    )


@solo_admins
async def seleccionar_campo_modificar_profesor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra los campos que se pueden modificar de un profesor"""
    query = update.callback_query
    await query.answer()

    # Extraer nombre del profesor del callback_data
    partes = query.data.split("_profesor_", 1)
    if len(partes) < 2:
        await query.answer("Error al procesar la solicitud", show_alert=True)
        return

    nombre_profesor = partes[1]
    info = profesores.profesores_info.get(nombre_profesor)

    if not info:
        await query.answer("Profesor no encontrado", show_alert=True)
        return

    user_id = str(query.from_user.id)
    admin_profesor_estado[user_id] = {
        "accion": "modificar",
        "profesor": nombre_profesor,
        "estado": "seleccionando_campo"
    }
    context.user_data["profesor_modificar"] = nombre_profesor

    deportes_str = ', '.join(info.get("deportes", []))
    lugares_str = ', '.join(info.get("lugares", [])) if isinstance(info.get("lugares"), list) else info.get("lugares", "No disponible")

    mensaje = f"✏️ <b>Modificar Profesor: {nombre_profesor}</b>\n\n"
    mensaje += f"📋 <b>Información actual:</b>\n"
    mensaje += f"🏅 Deportes: {deportes_str}\n"
    mensaje += f"📞 Contacto: {info.get('contacto', 'No disponible')}\n"
    mensaje += f"🕒 Horarios: {info.get('horarios', 'No disponible')}\n"
    mensaje += f"📍 Lugares: {lugares_str}\n"
    mensaje += f"📷 Foto: {'Sí' if info.get('foto') or info.get('foto_url') else 'No'}\n\n"
    mensaje += "¿Qué campo deseas modificar?"

    keyboard = [
        [InlineKeyboardButton("📝 Nombre", callback_data=f"admin_modificar_campo_profesor_{nombre_profesor}_nombre")],
        [InlineKeyboardButton("🏅 Deportes", callback_data=f"admin_modificar_campo_profesor_{nombre_profesor}_deportes")],
        [InlineKeyboardButton("📞 Contacto", callback_data=f"admin_modificar_campo_profesor_{nombre_profesor}_contacto")],
        [InlineKeyboardButton("🕒 Horarios", callback_data=f"admin_modificar_campo_profesor_{nombre_profesor}_horarios")],
        [InlineKeyboardButton("📍 Lugares", callback_data=f"admin_modificar_campo_profesor_{nombre_profesor}_lugares")],
        [InlineKeyboardButton("📷 Foto", callback_data=f"admin_modificar_campo_profesor_{nombre_profesor}_foto")],
        [InlineKeyboardButton("🔙 Volver", callback_data="admin_menu_profesores")]
    ]

    await query.edit_message_text(mensaje, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))


@solo_admins
async def iniciar_modificacion_campo_profesor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia la modificación de un campo específico"""
    query = update.callback_query
    await query.answer()

    # Formato: admin_modificar_campo_profesor_NOMBRE_CAMPO
    partes = query.data.split("_profesor_", 1)
    if len(partes) < 2:
        await query.answer("Error al procesar", show_alert=True)
        return

    resto = partes[1]
    campos_posibles = ["nombre", "deportes", "contacto", "horarios", "lugares", "foto"]
    campo = None
    nombre_profesor = None
    
    for campo_posible in campos_posibles:
        if resto.endswith(f"_{campo_posible}"):
            campo = campo_posible
            nombre_profesor = resto[:-len(f"_{campo_posible}")]
            break
    
    if not campo:
        await query.answer("Error: Campo no reconocido", show_alert=True)
        return

    user_id = str(query.from_user.id)
    admin_profesor_estado[user_id] = {
        "accion": "modificar",
        "profesor": nombre_profesor,
        "campo": campo,
        "estado": f"esperando_nuevo_{campo}"
    }
    context.user_data["profesor_modificar"] = nombre_profesor
    context.user_data["campo_modificar"] = campo

    campo_nombres = {
        "nombre": "nombre del profesor",
        "deportes": "deportes que imparte (separados por coma)",
        "contacto": "contacto del profesor",
        "horarios": "horarios",
        "lugares": "lugares (separados por coma)",
        "foto": "foto del profesor"
    }

    nombre_campo = campo_nombres.get(campo, campo)
    if campo == "foto":
        await query.edit_message_text("📷 Por favor, envía la foto del profesor directamente al bot. Si no quieres cambiar la foto, envía 'no'.")
    else:
        await query.edit_message_text(f"📝 Ingresa el nuevo {nombre_campo}:")


@solo_admins
async def confirmar_eliminar_profesor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Confirma la eliminación de un profesor"""
    query = update.callback_query
    await query.answer()

    # Extraer nombre del profesor
    partes = query.data.split("_profesor_", 1)
    if len(partes) < 2:
        await query.answer("Error al procesar", show_alert=True)
        return

    nombre_profesor = partes[1]
    info = profesores.profesores_info.get(nombre_profesor)

    if not info:
        await query.answer("Profesor no encontrado", show_alert=True)
        return

    user_id = str(query.from_user.id)
    admin_profesor_estado[user_id] = {
        "accion": "eliminar",
        "profesor": nombre_profesor,
        "estado": "confirmando"
    }
    context.user_data["profesor_eliminar"] = nombre_profesor

    mensaje = f"⚠️ <b>Confirmar eliminación</b>\n\n"
    mensaje += f"¿Estás seguro de que deseas eliminar al profesor:\n<b>{nombre_profesor}</b>?\n\n"
    mensaje += "Esta acción no se puede deshacer."

    keyboard = [
        [
            InlineKeyboardButton("✅ Sí, eliminar", callback_data=f"admin_confirmar_eliminar_profesor_{nombre_profesor}"),
            InlineKeyboardButton("❌ Cancelar", callback_data="admin_menu_profesores")
        ]
    ]

    await query.edit_message_text(mensaje, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))


@solo_admins
async def ejecutar_eliminar_profesor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ejecuta la eliminación del profesor"""
    query = update.callback_query
    await query.answer()

    partes = query.data.split("_profesor_", 1)
    if len(partes) < 2:
        await query.answer("Error al procesar", show_alert=True)
        return

    nombre_profesor = partes[1]

    if nombre_profesor in profesores.profesores_info:
        del profesores.profesores_info[nombre_profesor]
        profesores.guardar_profesores(profesores.profesores_info)
        
        user_id = str(query.from_user.id)
        admin_profesor_estado.pop(user_id, None)
        context.user_data.pop("profesor_eliminar", None)

        await query.edit_message_text(
            f"✅ Profesor <b>{nombre_profesor}</b> eliminado exitosamente.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Volver al menú", callback_data="admin_menu_profesores")]
            ])
        )
    else:
        await query.answer("Profesor no encontrado", show_alert=True)


@solo_admins
async def ver_profesor_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra los detalles de un profesor con opciones de edición"""
    query = update.callback_query
    await query.answer()

    partes = query.data.split("_profesor_", 1)
    if len(partes) < 2:
        await query.answer("Error", show_alert=True)
        return

    nombre_profesor = partes[1]
    info = profesores.profesores_info.get(nombre_profesor)

    if not info:
        await query.answer("Profesor no encontrado", show_alert=True)
        return

    deportes_str = ', '.join(info.get("deportes", []))
    lugares_str = ', '.join(info.get("lugares", [])) if isinstance(info.get("lugares"), list) else info.get("lugares", "No disponible")

    mensaje = f"👨‍🏫 <b>{nombre_profesor}</b>\n\n"
    mensaje += f"🏅 <b>Deportes:</b> {deportes_str}\n"
    mensaje += f"📞 <b>Contacto:</b> {info.get('contacto', 'No disponible')}\n"
    mensaje += f"🕒 <b>Horarios:</b> {info.get('horarios', 'No disponible')}\n"
    mensaje += f"📍 <b>Lugares:</b> {lugares_str}\n"
    mensaje += f"📷 <b>Foto:</b> {'Sí' if info.get('foto') or info.get('foto_url') else 'No'}"

    keyboard = [
        [
            InlineKeyboardButton("✏️ Modificar", callback_data=f"admin_modificar_profesor_{nombre_profesor}"),
            InlineKeyboardButton("🗑️ Eliminar", callback_data=f"admin_eliminar_profesor_{nombre_profesor}")
        ],
        [InlineKeyboardButton("🔙 Volver", callback_data="admin_listar_profesores")]
    ]

    await query.edit_message_text(mensaje, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))


async def cambiar_pagina_profesores_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cambia la página en la lista de profesores del admin"""
    query = update.callback_query
    await query.answer()

    partes = query.data.split("_profesores_", 1)
    if len(partes) < 2:
        await query.answer("Error", show_alert=True)
        return

    pagina = int(partes[1])
    prefijo = partes[0]
    accion = prefijo.split("_")[-1] if "_" in prefijo else "ver"

    context.user_data['pagina_profesores_admin'] = pagina

    reply_markup = generar_teclado_profesores_admin(pagina=pagina, accion=accion)

    mensajes = {
        "modificar": "✏️ Selecciona el profesor que deseas modificar:",
        "eliminar": "🗑️ Selecciona el profesor que deseas eliminar:",
        "ver": "📋 Selecciona un profesor para ver detalles:"
    }

    await query.edit_message_text(
        text=mensajes.get(accion, "Selecciona un profesor:"),
        reply_markup=reply_markup
    )


@solo_admins
async def manejar_foto_profesor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja cuando se envía una foto para un profesor"""
    user_id = str(update.effective_user.id)
    
    if user_id not in admin_profesor_estado:
        return
    
    estado_info = admin_profesor_estado[user_id]
    
    # Verificar si hay foto en el mensaje
    if not update.message.photo:
        await update.message.reply_text("⚠️ Por favor, envía una foto o escribe 'no' si no tienes foto.")
        return
    
    # Obtener el file_id de la foto más grande (última en la lista)
    foto_file_id = update.message.photo[-1].file_id
    
    if estado_info.get("accion") == "agregar":
        # Agregar profesor
        if estado_info.get("estado") == "esperando_foto":
            context.user_data["foto"] = foto_file_id
            admin_profesor_estado[user_id]["estado"] = "confirmacion"
            
            deportes_str = ', '.join(context.user_data.get("deportes", []))
            lugares_str = ', '.join(context.user_data.get("lugar", []))
            
            resumen = (
                f"👨‍🏫 *Resumen del nuevo profesor:*\n\n"
                f"*Nombre:* {context.user_data['nombre']}\n"
                f"*Deportes:* {deportes_str}\n"
                f"*Contacto:* {context.user_data['contacto']}\n"
                f"*Horario:* {context.user_data['horario']}\n"
                f"*Lugar:* {lugares_str}\n"
                f"*Foto:* Sí (recibida)\n\n"
                "¿Quieres confirmar y guardar este profesor? ✅"
            )
            
            teclado_confirmacion = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✅ Confirmar", callback_data="admin_confirmar_agregar_profesor"),
                    InlineKeyboardButton("❌ Cancelar", callback_data="admin_cancelar_agregar_profesor")
                ]
            ])
            
            await update.message.reply_text(resumen, reply_markup=teclado_confirmacion, parse_mode="Markdown")
            
    elif estado_info.get("accion") == "modificar":
        # Modificar profesor
        nombre_profesor = estado_info.get("profesor")
        campo = estado_info.get("campo")
        
        if campo == "foto" and nombre_profesor in profesores.profesores_info:
            profesores.profesores_info[nombre_profesor]["foto"] = foto_file_id
            profesores.guardar_profesores(profesores.profesores_info)
            admin_profesor_estado.pop(user_id, None)
            context.user_data.pop("profesor_modificar", None)
            context.user_data.pop("campo_modificar", None)
            
            await update.message.reply_text(
                f"✅ Foto del profesor <b>{nombre_profesor}</b> actualizada exitosamente.",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 Volver al menú", callback_data="admin_menu_profesores")]
                ])
            )


@solo_admins
async def manejar_respuesta_modificacion_profesor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja las respuestas durante la modificación de un profesor"""
    user_id = str(update.effective_user.id)
    
    if user_id not in admin_profesor_estado:
        return

    estado_info = admin_profesor_estado[user_id]
    
    if estado_info.get("accion") != "modificar":
        return

    texto = update.message.text.strip()
    nombre_profesor = estado_info.get("profesor")
    campo = estado_info.get("campo")

    if nombre_profesor not in profesores.profesores_info:
        await update.message.reply_text("❌ Error: Profesor no encontrado.")
        admin_profesor_estado.pop(user_id, None)
        return

    # Aplicar la modificación
    if campo == "nombre":
        nuevo_nombre = texto
        if nuevo_nombre != nombre_profesor:
            profesores.profesores_info[nuevo_nombre] = profesores.profesores_info[nombre_profesor].copy()
            del profesores.profesores_info[nombre_profesor]
            nombre_profesor = nuevo_nombre
    elif campo == "deportes":
        deportes = [d.strip() for d in texto.split(",")]
        profesores.profesores_info[nombre_profesor][campo] = deportes
    elif campo == "lugares":
        lugares = [l.strip() for l in texto.split(",")]
        profesores.profesores_info[nombre_profesor][campo] = lugares
    elif campo == "foto":
        # Esta función solo maneja texto, las fotos se manejan en otra función
        if texto.lower() == "no":
            # No cambiar la foto, continuar
            profesores.guardar_profesores(profesores.profesores_info)
            admin_profesor_estado.pop(user_id, None)
            context.user_data.pop("profesor_modificar", None)
            context.user_data.pop("campo_modificar", None)
            await update.message.reply_text(
                f"✅ No se cambió la foto del profesor <b>{nombre_profesor}</b>.",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 Volver al menú", callback_data="admin_menu_profesores")]
                ])
            )
            return
        else:
            await update.message.reply_text("⚠️ Por favor, envía la foto directamente al bot (no una URL). Si no quieres cambiar la foto, envía 'no'.")
            return
    else:
        profesores.profesores_info[nombre_profesor][campo] = texto

    profesores.guardar_profesores(profesores.profesores_info)
    admin_profesor_estado.pop(user_id, None)
    context.user_data.pop("profesor_modificar", None)
    context.user_data.pop("campo_modificar", None)

    await update.message.reply_text(
        f"✅ Campo <b>{campo}</b> del profesor <b>{nombre_profesor}</b> modificado exitosamente.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Volver al menú", callback_data="admin_menu_profesores")]
        ])
    )


@solo_admins
async def manejar_respuesta_agregar_profesor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja las respuestas durante la adición de un nuevo profesor"""
    user_id = str(update.effective_user.id)
    
    if user_id not in admin_profesor_estado:
        return

    estado_info = admin_profesor_estado[user_id]
    
    if estado_info.get("accion") != "agregar":
        return

    texto = update.message.text.strip()
    estado_actual = estado_info.get("estado")

    if estado_actual == "esperando_nombre":
        context.user_data["nombre"] = texto
        admin_profesor_estado[user_id]["estado"] = "esperando_deportes"
        await update.message.reply_text("🏅 Indica los deportes que imparte (separa con coma si hay más de uno):")

    elif estado_actual == "esperando_deportes":
        deportes = [d.strip() for d in texto.split(",")]
        context.user_data["deportes"] = deportes
        admin_profesor_estado[user_id]["estado"] = "esperando_contacto"
        await update.message.reply_text("📞 ¿Cuál es el contacto del profesor?")

    elif estado_actual == "esperando_contacto":
        context.user_data["contacto"] = texto
        admin_profesor_estado[user_id]["estado"] = "esperando_horarios"
        await update.message.reply_text("📅 ¿Qué días se imparten las clases?")

    elif estado_actual == "esperando_horarios":
        context.user_data["horario"] = texto
        admin_profesor_estado[user_id]["estado"] = "esperando_lugar"
        await update.message.reply_text("📍 ¿Dónde se imparten las clases? (puedes poner varios separados por coma)")

    elif estado_actual == "esperando_lugar":
        lugares = [l.strip() for l in texto.split(",")]
        context.user_data["lugar"] = lugares
        admin_profesor_estado[user_id]["estado"] = "esperando_foto"
        await update.message.reply_text("📷 Por favor, envía la foto del profesor directamente al bot. Si no tienes foto, envía 'no'.")

    elif estado_actual == "esperando_foto":
        # Esta función solo maneja texto, las fotos se manejan en otra función
        if texto.lower() == "no":
            admin_profesor_estado[user_id]["estado"] = "confirmacion"

        deportes_str = ', '.join(context.user_data.get("deportes", []))
        lugares_str = ', '.join(context.user_data.get("lugar", []))

        resumen = (
            f"👨‍🏫 *Resumen del nuevo profesor:*\n\n"
            f"*Nombre:* {context.user_data['nombre']}\n"
            f"*Deportes:* {deportes_str}\n"
            f"*Contacto:* {context.user_data['contacto']}\n"
            f"*Horario:* {context.user_data['horario']}\n"
            f"*Lugar:* {lugares_str}\n"
            f"*Foto:* {context.user_data.get('foto', 'No')}\n\n"
            "¿Quieres confirmar y guardar este profesor? ✅"
        )

        teclado_confirmacion = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Confirmar", callback_data="admin_confirmar_agregar_profesor"),
                InlineKeyboardButton("❌ Cancelar", callback_data="admin_cancelar_agregar_profesor")
            ]
        ])

        await update.message.reply_text(resumen, reply_markup=teclado_confirmacion, parse_mode="Markdown")


@solo_admins
async def confirmar_agregar_profesor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Confirma y guarda el nuevo profesor"""
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)
    
    if user_id not in admin_profesor_estado:
        await query.answer("Error: No hay operación en curso", show_alert=True)
        return

    nombre = context.user_data.get("nombre", "").strip()
    if not nombre:
        await query.answer("Error: Nombre no válido", show_alert=True)
        return

    profesores.profesores_info[nombre] = {
        "deportes": context.user_data.get("deportes", []),
        "contacto": context.user_data.get("contacto", "No disponible"),
        "horarios": context.user_data.get("horario", "Sin horario"),
        "lugares": context.user_data.get("lugar", []),
        "foto": context.user_data.get("foto", None)
    }

    profesores.guardar_profesores(profesores.profesores_info)
    admin_profesor_estado.pop(user_id, None)
    context.user_data.clear()

    await query.edit_message_text(
        "✅ *¡Profesor agregado exitosamente!*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Volver al menú", callback_data="admin_menu_profesores")]
        ])
    )


@solo_admins
async def cancelar_agregar_profesor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancela la adición de un nuevo profesor"""
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)
    admin_profesor_estado.pop(user_id, None)
    context.user_data.clear()

    await query.edit_message_text(
        "❌ Operación cancelada. No se guardó ningún dato.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Volver al menú", callback_data="admin_menu_profesores")]
        ])
    )

