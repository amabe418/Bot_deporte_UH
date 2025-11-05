
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown
from admin import solo_admins
import instalaciones

# Estados para operaciones de admin
admin_instalacion_estado = {}


def generar_teclado_instalaciones_admin(pagina: int, elementos_por_pagina: int = 5, accion="modificar"):
    """Genera teclado de instalaciones para admin con paginación"""
    instalaciones_lista = list(instalaciones.instalaciones_info.keys())
    total_paginas = (len(instalaciones_lista) + elementos_por_pagina - 1) // elementos_por_pagina

    inicio = pagina * elementos_por_pagina
    fin = inicio + elementos_por_pagina
    instalaciones_pagina = instalaciones_lista[inicio:fin]

    botones = [
        [InlineKeyboardButton(nombre, callback_data=f"admin_{accion}_instalacion_{nombre}")]
        for nombre in instalaciones_pagina
    ]

    botones_navegacion = []
    if pagina > 0:
        botones_navegacion.append(InlineKeyboardButton("⬅️ Anterior", callback_data=f"admin_pagina_{accion}_instalaciones_{pagina - 1}"))
    if pagina < total_paginas - 1:
        botones_navegacion.append(InlineKeyboardButton("Siguiente ➡️", callback_data=f"admin_pagina_{accion}_instalaciones_{pagina + 1}"))

    if botones_navegacion:
        botones.append(botones_navegacion)
    
    botones.append([InlineKeyboardButton("🔙 Volver", callback_data="admin_menu_instalaciones")])

    return InlineKeyboardMarkup(botones)


@solo_admins
async def agregar_instalacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia el flujo para agregar una nueva instalación"""
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)
    admin_instalacion_estado[user_id] = {"accion": "agregar", "estado": "esperando_nombre"}
    context.user_data.clear()

    await query.edit_message_text("📝 ¿Cuál es el nombre de la nueva instalación?")


@solo_admins
async def listar_instalaciones_para_modificar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lista instalaciones para seleccionar cuál modificar"""
    query = update.callback_query
    await query.answer()

    if not instalaciones.instalaciones_info:
        await query.edit_message_text(
            "❌ No hay instalaciones registradas.\n\n🔙 Volver al menú de instalaciones.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Volver", callback_data="admin_menu_instalaciones")]
            ])
        )
        return

    reply_markup = generar_teclado_instalaciones_admin(pagina=0, accion="modificar")
    await query.edit_message_text(
        "✏️ Selecciona la instalación que deseas modificar:",
        reply_markup=reply_markup
    )


@solo_admins
async def listar_instalaciones_para_eliminar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lista instalaciones para seleccionar cuál eliminar"""
    query = update.callback_query
    await query.answer()

    if not instalaciones.instalaciones_info:
        await query.edit_message_text(
            "❌ No hay instalaciones registradas.\n\n🔙 Volver al menú de instalaciones.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Volver", callback_data="admin_menu_instalaciones")]
            ])
        )
        return

    reply_markup = generar_teclado_instalaciones_admin(pagina=0, accion="eliminar")
    await query.edit_message_text(
        "🗑️ Selecciona la instalación que deseas eliminar:",
        reply_markup=reply_markup
    )


@solo_admins
async def listar_instalaciones_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lista todas las instalaciones con opciones de edición"""
    query = update.callback_query
    await query.answer()

    if not instalaciones.instalaciones_info:
        await query.edit_message_text(
            "❌ No hay instalaciones registradas.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Volver", callback_data="admin_menu_instalaciones")]
            ])
        )
        return

    reply_markup = generar_teclado_instalaciones_admin(pagina=0, accion="ver")
    await query.edit_message_text(
        "📋 Selecciona una instalación para ver detalles:",
        reply_markup=reply_markup
    )


@solo_admins
async def seleccionar_campo_modificar_instalacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra los campos que se pueden modificar de una instalación"""
    query = update.callback_query
    await query.answer()

    # Extraer nombre de la instalación del callback_data
    partes = query.data.split("_instalacion_", 1)
    if len(partes) < 2:
        await query.answer("Error al procesar la solicitud", show_alert=True)
        return

    nombre_instalacion = partes[1]
    info = instalaciones.instalaciones_info.get(nombre_instalacion)

    if not info:
        await query.answer("Instalación no encontrada", show_alert=True)
        return

    user_id = str(query.from_user.id)
    admin_instalacion_estado[user_id] = {
        "accion": "modificar",
        "instalacion": nombre_instalacion,
        "estado": "seleccionando_campo"
    }
    context.user_data["instalacion_modificar"] = nombre_instalacion

    latitud = info.get("latitud")
    longitud = info.get("longitud")
    coordenadas_str = f"{latitud}, {longitud}" if latitud and longitud else "No definidas"

    mensaje = f"✏️ <b>Modificar Instalación: {nombre_instalacion}</b>\n\n"
    mensaje += f"📋 <b>Información actual:</b>\n"
    mensaje += f"📍 Dirección: {info.get('direccion', 'No disponible')}\n"
    mensaje += f"🗺️ Coordenadas: {coordenadas_str}\n"
    mensaje += f"📷 Foto: {'Sí' if info.get('foto') or info.get('foto_url') else 'No'}\n\n"
    mensaje += "¿Qué campo deseas modificar?"

    keyboard = [
        [InlineKeyboardButton("📝 Nombre", callback_data=f"admin_modificar_campo_instalacion_{nombre_instalacion}_nombre")],
        [InlineKeyboardButton("📍 Dirección", callback_data=f"admin_modificar_campo_instalacion_{nombre_instalacion}_direccion")],
        [InlineKeyboardButton("🗺️ Coordenadas", callback_data=f"admin_modificar_campo_instalacion_{nombre_instalacion}_coordenadas")],
        [InlineKeyboardButton("📷 Foto", callback_data=f"admin_modificar_campo_instalacion_{nombre_instalacion}_foto")],
        [InlineKeyboardButton("🔙 Volver", callback_data="admin_menu_instalaciones")]
    ]

    await query.edit_message_text(mensaje, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))


@solo_admins
async def iniciar_modificacion_campo_instalacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia la modificación de un campo específico"""
    query = update.callback_query
    await query.answer()

    # Formato: admin_modificar_campo_instalacion_NOMBRE_CAMPO
    partes = query.data.split("_instalacion_", 1)
    if len(partes) < 2:
        await query.answer("Error al procesar", show_alert=True)
        return

    resto = partes[1]
    campos_posibles = ["nombre", "direccion", "coordenadas", "foto"]
    campo = None
    nombre_instalacion = None
    
    for campo_posible in campos_posibles:
        if resto.endswith(f"_{campo_posible}"):
            campo = campo_posible
            nombre_instalacion = resto[:-len(f"_{campo_posible}")]
            break
    
    if not campo:
        await query.answer("Error: Campo no reconocido", show_alert=True)
        return

    user_id = str(query.from_user.id)
    admin_instalacion_estado[user_id] = {
        "accion": "modificar",
        "instalacion": nombre_instalacion,
        "campo": campo,
        "estado": f"esperando_nuevo_{campo}"
    }
    context.user_data["instalacion_modificar"] = nombre_instalacion
    context.user_data["campo_modificar"] = campo

    campo_nombres = {
        "nombre": "nombre de la instalación",
        "direccion": "dirección de la instalación",
        "coordenadas": "coordenadas (formato: latitud,longitud)",
        "foto": "foto de la instalación"
    }

    nombre_campo = campo_nombres.get(campo, campo)
    
    if campo == "coordenadas":
        await query.edit_message_text(f"🗺️ Ingresa las nuevas coordenadas en formato: <b>latitud,longitud</b>\n\nEjemplo: 23.1363,-82.3782", parse_mode="HTML")
    elif campo == "foto":
        await query.edit_message_text("📷 Por favor, envía la foto de la instalación directamente al bot. Si no quieres cambiar la foto, envía 'no'.")
    else:
        await query.edit_message_text(f"📝 Ingresa el nuevo {nombre_campo}:")


@solo_admins
async def confirmar_eliminar_instalacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Confirma la eliminación de una instalación"""
    query = update.callback_query
    await query.answer()

    # Extraer nombre de la instalación
    partes = query.data.split("_instalacion_", 1)
    if len(partes) < 2:
        await query.answer("Error al procesar", show_alert=True)
        return

    nombre_instalacion = partes[1]
    info = instalaciones.instalaciones_info.get(nombre_instalacion)

    if not info:
        await query.answer("Instalación no encontrada", show_alert=True)
        return

    user_id = str(query.from_user.id)
    admin_instalacion_estado[user_id] = {
        "accion": "eliminar",
        "instalacion": nombre_instalacion,
        "estado": "confirmando"
    }
    context.user_data["instalacion_eliminar"] = nombre_instalacion

    mensaje = f"⚠️ <b>Confirmar eliminación</b>\n\n"
    mensaje += f"¿Estás seguro de que deseas eliminar la instalación:\n<b>{nombre_instalacion}</b>?\n\n"
    mensaje += "Esta acción no se puede deshacer."

    keyboard = [
        [
            InlineKeyboardButton("✅ Sí, eliminar", callback_data=f"admin_confirmar_eliminar_instalacion_{nombre_instalacion}"),
            InlineKeyboardButton("❌ Cancelar", callback_data="admin_menu_instalaciones")
        ]
    ]

    await query.edit_message_text(mensaje, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))


@solo_admins
async def ejecutar_eliminar_instalacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ejecuta la eliminación de la instalación"""
    query = update.callback_query
    await query.answer()

    partes = query.data.split("_instalacion_", 1)
    if len(partes) < 2:
        await query.answer("Error al procesar", show_alert=True)
        return

    nombre_instalacion = partes[1]

    if nombre_instalacion in instalaciones.instalaciones_info:
        del instalaciones.instalaciones_info[nombre_instalacion]
        instalaciones.guardar_instalaciones(instalaciones.instalaciones_info)
        
        user_id = str(query.from_user.id)
        admin_instalacion_estado.pop(user_id, None)
        context.user_data.pop("instalacion_eliminar", None)

        await query.edit_message_text(
            f"✅ Instalación <b>{nombre_instalacion}</b> eliminada exitosamente.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Volver al menú", callback_data="admin_menu_instalaciones")]
            ])
        )
    else:
        await query.answer("Instalación no encontrada", show_alert=True)


@solo_admins
async def ver_instalacion_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra los detalles de una instalación con opciones de edición"""
    query = update.callback_query
    await query.answer()

    partes = query.data.split("_instalacion_", 1)
    if len(partes) < 2:
        await query.answer("Error", show_alert=True)
        return

    nombre_instalacion = partes[1]
    info = instalaciones.instalaciones_info.get(nombre_instalacion)

    if not info:
        await query.answer("Instalación no encontrada", show_alert=True)
        return

    latitud = info.get("latitud")
    longitud = info.get("longitud")
    coordenadas_str = f"{latitud}, {longitud}" if latitud and longitud else "No definidas"

    mensaje = f"🏟️ <b>{nombre_instalacion}</b>\n\n"
    mensaje += f"📍 <b>Dirección:</b> {info.get('direccion', 'No disponible')}\n"
    mensaje += f"🗺️ <b>Coordenadas:</b> {coordenadas_str}\n"
    mensaje += f"📷 <b>Foto:</b> {'Sí' if info.get('foto') or info.get('foto_url') else 'No'}"

    keyboard = [
        [
            InlineKeyboardButton("✏️ Modificar", callback_data=f"admin_modificar_instalacion_{nombre_instalacion}"),
            InlineKeyboardButton("🗑️ Eliminar", callback_data=f"admin_eliminar_instalacion_{nombre_instalacion}")
        ],
        [InlineKeyboardButton("🔙 Volver", callback_data="admin_listar_instalaciones")]
    ]

    await query.edit_message_text(mensaje, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))


async def cambiar_pagina_instalaciones_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cambia la página en la lista de instalaciones del admin"""
    query = update.callback_query
    await query.answer()

    partes = query.data.split("_instalaciones_", 1)
    if len(partes) < 2:
        await query.answer("Error", show_alert=True)
        return

    pagina = int(partes[1])
    prefijo = partes[0]
    accion = prefijo.split("_")[-1] if "_" in prefijo else "ver"

    context.user_data['pagina_instalaciones_admin'] = pagina

    reply_markup = generar_teclado_instalaciones_admin(pagina=pagina, accion=accion)

    mensajes = {
        "modificar": "✏️ Selecciona la instalación que deseas modificar:",
        "eliminar": "🗑️ Selecciona la instalación que deseas eliminar:",
        "ver": "📋 Selecciona una instalación para ver detalles:"
    }

    await query.edit_message_text(
        text=mensajes.get(accion, "Selecciona una instalación:"),
        reply_markup=reply_markup
    )


@solo_admins
async def manejar_foto_instalacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja cuando se envía una foto para una instalación"""
    user_id = str(update.effective_user.id)
    
    if user_id not in admin_instalacion_estado:
        return
    
    estado_info = admin_instalacion_estado[user_id]
    
    # Verificar si hay foto en el mensaje
    if not update.message.photo:
        await update.message.reply_text("⚠️ Por favor, envía una foto o escribe 'no' si no tienes foto.")
        return
    
    # Obtener el file_id de la foto más grande (última en la lista)
    foto_file_id = update.message.photo[-1].file_id
    
    if estado_info.get("accion") == "agregar":
        # Agregar instalación
        if estado_info.get("estado") == "esperando_foto":
            context.user_data["foto"] = foto_file_id
            admin_instalacion_estado[user_id]["estado"] = "confirmacion"
            
            coordenadas_str = f"{context.user_data.get('latitud')}, {context.user_data.get('longitud')}" if context.user_data.get('latitud') else "No definidas"
            
            resumen = (
                f"🏟️ *Resumen de la nueva instalación:*\n\n"
                f"*Nombre:* {context.user_data['nombre']}\n"
                f"*Dirección:* {context.user_data['direccion']}\n"
                f"*Coordenadas:* {coordenadas_str}\n"
                f"*Foto:* Sí (recibida)\n\n"
                "¿Quieres confirmar y guardar esta instalación? ✅"
            )
            
            teclado_confirmacion = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✅ Confirmar", callback_data="admin_confirmar_agregar_instalacion"),
                    InlineKeyboardButton("❌ Cancelar", callback_data="admin_cancelar_agregar_instalacion")
                ]
            ])
            
            await update.message.reply_text(resumen, reply_markup=teclado_confirmacion, parse_mode="Markdown")
            
    elif estado_info.get("accion") == "modificar":
        # Modificar instalación
        nombre_instalacion = estado_info.get("instalacion")
        campo = estado_info.get("campo")
        
        if campo == "foto" and nombre_instalacion in instalaciones.instalaciones_info:
            instalaciones.instalaciones_info[nombre_instalacion]["foto"] = foto_file_id
            instalaciones.guardar_instalaciones(instalaciones.instalaciones_info)
            admin_instalacion_estado.pop(user_id, None)
            context.user_data.pop("instalacion_modificar", None)
            context.user_data.pop("campo_modificar", None)
            
            await update.message.reply_text(
                f"✅ Foto de la instalación <b>{nombre_instalacion}</b> actualizada exitosamente.",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 Volver al menú", callback_data="admin_menu_instalaciones")]
                ])
            )


@solo_admins
async def manejar_respuesta_modificacion_instalacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja las respuestas durante la modificación de una instalación"""
    user_id = str(update.effective_user.id)
    
    if user_id not in admin_instalacion_estado:
        return

    estado_info = admin_instalacion_estado[user_id]
    
    if estado_info.get("accion") != "modificar":
        return

    texto = update.message.text.strip()
    nombre_instalacion = estado_info.get("instalacion")
    campo = estado_info.get("campo")

    if nombre_instalacion not in instalaciones.instalaciones_info:
        await update.message.reply_text("❌ Error: Instalación no encontrada.")
        admin_instalacion_estado.pop(user_id, None)
        return

    # Aplicar la modificación
    if campo == "nombre":
        nuevo_nombre = texto
        if nuevo_nombre != nombre_instalacion:
            instalaciones.instalaciones_info[nuevo_nombre] = instalaciones.instalaciones_info[nombre_instalacion].copy()
            del instalaciones.instalaciones_info[nombre_instalacion]
            nombre_instalacion = nuevo_nombre
    elif campo == "coordenadas":
        # Parsear coordenadas: latitud,longitud
        try:
            partes = texto.split(",")
            if len(partes) == 2:
                latitud = float(partes[0].strip())
                longitud = float(partes[1].strip())
                instalaciones.instalaciones_info[nombre_instalacion]["latitud"] = latitud
                instalaciones.instalaciones_info[nombre_instalacion]["longitud"] = longitud
            else:
                await update.message.reply_text("❌ Formato incorrecto. Usa: latitud,longitud")
                return
        except ValueError:
            await update.message.reply_text("❌ Error: Las coordenadas deben ser números válidos.")
            return
    elif campo == "foto":
        # Esta función solo maneja texto, las fotos se manejan en otra función
        if texto.lower() == "no":
            # No cambiar la foto, continuar
            instalaciones.guardar_instalaciones(instalaciones.instalaciones_info)
            admin_instalacion_estado.pop(user_id, None)
            context.user_data.pop("instalacion_modificar", None)
            context.user_data.pop("campo_modificar", None)
            await update.message.reply_text(
                f"✅ No se cambió la foto de la instalación <b>{nombre_instalacion}</b>.",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 Volver al menú", callback_data="admin_menu_instalaciones")]
                ])
            )
            return
        else:
            await update.message.reply_text("⚠️ Por favor, envía la foto directamente al bot (no una URL). Si no quieres cambiar la foto, envía 'no'.")
            return
    else:
        instalaciones.instalaciones_info[nombre_instalacion][campo] = texto

    instalaciones.guardar_instalaciones(instalaciones.instalaciones_info)
    admin_instalacion_estado.pop(user_id, None)
    context.user_data.pop("instalacion_modificar", None)
    context.user_data.pop("campo_modificar", None)

    await update.message.reply_text(
        f"✅ Campo <b>{campo}</b> de la instalación <b>{nombre_instalacion}</b> modificado exitosamente.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Volver al menú", callback_data="admin_menu_instalaciones")]
        ])
    )


@solo_admins
async def manejar_respuesta_agregar_instalacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja las respuestas durante la adición de una nueva instalación"""
    user_id = str(update.effective_user.id)
    
    if user_id not in admin_instalacion_estado:
        return

    estado_info = admin_instalacion_estado[user_id]
    
    if estado_info.get("accion") != "agregar":
        return

    texto = update.message.text.strip()
    estado_actual = estado_info.get("estado")

    if estado_actual == "esperando_nombre":
        context.user_data["nombre"] = texto
        admin_instalacion_estado[user_id]["estado"] = "esperando_direccion"
        await update.message.reply_text("📍 ¿Cuál es la dirección de la instalación?")

    elif estado_actual == "esperando_direccion":
        context.user_data["direccion"] = texto
        admin_instalacion_estado[user_id]["estado"] = "esperando_coordenadas"
        await update.message.reply_text("🗺️ Ingresa las coordenadas (formato: latitud,longitud)\nEjemplo: 23.1363,-82.3782\n\nO envía 'no' si no las tienes:")

    elif estado_actual == "esperando_coordenadas":
        if texto.lower() != "no":
            try:
                partes = texto.split(",")
                if len(partes) == 2:
                    latitud = float(partes[0].strip())
                    longitud = float(partes[1].strip())
                    context.user_data["latitud"] = latitud
                    context.user_data["longitud"] = longitud
                else:
                    await update.message.reply_text("❌ Formato incorrecto. Usa: latitud,longitud")
                    return
            except ValueError:
                await update.message.reply_text("❌ Error: Las coordenadas deben ser números válidos. Intenta de nuevo:")
                return
        admin_instalacion_estado[user_id]["estado"] = "esperando_foto"
        await update.message.reply_text("📷 Por favor, envía la foto de la instalación directamente al bot. Si no tienes foto, envía 'no'.")

    elif estado_actual == "esperando_foto":
        # Esta función solo maneja texto, las fotos se manejan en otra función
        if texto.lower() == "no":
            admin_instalacion_estado[user_id]["estado"] = "confirmacion"

        coordenadas_str = f"{context.user_data.get('latitud')}, {context.user_data.get('longitud')}" if context.user_data.get('latitud') else "No definidas"

        resumen = (
            f"🏟️ *Resumen de la nueva instalación:*\n\n"
            f"*Nombre:* {context.user_data['nombre']}\n"
            f"*Dirección:* {context.user_data['direccion']}\n"
            f"*Coordenadas:* {coordenadas_str}\n"
            f"*Foto:* {context.user_data.get('foto', 'No')}\n\n"
            "¿Quieres confirmar y guardar esta instalación? ✅"
        )

        teclado_confirmacion = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Confirmar", callback_data="admin_confirmar_agregar_instalacion"),
                InlineKeyboardButton("❌ Cancelar", callback_data="admin_cancelar_agregar_instalacion")
            ]
        ])

        await update.message.reply_text(resumen, reply_markup=teclado_confirmacion, parse_mode="Markdown")


@solo_admins
async def confirmar_agregar_instalacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Confirma y guarda la nueva instalación"""
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)
    
    if user_id not in admin_instalacion_estado:
        await query.answer("Error: No hay operación en curso", show_alert=True)
        return

    nombre = context.user_data.get("nombre", "").strip()
    if not nombre:
        await query.answer("Error: Nombre no válido", show_alert=True)
        return

    instalaciones.instalaciones_info[nombre] = {
        "direccion": context.user_data.get("direccion", "No disponible"),
        "latitud": context.user_data.get("latitud"),
        "longitud": context.user_data.get("longitud"),
        "foto": context.user_data.get("foto", None)
    }

    instalaciones.guardar_instalaciones(instalaciones.instalaciones_info)
    admin_instalacion_estado.pop(user_id, None)
    context.user_data.clear()

    await query.edit_message_text(
        "✅ *¡Instalación agregada exitosamente!*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Volver al menú", callback_data="admin_menu_instalaciones")]
        ])
    )


@solo_admins
async def cancelar_agregar_instalacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancela la adición de una nueva instalación"""
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)
    admin_instalacion_estado.pop(user_id, None)
    context.user_data.clear()

    await query.edit_message_text(
        "❌ Operación cancelada. No se guardó ningún dato.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Volver al menú", callback_data="admin_menu_instalaciones")]
        ])
    )



