

from telegram import Update, InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,CallbackQueryHandler,MessageHandler,filters
import usuarios
import deporte
import profesores
import instalaciones
import horarios
import actividades
import ayuda
import admin
import admin_panel
import admin_deportes
import admin_profesores
import admin_instalaciones

actividades.cargar_actividades()
deporte.cargar_deportes()
instalaciones.cargar_instalaciones()  

profesores.cargar_profesores()
usuarios.cargar_usuarios()

admin.cargar_admins()

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = str(user.id)

    if user_id not in usuarios.usuarios:
        usuarios.registro_estado[user_id] = "esperando_nombre"
        await update.message.reply_text(
            "👋 <b>¡Bienvenido al Bot Deportivo de la Universidad de La Habana!</b>\n\n"
            "🔐 Para comenzar, necesitamos algunos datos.\n\n"
            "📝 ¿Cuál es tu <b>nombre completo</b>?",
            parse_mode="HTML"
        )
    else:
        msg = (
            f"🙌 <b>¡Hola {usuarios.usuarios[user_id]['nombre']}!</b>\n\n"
            "🏟️ Bienvenido de nuevo al Bot de Deportes de la Universidad de La Habana.\n"
            "Explora actividades, entrenamientos y más. 🏀🏐🏊"
        )

        if admin.ADMIN_IDS and user_id in admin.ADMIN_IDS:
            teclado = [
                [InlineKeyboardButton("🔐 Panel de Administración", callback_data="admin_menu_principal")],
            ]
            await update.message.reply_text(
                msg,
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup(teclado)
            )
        else:
            await update.message.reply_text(
                msg,
                parse_mode="HTML"
            )



TOKEN = ""
with open("../token.txt", "r") as f:
    TOKEN = f.read().strip()


async def manejar_foto_privado(update, context):
    """Maneja cuando se envía una foto en chat privado"""
    user_id = str(update.effective_user.id)

    # Verificar estados de admin primero
    if user_id in admin_profesores.admin_profesor_estado:
        estado_info = admin_profesores.admin_profesor_estado[user_id]
        if estado_info.get("accion") == "agregar" and estado_info.get("estado") == "esperando_foto":
            await admin_profesores.manejar_foto_profesor(update, context)
        elif estado_info.get("accion") == "modificar" and estado_info.get("campo") == "foto":
            await admin_profesores.manejar_foto_profesor(update, context)
    elif user_id in admin_instalaciones.admin_instalacion_estado:
        estado_info = admin_instalaciones.admin_instalacion_estado[user_id]
        if estado_info.get("accion") == "agregar" and estado_info.get("estado") == "esperando_foto":
            await admin_instalaciones.manejar_foto_instalacion(update, context)
        elif estado_info.get("accion") == "modificar" and estado_info.get("campo") == "foto":
            await admin_instalaciones.manejar_foto_instalacion(update, context)
    else:
        await update.message.reply_text("🤖 No estás en ningún flujo que requiera foto. Usa /start para comenzar.")


async def manejar_texto_privado(update, context):
    user_id = str(update.effective_user.id)

    # Verificar estados de admin primero
    if user_id in admin_deportes.admin_deporte_estado:
        estado_info = admin_deportes.admin_deporte_estado[user_id]
        if estado_info.get("accion") == "agregar":
            await admin_deportes.manejar_respuesta_agregar_deporte(update, context)
        elif estado_info.get("accion") == "modificar":
            await admin_deportes.manejar_respuesta_modificacion_deporte(update, context)
    elif user_id in admin_profesores.admin_profesor_estado:
        estado_info = admin_profesores.admin_profesor_estado[user_id]
        if estado_info.get("accion") == "agregar":
            await admin_profesores.manejar_respuesta_agregar_profesor(update, context)
        elif estado_info.get("accion") == "modificar":
            await admin_profesores.manejar_respuesta_modificacion_profesor(update, context)
    elif user_id in admin_instalaciones.admin_instalacion_estado:
        estado_info = admin_instalaciones.admin_instalacion_estado[user_id]
        if estado_info.get("accion") == "agregar":
            await admin_instalaciones.manejar_respuesta_agregar_instalacion(update, context)
        elif estado_info.get("accion") == "modificar":
            await admin_instalaciones.manejar_respuesta_modificacion_instalacion(update, context)
    # Estados normales de usuarios
    elif user_id in usuarios.registro_estado:
        await usuarios.manejar_respuesta_registro(update, context)
    elif user_id in deporte.deporte_estado:
        await deporte.manejar_respuesta_deporte(update, context)
    elif user_id in profesores.profesores_estado:
        await profesores.manejar_respuesta_profesores(update, context)
    else:
        await update.message.reply_text("🤖 No estás en ningún flujo. Usa /start para comenzar.")

# Define tus filtros como clases



application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", welcome))
application.add_handler(CommandHandler("registrar", usuarios.registro))



application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE,
        manejar_texto_privado
    ))

application.add_handler(MessageHandler(
        filters.PHOTO & filters.ChatType.PRIVATE,
        manejar_foto_privado
    ))

application.add_handler(CallbackQueryHandler(usuarios.manejar_tipo_callback, pattern="^tipo_"))
application.add_handler(CallbackQueryHandler(deporte.manejar_confirmacion_deporte, pattern="^confirmar_deporte|cancelar_deporte$"))
application.add_handler(CallbackQueryHandler(profesores.manejar_confirmacion_profesores, pattern="^confirmar_profesor|cancelar_profesor$"))


# application.add_handler(CommandHandler("registrar", registrar))
# application.add_handler(CommandHandler("info_estudiante", info_estudiante))
# application.add_handler(CallbackQueryHandler(procesar_tipo_usuario, pattern=r"^tipo_"))
application.add_handler(CommandHandler("horario", horarios.horario))
application.add_handler(CallbackQueryHandler(horarios.mostrar_horario_dia, pattern="^horario_"))
application.add_handler(CallbackQueryHandler(horarios.volver_horarios, pattern="^volver_horarios$"))
application.add_handler(CommandHandler("listar_deportes", deporte.listar_deportes))
application.add_handler(CommandHandler("listar_profesores", profesores.listar_profesores))
application.add_handler(CommandHandler("listar_instalaciones", instalaciones.listar_instalaciones))
application.add_handler(CallbackQueryHandler(instalaciones.mostrar_info_instalacion, pattern="^instalacion_"))
application.add_handler(CallbackQueryHandler(instalaciones.listar_instalaciones_callback, pattern="^volver_instalaciones$"))
application.add_handler(CallbackQueryHandler(instalaciones.cambiar_pagina_instalaciones, pattern="^pagina_instalaciones_"))
application.add_handler(CommandHandler("ayuda", ayuda.ayuda))
application.add_handler(CommandHandler("actividades", actividades.mostrar_noticias))

application.add_handler(CallbackQueryHandler(profesores.mostrar_info_profesor,pattern="^profesor_"))
application.add_handler(CallbackQueryHandler(deporte.mostrar_info_deporte,pattern="^deporte_"))


application.add_handler(CallbackQueryHandler(deporte.listar_deportes_callback, pattern="^volver_deportes$"))
application.add_handler(CallbackQueryHandler(profesores.listar_profesores_callback, pattern="^volver_profesores$"))


application.add_handler(CallbackQueryHandler(deporte.cambiar_pagina_deportes, pattern="^pagina_deportes_"))
application.add_handler(CallbackQueryHandler(profesores.cambiar_pagina_profesores, pattern="^pagina_profesores_"))

# ========== HANDLERS DE ADMINISTRACIÓN ==========

# Panel principal de admin
application.add_handler(CallbackQueryHandler(admin_panel.mostrar_menu_admin, pattern="^admin_menu_principal$"))
application.add_handler(CallbackQueryHandler(admin_panel.volver_inicio, pattern="^admin_volver_inicio$"))

# Submenús de admin
application.add_handler(CallbackQueryHandler(admin_panel.mostrar_submenu_deportes, pattern="^admin_menu_deportes$"))
application.add_handler(CallbackQueryHandler(admin_panel.mostrar_submenu_profesores, pattern="^admin_menu_profesores$"))
application.add_handler(CallbackQueryHandler(admin_panel.mostrar_submenu_instalaciones, pattern="^admin_menu_instalaciones$"))

# Gestión de Deportes
application.add_handler(CallbackQueryHandler(admin_deportes.agregar_deporte, pattern="^admin_agregar_deporte$"))
application.add_handler(CallbackQueryHandler(admin_deportes.listar_deportes_para_modificar, pattern="^admin_modificar_deporte_lista$"))
application.add_handler(CallbackQueryHandler(admin_deportes.listar_deportes_para_eliminar, pattern="^admin_eliminar_deporte_lista$"))
application.add_handler(CallbackQueryHandler(admin_deportes.listar_deportes_admin, pattern="^admin_listar_deportes$"))
application.add_handler(CallbackQueryHandler(admin_deportes.confirmar_agregar_deporte, pattern="^admin_confirmar_agregar_deporte$"))
application.add_handler(CallbackQueryHandler(admin_deportes.cancelar_agregar_deporte, pattern="^admin_cancelar_agregar_deporte$"))
application.add_handler(CallbackQueryHandler(admin_deportes.ejecutar_eliminar_deporte, pattern="^admin_confirmar_eliminar_deporte_"))
application.add_handler(CallbackQueryHandler(admin_deportes.iniciar_modificacion_campo_deporte, pattern="^admin_modificar_campo_deporte_"))
application.add_handler(CallbackQueryHandler(admin_deportes.seleccionar_campo_modificar_deporte, pattern="^admin_modificar_deporte_"))
application.add_handler(CallbackQueryHandler(admin_deportes.confirmar_eliminar_deporte, pattern="^admin_eliminar_deporte_"))
application.add_handler(CallbackQueryHandler(admin_deportes.ver_deporte_admin, pattern="^admin_ver_deporte_"))
application.add_handler(CallbackQueryHandler(admin_deportes.cambiar_pagina_deportes_admin, pattern="^admin_pagina_.*_deportes_"))

# Gestión de Profesores
application.add_handler(CallbackQueryHandler(admin_profesores.agregar_profesor, pattern="^admin_agregar_profesor$"))
application.add_handler(CallbackQueryHandler(admin_profesores.listar_profesores_para_modificar, pattern="^admin_modificar_profesor_lista$"))
application.add_handler(CallbackQueryHandler(admin_profesores.listar_profesores_para_eliminar, pattern="^admin_eliminar_profesor_lista$"))
application.add_handler(CallbackQueryHandler(admin_profesores.listar_profesores_admin, pattern="^admin_listar_profesores$"))
application.add_handler(CallbackQueryHandler(admin_profesores.confirmar_agregar_profesor, pattern="^admin_confirmar_agregar_profesor$"))
application.add_handler(CallbackQueryHandler(admin_profesores.cancelar_agregar_profesor, pattern="^admin_cancelar_agregar_profesor$"))
application.add_handler(CallbackQueryHandler(admin_profesores.ejecutar_eliminar_profesor, pattern="^admin_confirmar_eliminar_profesor_"))
application.add_handler(CallbackQueryHandler(admin_profesores.iniciar_modificacion_campo_profesor, pattern="^admin_modificar_campo_profesor_"))
application.add_handler(CallbackQueryHandler(admin_profesores.seleccionar_campo_modificar_profesor, pattern="^admin_modificar_profesor_"))
application.add_handler(CallbackQueryHandler(admin_profesores.confirmar_eliminar_profesor, pattern="^admin_eliminar_profesor_"))
application.add_handler(CallbackQueryHandler(admin_profesores.ver_profesor_admin, pattern="^admin_ver_profesor_"))
application.add_handler(CallbackQueryHandler(admin_profesores.cambiar_pagina_profesores_admin, pattern="^admin_pagina_.*_profesores_"))

# Gestión de Instalaciones
application.add_handler(CallbackQueryHandler(admin_instalaciones.agregar_instalacion, pattern="^admin_agregar_instalacion$"))
application.add_handler(CallbackQueryHandler(admin_instalaciones.listar_instalaciones_para_modificar, pattern="^admin_modificar_instalacion_lista$"))
application.add_handler(CallbackQueryHandler(admin_instalaciones.listar_instalaciones_para_eliminar, pattern="^admin_eliminar_instalacion_lista$"))
application.add_handler(CallbackQueryHandler(admin_instalaciones.listar_instalaciones_admin, pattern="^admin_listar_instalaciones$"))
application.add_handler(CallbackQueryHandler(admin_instalaciones.confirmar_agregar_instalacion, pattern="^admin_confirmar_agregar_instalacion$"))
application.add_handler(CallbackQueryHandler(admin_instalaciones.cancelar_agregar_instalacion, pattern="^admin_cancelar_agregar_instalacion$"))
application.add_handler(CallbackQueryHandler(admin_instalaciones.ejecutar_eliminar_instalacion, pattern="^admin_confirmar_eliminar_instalacion_"))
application.add_handler(CallbackQueryHandler(admin_instalaciones.iniciar_modificacion_campo_instalacion, pattern="^admin_modificar_campo_instalacion_"))
application.add_handler(CallbackQueryHandler(admin_instalaciones.seleccionar_campo_modificar_instalacion, pattern="^admin_modificar_instalacion_"))
application.add_handler(CallbackQueryHandler(admin_instalaciones.confirmar_eliminar_instalacion, pattern="^admin_eliminar_instalacion_"))
application.add_handler(CallbackQueryHandler(admin_instalaciones.ver_instalacion_admin, pattern="^admin_ver_instalacion_"))
application.add_handler(CallbackQueryHandler(admin_instalaciones.cambiar_pagina_instalaciones_admin, pattern="^admin_pagina_.*_instalaciones_"))



application.run_polling(allowed_updates=Update.ALL_TYPES)
